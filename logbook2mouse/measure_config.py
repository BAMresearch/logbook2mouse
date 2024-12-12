from pathlib import Path
import os
import time
import h5py
import logging
import caproto.threading.pyepics_compat as epics
import logbook2mouse.file_management as filemanagement
import logbook2mouse.detector as detector
import logbook2mouse.metadata as meta
from logbook2mouse.experiment import get_address
from logbook2mouse.logbook_reader import Logbook2MouseEntry

def move_motor(
    motorname, position: float, prefix: str = "mc0", parrot_prefix: str = "pa0"
):
    """Move the motor to the requested value and set parrot PVs."""
    robust_caput(f"{prefix}:{motorname}", position)
    # figure out which parrot variable to use
    if motorname.startswith("s") and motorname != "shutter":
        slitnumber = motorname[1]
        blade = motorname[2:]
        if blade in ["hl", "hr"]:
            parrot_pv = f"{parrot_prefix}:config:slits:horizontal{slitnumber}:{blade}"
        else:
            parrot_pv = f"{parrot_prefix}:config:slits:vertical{slitnumber}:{blade}"
    elif "bs" in motorname:
        parrot_pv = f"{parrot_prefix}:config:beamstop:{motorname}"
    elif "det" in motorname:
        parrot_pv = f"{parrot_prefix}:config:{motorname}"
    else:
        # assume all other motors have their own variable
        parrot_pv = f"{parrot_prefix}:environment:motors:{motorname}"
    actual_value = epics.caget(f"{prefix}:{motorname}")
    epics.caput(parrot_pv, actual_value)
    return actual_value

def move_to_sampleposition(experiment, entry: Logbook2MouseEntry, blank: bool = False):
    """Move the motors according to the sample position entries."""
    for motor in entry.sampleposition.keys():
        addr = None  # some like xsam don't exist
        if "blank" in motor:
            motorname = motor.rstrip(".blank")
        else:
            motorname = motor
        addr = get_address(experiment, motorname)
        if addr is not None:  # xsam can't be moved
            if blank:
                if "blank" in motor:
                    move_motor(motorname, entry.sampleposition[motor], prefix=addr.split(":")[0])
            else:
                if "blank" not in motor:
                    move_motor(motorname, entry.sampleposition[motor], prefix=addr.split(":")[0])



def move_motor_fromconfig(motorname, imcrawfile="im_craw.nxs", prefix="ims"):
    with h5py.File(imcrawfile) as h5:
        motorpos = float(h5[f"/saxs/Saxslab/{motorname}"][()])
    move_motor(motorname, motorpos, prefix=prefix, parrot_prefix="pa0")
    logging.info(f"Moved motor {motorname} to stored position {motorpos}.")
    return motorname, motorpos


def moveto_config(
    required_pvs,
    config_path: Path = Path("/home/ws8665-epics/data/configurations"),
    config_no: int = 110,
):
    config_no = int(float(config_no)) if type(config_no) == str else int(config_no)
    configfile = config_path / f"{config_no}.nxs"
    if not configfile.is_file():
        raise FileNotFoundError(f"File {configfile} does not exist.")

    pvs_not_to_move = ["shutter", "pressure", "pa0", "image"]
    for pv in required_pvs:
        if not any(substr in pv for substr in pvs_not_to_move):
            prefix, motorname = pv.split(":")
            name, position = move_motor_fromconfig(
                motorname, imcrawfile=configfile, prefix=prefix
            )
            if name == "bsr":
                bsr = position

    epics.caput("pa0:config:config_id", config_no)
    return {"bsr": position}


def robust_caput(pv, value, timeout=5):
    epics.caput(pv, value, timeout=timeout)
    dmov_addr = pv + ".DMOV"
    new_position = epics.caget(dmov_addr)
    while new_position != 1:
        time.sleep(0.2)
        new_position = epics.caget(dmov_addr)


def measure_profile(
    entry,
    store_location,
    experiment,
    mode="blank",
    duration: int = 20,  # add functionality to determine time needed later
):
    if not os.path.exists(store_location):
        os.mkdir(store_location)
    epics.caput(f"{experiment.parrot_prefix}:exp:count_time", duration)
    if mode == "blank":
        # to do: determine motors from pvs, or logbook
        move_to_sampleposition(experiment, entry, blank = True)
        beamprofilepath = store_location / "beam_profile"
        if not os.path.exists(beamprofilepath):
            os.mkdir(beamprofilepath)
    else:
        move_to_sampleposition(experiment, entry)
        beamprofilepath = store_location / "beam_profile_through_sample"
        if not os.path.exists(beamprofilepath):
            os.mkdir(beamprofilepath)
    epics.caput("source_cu:shutter", 1, wait=True)
    detector.measurement(
        experiment,
        duration=duration,
        store_location=beamprofilepath,
    )

    epics.caput("source_cu:shutter", 0, wait=True)

    # communicate to image processing ioc which expects the _data_*h5 files
    for fname in beamprofilepath.glob("*data*.h5"):
        if beamprofilepath.stem == "beam_profile":
            pv = "ImagePathPrimary"
        else:
            pv = "ImagePathSecondary"
        epics.caput(f"{experiment.image_processing_prefix}:{pv}", str(fname).encode('utf-8'))


def measure_dataset(
        entry, experiment, store_location: Path, duration: int = 600,
):
    epics.caput(f"{experiment.parrot_prefix}:exp:frame_time", experiment.eiger.frame_time)
    bsr_addr = get_address(experiment, "bsr")
    bsr = epics.caget(bsr_addr)
    move_motor("bsr", 270, prefix=bsr_addr.split(":")[0])
    for mode in ["blank", "sample"]:
        measure_profile(
            entry, store_location, experiment, mode=mode, duration=2
        )
    move_to_sampleposition(experiment, entry)
    move_motor("bsr", bsr, prefix="ims")
    epics.caput("source_cu:shutter", 1, wait=True)
    epics.caput(f"{experiment.parrot_prefix}:exp:count_time", duration)
    detector.measurement(
        experiment, duration=duration, store_location=store_location
    )
    epics.caput("source_cu:shutter", 0, wait=True)

def measure_at_config(
    config_no: int,
    entry,
    experiment,
    repetitions=None,
    duration: int = 600,
):
    """Measure with the default settings for each configuration."""

    config_no = int(float(config_no)) if type(config_no) == str else int(config_no)
    config_dict = moveto_config(
        experiment.required_pvs,
        config_path=Path("/mnt/vsi-db/Measurements/SAXS002/data/configurations"),
        config_no=config_no,
    )

    meta.logbook2parrot(entry)

    if repetitions is None:
        if int(config_no) in [117, 127]:
            repetitions = 16
        elif int(config_no) in [115, 125]:
            repetitions = 10
        elif int(config_no) in [113, 123]:
            repetitions = 5
        elif int(config_no) in [110]:
            repetitions = 4
        else:
            repetitions = 1

    logger = logging.getLogger("measurement")
    logger.info(f"Measuring {repetitions} repetitions.")

    epics.caput(f"{experiment.parrot_prefix}:exp:nrep", repetitions)
    scan_counter = 0
    work_directory = filemanagement.work_directory(entry)
    ymd = entry.date.strftime("%Y%m%d")
    epics.caput(f"{experiment.parrot_prefix}:exp:logbook_date", ymd)

    for i in range(repetitions):
        next_measurement_no = filemanagement.scan_counter_next(
            scan_counter, work_directory, entry
        )
        store_location = (
            work_directory / f"{ymd}_{entry.batchnum}_{next_measurement_no}"
        )
        measure_dataset(
            entry,
            experiment,
            store_location=store_location,
            duration=duration,
        )


def standard_configurations(keyword: str = "standard"):
    if keyword == "standard":
        configurations = [150, 151, 152, 153, 154, 155, 156, 123, 125, 127]
    elif keyword == "capillary":
        configurations = [110, 123, 125, 127]
    else:
        raise ValueError(
            f"""Configuration set {keyword} is not defined. 
Specify the configurations to measure explicitly one by one, 
with e.g. 'key1=configuration' and 'value1=123' for configuration 123."""
        )
    return configurations
