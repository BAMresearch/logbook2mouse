from pathlib import Path
import h5py
import logging
import caproto.threading.pyepics_compat as epics


def move_motor(motorname, imcrawfile="im_craw.nxs", prefix="ims"):
    with h5py.File(imcrawfile) as h5:
        motorpos = float(h5[f"/saxs/Saxslab/{motorname}"][()])
    epics.caput(f"{prefix}:{motorname}", motorpos)
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
        prefix, motorname = pv.split(":")
        name, position = move_motor(motorname, imcrawfile=configfile, prefix=prefix)
        if name == "bsr":
            bsr = position
    return {"bsr": position}


def measure_profile(
    entry,
    store_location,
    dEiger_connection,
    mode="blank",
    duration: int = 20,  # add functionality to determine time needed later
):
    if mode == "blank":
        epics.caput("mc0:ysam", entry.blankpositiony)
        epics.caput("mc0:zsam", entry.blankpositionz)
        beamprofilepath = store_location / "beam_profile"
        if not os.path.exists(beamprofilepath):
            mkdir(beamprofilepath)
    else:
        epics.caput("mc0:ysam", entry.positiony)
        epics.caput("mc0:zsam", entry.positionz)
        beamprofilepath = store_location / "beam_profile_through_sample"
        if not os.path.exists(beamprofilepath):
            mkdir(beamprofilepath)
    epics.caput("source_cu:shutter", "Open")
    detector.measurement(
        dEiger_connection, duration=duration, store_location=store_location
    )
    epics.caput("source_cu:shutter", "Closed")


def measure_dataset(
    entry, dEiger_connection, store_location: Path, bsr: float, duration: int = 600
):
    epics.caput("ims:bsr", 270)
    for mode in ["blank", "sample"]:
        measure_profile(
            entry, store_location, dEiger_connection, mode=mode, duration=20
        )
    epics.caput("mc0:ysam", entry.positiony)
    epics.caput("mc0:zsam", entry.positionz)
    epics.caput("ims:bsr", bsr)
    epics.caput("source_cu:shutter", "Open")
    detector.measurement(
        dEiger_connection, duration=duration, store_location=store_location
    )
    epics.caput("source_cu:shutter", "Closed")


def measure_at_config(
    config_no: int,
    entry,
    required_pvs,
    dEiger_connection,
    repetitions=None,
    duration: int = 600,
):
    """Measure with the default settings for each configuration."""
    config_dict = moveto_config(
        required_pvs,
        config_path=Path("/mnt/vsi-db/Measurements/SAXS002/data/configurations"),
        config_no=config_no,
    )

    if repetitions is None:
        if config_no in [117, 127]:
            repetitions = 16
        elif config_no in [115, 125]:
            repetitions = 10
        elif config_no in [113, 123]:
            repetitions = 5
        else:
            repetitions = 1

    scan_counter = 0
    work_directory = filemanagement.work_directory(entry)
    ymd = entry.date.strftime("%Y%m%d")
    for i in range(repetitions):
        next_measurement_no = filemanagement.scan_counter_next(
            scan_counter, work_directory, entry
        )
        store_location = work_directory / f"{ymd}_{next_measurement_no}"
        measure_dataset(
            entry,
            dEiger_connection,
            store_location=store_location,
            bsr=config_dict["bsr"],
            duration=duration,
        )
