from logbook2mouse.measure_config import move_motor, measure_profile
from logbook2mouse.experiment import get_address
import epics
from csv import DictWriter
from pathlib import Path

def scan(motorname, scan_start, scan_end, npoints,
         seconds,
         experiment, entry, store_location):
    """Scan and record transmission relative to the current position."""
    motor_addr = get_address(experiment, motorname)
    prefix = motor_addr.rstrip(f":{motorname}")
    current_pos = epics.caget(motor_addr)

    # measure direct beam as a reference
    measure_profile(entry, store_location, experiment,
                    mode="blank",
                    duration=seconds)

    # write values to where the dashboard can see them
    scan_csv = Path("/home/ws8665-epics/scan-using-epics-ioc/") / "current_scan.csv"
    with open(scan_csv, "w", newline = "") as current_file:
        writer = DictWriter(current_file,
                            fieldnames = ["point", "value"])
        writer.writerow({"point": motorname, "value": "ratio"})

    # get pv address of transmission / image ratio
    transmission_addr = get_address(experiment, "ratio")

    for point in np.linspace(current_pos + scan_start,
                             current_pos + scan_end,
                             npoints):

        move_motor(motorname, position = point, prefix = prefix,
                   parrot_prefix = experiment.parrot_prefix)

        measure_profile(entry, store_location, experiment,
                        mode="scan",
                        duration=seconds)

        transmission = epics.caget(transmission_addr)
        with open(scan_csv, "a", newline = "") as current_file:
            writer = DictWriter(current_file,
                                fieldnames = ["point", "value"])
            writer.writerow({"point": point, "value": transmission})

    # move back to initial position
    move_motor(motorname, position = current_pos, prefix = prefix,
               parrot_prefix = experiment.parrot_prefix)
    return 0
