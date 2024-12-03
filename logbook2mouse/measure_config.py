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
