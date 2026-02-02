from logbook2mouse.measure_config import (
    move_motor,
    measure_profile,
    move_to_sampleposition,
)
from logbook2mouse.experiment import get_address
from logbook2mouse.file_management import scan_counter_simple
import logging
import epics
from csv import DictWriter
from pathlib import Path
import numpy as np
import os, time


def create_scandir(work_dir):
    """
    Create a subdirectory in work_dir with the next
    free number, scan_{next number}.
    """

    os.makedirs(work_dir, exist_ok=True)
    new_dir_no = scan_counter_simple(0, work_dir)
    scandir = work_dir / f"scan_{new_dir_no}"
    os.makedirs(scandir, exist_ok=True)
    return scandir


def scan_point_directory(work_dir):
    """
    Construct a subdirectory name for scan datapoints
    from the work_dir the scan is located in.

    work_dir typically ends in ymd_batch_repetition.

    returns a string of type format ymd_batch_ if work_dir is of
    the appropriate format, otherwise a dummy string.
    """

    subdir_parts = work_dir.name.split("_")
    ymd = work_dir.parent.name
    if len(subdir_parts) == 3 and subdir_parts[0] == ymd:
        # this directory follows the regular pattern
        scan_point_format = f"{ymd}_{subdir_parts[1]}_"
    else:
        logger = logging.getLogger("measurement")
        logger.info(
            f"Scan directory does not follow the pattern necessary for post-processing."
        )
        scan_point_format = f"{time.strftime('%Y%m%d', time.localtime())}_0_"
    return scan_point_format


def scan(
    motorname,
    scan_start,
    scan_end,
    npoints,
    seconds,
    experiment,
    sampleposition,
    store_location,
):
    """Scan and record transmission relative to the current position."""
    motor_addr = get_address(experiment, motorname)
    prefix = motor_addr.rstrip(f":{motorname}")
    current_pos = epics.caget(motor_addr)
    store_location = create_scandir(store_location)
    scan_point_format = scan_point_directory(work_dir)

    # measure direct beam as a reference
    move_to_sampleposition(experiment, sampleposition, blank=True)
    measure_profile(
        sampleposition, store_location, experiment, mode="blank", duration=seconds
    )
    move_to_sampleposition(experiment, sampleposition)

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

        store_point = store_location / f"{scan_point_format}{counter}"
        counter += 1
        measure_profile(
            sampleposition, store_point, experiment, mode="scan", duration=seconds
        )

        time.sleep(0.2)  # hopefully ensuring we get the transmission
        # corresponding to the latest file
        transmission = epics.caget(transmission_addr)
        with open(scan_csv, "a", newline="") as current_file:
            writer = DictWriter(current_file, fieldnames=["point", "value"])
            writer.writerow({"point": actual_pos, "value": transmission})

    epics.caput(f"{source_name}:shutter", 0, wait=True)
    # move back to initial position
    move_motor(
        motorname,
        position=current_pos,
        prefix=prefix,
        parrot_prefix=experiment.parrot_prefix,
    )
    return 0
