from logbook2mouse.measure_config import move_motor, measure_profile, move_to_sampleposition
from logbook2mouse.experiment import get_address
from logbook2mouse.file_management import scan_counter_simple
import epics
from csv import DictWriter
from pathlib import Path
import numpy as np
import os




def create_scandir(work_dir):
    new_dir_no = scan_counter_simple(0, work_dir)
    scandir = work_dir / f"scan_{new_dir_no}"
    os.makedirs(scandir,
                exist_ok = True)
    return scandir

def scan(motorname, scan_start, scan_end, npoints,
         seconds,
         experiment, sampleposition, store_location):
    """Scan and record transmission relative to the current position."""
    motor_addr = get_address(experiment, motorname)
    prefix = motor_addr.rstrip(f":{motorname}")
    current_pos = epics.caget(motor_addr)
    store_location = create_scandir(store_location)

    # measure direct beam as a reference
    move_to_sampleposition(experiment, sampleposition, blank = True)
    measure_profile(sampleposition, store_location, experiment,
                    mode="blank",
                    duration=seconds)
    move_to_sampleposition(experiment, sampleposition)

    # write values to where the dashboard can see them
    scan_csv = Path("/home/ws8665-epics/scan-using-epics-ioc/") / "current_scan.csv"
    with open(scan_csv, "w", newline = "") as current_file:
        writer = DictWriter(current_file,
                            fieldnames = ["point", "value"])
        writer.writerow({"point": motorname, "value": "ratio"})

    # get pv address of transmission / image ratio
    transmission_addr = get_address(experiment, "ratio")
    counter = 0
    epics.caput("source_cu:shutter", 1, wait=True)
    for point in np.linspace(current_pos + scan_start,
                             current_pos + scan_end,
                             npoints):

        move_motor(motorname, position = point, prefix = prefix,
                   parrot_prefix = experiment.parrot_prefix)

        store_point = store_location / f"scan_{counter}"
        counter += 1
        measure_profile(sampleposition, store_point, experiment,
                        mode="scan",
                        duration=seconds)

        transmission = epics.caget(transmission_addr)
        with open(scan_csv, "a", newline = "") as current_file:
            writer = DictWriter(current_file,
                                fieldnames = ["point", "value"])
            writer.writerow({"point": point, "value": transmission})

    epics.caput("source_cu:shutter", 0, wait=True)
    # move back to initial position
    move_motor(motorname, position = current_pos, prefix = prefix,
               parrot_prefix = experiment.parrot_prefix)
    return 0
