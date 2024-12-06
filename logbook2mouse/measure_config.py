from pathlib import Path
import os
import time
import h5py
import logging
import caproto.threading.pyepics_compat as epics
import logbook2mouse.file_management as filemanagement
import logbook2mouse.detector as detector
import logbook2mouse.metadata as meta


def move_motor(
    motorname, position: float, prefix: str = "mc0", parrot_prefix: str = "pa0"
):
    """Move the motor to the requested value and set parrot PVs."""
    epics.caput(f"{prefix}:{motorname}", position, wait=True)
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


def move_motor_fromconfig(motorname, imcrawfile="im_craw.nxs", prefix="ims"):
    with h5py.File(imcrawfile) as h5:
        motorpos = float(h5[f"/saxs/Saxslab/{motorname}"][()])
    move_motor(motorname, motorpos, prefix=prefix, parrot_prefix="pa0")
    logging.info(f"Moved motor {motorname} to stored position {motorpos}.")
    return motorname, motorpos


def moveto_config(
    required_pvs,
    config_path: Path = Path("/mnt/vsi-db/Measurements/SAXS002/data/configurations"),
    config_no: int = 110,
):
    configfile = config_path / f"{config_no}.nxs"
    if not configfile.is_file():
        raise FileNotFoundError(f"File {configfile} does not exist.")

    for pv in required_pvs:
        if "shutter" not in pv:
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
    new_position = epics.caget(pv)
    while new_position != value:
        time.sleep(0.2)
        new_position = epics.caget(pv)


def measure_profile(
    entry,
    store_location,
    dEiger_connection,
    mode="blank",
    duration: int = 20,  # add functionality to determine time needed later
    parrot_prefix: str = "pa0"
):
    if not os.path.exists(store_location):
        os.mkdir(store_location)
    epics.caput(f"{parrot_prefix}:exp:count_time", duration)
    if mode == "blank":
        move_motor("ysam", entry.blankpositiony, prefix="mc0")
        move_motor("zsam", entry.blankpositionz, prefix="mc0")
        beamprofilepath = store_location / "beam_profile"
        if not os.path.exists(beamprofilepath):
            os.mkdir(beamprofilepath)
    else:
        move_motor("ysam", entry.positiony, prefix="mc0")
        move_motor("zsam", entry.positionz, prefix="mc0")
        beamprofilepath = store_location / "beam_profile_through_sample"
        if not os.path.exists(beamprofilepath):
            os.mkdir(beamprofilepath)
    robust_caput("source_cu:shutter", 1, timeout=5)
    detector.measurement(
        dEiger_connection,
        duration=duration,
        store_location=beamprofilepath,
    )
    robust_caput("source_cu:shutter", 0, timeout=5)


def measure_dataset(
        entry, dEiger_connection, store_location: Path, bsr: float, duration: int = 600,
        parrot_prefix: str = "pa0",
):
    epics.caput(f"{parrot_prefix}:exp:frame_time", dEiger_connection.frame_time)
    move_motor("bsr", 270, prefix="ims")
    for mode in ["blank", "sample"]:
        measure_profile(
            entry, store_location, dEiger_connection, mode=mode, duration=20
        )
    move_motor("ysam", entry.positiony, prefix="mc0")
    move_motor("zsam", entry.positionz, prefix="mc0")
    move_motor("bsr", bsr, prefix="ims")
    robust_caput("source_cu:shutter", 1, timeout=5)
    epics.caput(f"{parrot_prefix}:exp:count_time", duration)
    detector.measurement(
        dEiger_connection, duration=duration, store_location=store_location
    )
    robust_caput("source_cu:shutter", 0, timeout=5)

def measure_at_config(
    config_no: int,
    entry,
    required_pvs,
    dEiger_connection,
    repetitions=None,
    duration: int = 600,
    parrot_prefix: str = "pa0"
):
    """Measure with the default settings for each configuration."""
    config_dict = moveto_config(
        required_pvs,
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

    logger = logging.getLogger("logbook2mouse")
    logger.info(f"Measuring {repetitions} repetitions.")

    epics.caput(f"{parrot_prefix}:exp:nrep", repetitions)
    scan_counter = 0
    work_directory = filemanagement.work_directory(entry)
    ymd = entry.date.strftime("%Y%m%d")
    epics.caput(f"{parrot_prefix}:exp:logbook_date", ymd)
    for i in range(repetitions):
        next_measurement_no = filemanagement.scan_counter_next(
            scan_counter, work_directory, entry
        )
        store_location = (
            work_directory / f"{ymd}_{entry.batchnum}_{next_measurement_no}"
        )
        measure_dataset(
            entry,
            dEiger_connection,
            store_location=store_location,
            bsr=config_dict["bsr"],
            duration=duration,
        )


def standard_configurations(keyword: str = "standard"):
    if keyword == "standard":
        configurations = [151, 152, 153, 154, 155, 156, 123, 125, 127]
    elif keyword == "capillary":
        configurations = [110, 113, 115, 117]
    else:
        raise ValueError(
            f"Configuration set {keyword} is not defined. Specify the configurations to measure explicitly one by one, with e.g. 'key1=configuration' and 'value1=123' for configuration 123."
        )
    return configurations
