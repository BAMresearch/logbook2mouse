from logbook2mouse.measure_config import (
    move_motor,
    measure_profile,
    move_to_sampleposition,
)
from logbook2mouse.experiment import get_address
from logbook2mouse.file_management import scan_counter_simple
import epics
from csv import DictWriter
from pathlib import Path
from shutil import copyfile
import numpy as np
import os, time


def create_scandir(work_dir):
    os.makedirs(work_dir, exist_ok=True)
    new_dir_no = scan_counter_simple(0, work_dir)
    scandir = work_dir / f"scan_{new_dir_no}"
    os.makedirs(scandir, exist_ok=True)
    return scandir


def scan(
    motorname,
    scan_start,
    scan_end,
    npoints,
    seconds,
    experiment,
    sampleposition,
    store_location,
    save_data=False,
):
    """Scan and record transmission relative to the current position."""
    motor_addr = get_address(experiment, motorname)
    prefix = motor_addr.rstrip(f":{motorname}")
    current_pos = epics.caget(motor_addr)
    store_location = create_scandir(store_location)

    # measure direct beam as a reference
    move_to_sampleposition(experiment, sampleposition, blank=True)
    measure_profile(
        sampleposition, store_location, experiment, mode="blank", duration=seconds
    )
    # sometimes the Total_RBV is zero - not sure why.
    time.sleep(0.2)  # hopefully ensuring we get the transmission
    blank_roi_intensity = epics.caget(f"{experiment.roi_prefix}:Total_RBV")
    # if blank_roi_intensity == 0:
    #     epics.caput(f"{experiment.eiger_prefix}:ROIStat1:EnableCallbacks", 1)
    #     epics.caput(f"{experiment.roi_prefix}:Use", 1)

    #     measure_profile(sampleposition, store_location, experiment,
    #                 mode="blank",
    #                 duration=seconds)
    #     time.sleep(1)  # hopefully ensuring we get the transmission
    #     blank_roi_intensity = max(epics.caget(f"{experiment.roi_prefix}:Total_RBV"), 1)
    move_to_sampleposition(experiment, sampleposition)

    if save_data:
        mode = "saved_scan"
    else:
        mode = "scan"
        epics.caput(f"{experiment.eiger_prefix}:DataSource", "Stream", wait=True)
        # disable filewriter
        epics.caput(f"{experiment.eiger_prefix}:SaveFiles", 0, wait=True)
        epics.caput(f"{experiment.eiger_prefix}:FWEnable", 0, wait=True)

    # write values to where the dashboard can see them
    scan_csv = Path("/home/ws8665-epics/scan-using-epics-ioc/") / "current_scan.csv"
    with open(scan_csv, "w", newline="") as current_file:
        writer = DictWriter(current_file, fieldnames=["point", "value"])
        writer.writerow({"point": motorname, "value": "ratio"})

    # get pv address of transmission / image ratio
    transmission_addr = get_address(experiment, "ratio")
    counter = 0
    source_name = epics.caget(
        f"{experiment.parrot_prefix}:config:source", as_string=True
    )
    epics.caput(f"{source_name}:shutter", 1, wait=True)
    for point in np.linspace(current_pos + scan_start, current_pos + scan_end, npoints):
        actual_pos = move_motor(
            motorname,
            position=point,
            prefix=prefix,
            parrot_prefix=experiment.parrot_prefix,
        )

        store_point = store_location / f"scan_{counter}"
        counter += 1
        measure_profile(
            sampleposition, store_point, experiment, mode=mode, duration=seconds
        )

        time.sleep(0.2)  # hopefully ensuring we get the transmission
        # corresponding to the latest file
        transmission = (
            epics.caget(f"{experiment.roi_prefix}:Total_RBV") / blank_roi_intensity
        )
        # transmission = epics.caget(transmission_addr)
        with open(scan_csv, "a", newline="") as current_file:
            writer = DictWriter(current_file, fieldnames=["point", "value"])
            writer.writerow({"point": actual_pos, "value": transmission})

    status_message = epics.caget(
        f"{experiment.eiger_prefix}:StatusMessage_RBV", as_string=True
    )
    while status_message != "Ready":
        time.sleep(0.2)
        status_message = epics.caget(
            f"{experiment.eiger_prefix}:StatusMessage_RBV", as_string=True
        )

    epics.caput(f"{source_name}:shutter", 0, wait=True)
    # move back to initial position
    move_motor(
        motorname,
        position=current_pos,
        prefix=prefix,
        parrot_prefix=experiment.parrot_prefix,
    )
    # copy scan data to directory
    copyfile(scan_csv, store_location / "scan_data.csv")

    if not save_data:
        # reenable filewriter
        epics.caput(f"{experiment.eiger_prefix}:SaveFiles", 1, wait=True)
        epics.caput(f"{experiment.eiger_prefix}:FWEnable", 1, wait=True)
        epics.caput(f"{experiment.eiger_prefix}:DataSource", "FileWriter", wait=True)
        time.sleep(1)  # to ensure it is actually updated
    return 0
