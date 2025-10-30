from pathlib import Path
import os
import time
import h5py
from math import isclose
import logging
from shutil import copy
from typing import Dict, List, Optional
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
    actual_value = epics.caget(f"{prefix}:{motorname}.RBV")
    epics.caput(parrot_pv, actual_value)
    return actual_value

def move_to_sampleposition(experiment, sampleposition: Dict[str, float], blank: bool = False):
    """Move the motors according to the sample position entries."""
    for motor in sampleposition.keys():
        addr = None  # some like xsam don't exist
        if "blank" in motor:
            motorname = motor.rstrip(".blank")
        else:
            motorname = motor
        addr = get_address(experiment, motorname)
        if addr is not None:  # xsam can't be moved
            if blank:
                if "blank" in motor:
                    move_motor(motorname, sampleposition[motor], prefix=addr.split(":")[0])
            else:
                if "blank" not in motor:
                    move_motor(motorname, sampleposition[motor], prefix=addr.split(":")[0])



def move_motor_fromconfig(motorname, imcrawfile="im_craw.nxs", prefix="ims"):
    with h5py.File(imcrawfile) as h5:
        motorpos = float(h5[f"/saxs/Saxslab/{motorname}"][()])
    current_position = epics.caget(f"{prefix}:{motorname}.VAL")  # use set position to ensure close match
    if isclose(current_position, motorpos, rel_tol = 1e-8, abs_tol = 1e-5):
        logging.info(f"Motor {motorname} already at stored position {motorpos}.")
    else:
        move_motor(motorname, motorpos, prefix=prefix, parrot_prefix="pa0")
        logging.info(f"Moved motor {motorname} to stored position {motorpos}.")

    return motorname, motorpos


def moveto_config(
    experiment,
    config_path: Path = Path.home() / "data/configurations",
    config_no: int = 110,
):
    config_no = int(float(config_no)) if type(config_no) == str else int(config_no)
    # don't move at all if we are at this config according to parrot
    latest_config = int(epics.caget(f"{experiment.parrot_prefix}:config:config_id"))
    if latest_config == config_no:
        # exit without moving
        return

    configfile = config_path / f"{config_no}.nxs"
    if not configfile.is_file():
        raise FileNotFoundError(f"File {configfile} does not exist.")

    pvs_to_move = ["ims"]  # only move motors on ims, i.e. not sample motors
    for pv in experiment.required_pvs:
        if any(substr in pv for substr in pvs_to_move):
            prefix, motorname = pv.split(":")
            name, position = move_motor_fromconfig(
                motorname, imcrawfile=configfile, prefix=prefix
            )

    epics.caput(f"{experiment.parrot_prefix}:config:config_id", config_no)
    if str(config_no).startswith("1"):
        source_name = "source_cu"
        epics.caput(f"{experiment.eiger_prefix}:PhotonEnergy", 8050)
        epics.caput(f"{experiment.eiger_prefix}:ThresholdEnergy", 4025)
    elif str(config_no).startswith("2"):
        source_name = "source_mo"
        epics.caput(f"{experiment.eiger_prefix}:PhotonEnergy", 17400)
        epics.caput(f"{experiment.eiger_prefix}:ThresholdEnergy", 8700)
    else:
        raise ValueError(f"Configuration number must start with either 1 (Cu source) or 2 (Mo source), received {config_no}")
    epics.caput(f"{experiment.parrot_prefix}:config:source", source_name)
    return


def robust_caput(pv, value, timeout=5):
    epics.caput(pv, value, timeout=timeout)
    dmov_addr = pv + ".DMOV"
    new_position = epics.caget(dmov_addr)
    while new_position != 1:
        time.sleep(0.2)
        new_position = epics.caget(dmov_addr)


def measure_profile(
    sampleposition,
    store_location,
    experiment,
    mode="blank",
    duration: int = 20,  # add functionality to determine time needed later
):
    epics.caput(f"{experiment.parrot_prefix}:exp:count_time", duration)
    if mode == "blank":
        move_to_sampleposition(experiment, sampleposition, blank = True)
        beamprofilepath = store_location / "beam_profile"
        os.makedirs(beamprofilepath, exist_ok = True)
    elif mode == "sample":
        move_to_sampleposition(experiment, sampleposition)
        beamprofilepath = store_location / "beam_profile_through_sample"
        os.makedirs(beamprofilepath, exist_ok = True)
    elif mode == "scan":
        # do not move
        beamprofilepath = store_location
        os.makedirs(beamprofilepath, exist_ok = True)
    else:
        raise ValueError(f"Unknown profile measurement mode {mode}. Available options: 'blank', 'sample', 'scan'.")

    source_name = epics.caget(f"{experiment.parrot_prefix}:config:source", as_string=True)
    if mode in ["blank", "sample"]:
        epics.caput(f"{source_name}:shutter", 1, wait=True)
    detector.measurement(
        experiment,
        duration=duration,
        store_location=beamprofilepath,
    )
    if mode in ["blank", "sample"]:
        epics.caput(f"{source_name}:shutter", 0, wait=True)

    # communicate to image processing ioc which expects the _data_*h5 files
    for fname in beamprofilepath.glob("*data*.h5"):
        if beamprofilepath.stem == "beam_profile":
            pv = "ImagePathPrimary"
        else:
            pv = "ImagePathSecondary"
        epics.caput(f"{experiment.image_processing_prefix}:{pv}", str(fname).encode('utf-8'))

        copy(fname, "/home/ws8665-epics/scan-using-epics-ioc/.current/current.h5")

def measure_dataset(
        entry, experiment, store_location: Path, duration: float = 600.0,
):
    frame_time = epics.caget(f"{experiment.eiger_prefix}:FrameTime")
    epics.caput(f"{experiment.parrot_prefix}:exp:frame_time", frame_time)
    bsr_addr = get_address(experiment, "bsr")
    bsr = epics.caget(bsr_addr)
    move_motor("bsr", 270, prefix=bsr_addr.split(":")[0])
    for mode in ["blank", "sample"]:
        measure_profile(
            entry.sampleposition, store_location, experiment, mode=mode, duration=20
        )
    move_to_sampleposition(experiment, entry.sampleposition)
    move_motor("bsr", bsr, prefix="ims")
    source_name = epics.caget(f"{experiment.parrot_prefix}:config:source", as_string=True)
    epics.caput(f"{source_name}:shutter", 1, wait=True)
    epics.caput(f"{experiment.parrot_prefix}:exp:count_time", duration)
    detector.measurement(
        experiment, duration=duration, store_location=store_location
    )

    for fname in store_location.glob("*data*.h5"):
        copy(fname, "/home/ws8665-epics/scan-using-epics-ioc/.current/current.h5")

    epics.caput(f"{source_name}:shutter", 0, wait=True)

def measure_at_config(
    config_no: int,
    entry,
    experiment,
    repetitions=None,
    duration: int = 600,
):
    """Measure with the default settings for each configuration."""

    config_no = int(float(config_no)) if type(config_no) == str else int(config_no)
    moveto_config(
        experiment,
        config_path=Path.home() / "data/configurations",
        config_no=config_no,
    )

    meta.logbook2parrot(entry)

    if repetitions is None:
        repetitions = default_repetitions(config_no)

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
        # update the counter for measurement progress
        measurements_so_far = epics.caget(f'{experiment.parrot_prefix}:exp:progress:measurements_completed')
        epics.caput(f'{experiment.parrot_prefix}:exp:progress:measurements_completed', measurements_so_far + 1)


def standard_configurations(keyword: str = "standard"):
    if keyword == "standard":
        configurations = [160, 161, 162, 163, 164, 165, 166, 123, 125, 127]
    elif keyword == "capillary":
        configurations = [110, 123, 125, 127]
    elif keyword == "cu_waxs":
        configurations = [160, 161, 162, 163, 164, 165, 166, 123]
    elif keyword == "mo_extension":
        configurations = [250, 251, 252, 253, 254, 255, 256, 223]
    elif keyword == "mo_standard":
        configurations = [250, 251, 252, 253, 254, 255, 256, 223, 225, 226]
    else:
        raise ValueError(
            f"""Configuration set {keyword} is not defined. 
Specify the configurations to measure explicitly one by one, 
with e.g. 'key1=configuration' and 'value1=123' for configuration 123."""
        )
    return configurations

def default_repetitions(config_no: int = 110):
    if config_no in [117, 127, 226]:
        repetitions = 16
    elif config_no in [115, 125, 225]:
        repetitions = 10
    elif config_no in [113, 123, 223]:
        repetitions = 5
    elif config_no in [110]:
        repetitions = 4
    else:
        repetitions = 1
    return repetitions
