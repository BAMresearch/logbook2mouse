# 20250116_reflectivity.py

from logbook2mouse.scan import scan
from logbook2mouse.measure_config import (
    move_motor, move_motor_fromconfig, moveto_config,
    measure_at_config)
from logbook2mouse.file_management import work_directory, scan_counter_next
from logbook2mouse.experiment import get_address
from pathlib import Path
import epics

configuration = entry.additional_parameters.get('configuration', None)
if configuration is not None:
    moveto_config(experiment.required_pvs,
                  config_no = configuration)

ymd = entry.date.strftime("%Y%m%d")
wd = Path(work_directory(entry)) / ymd
aligned_data =  wd / f"{ymd}_{entry.batchnum}_{0}")
scan_dir = wd / f"{ymd}_{entry.batchnum}_{scan_counter_next(0, wd, entry)}"

# move to aligned position
for motor in ["ysam", "zheavy", "yawgi", "rollgi", "pitchgi"]:
    motorname, motorpos = move_motor_fromconfig(motor, imcrawfile=aligned_data/"im_craw.nxs",
                                                prefix=get_address(motor).split(":")[0]
                                                )
    entry.sampleposition[motor] = motorpos

incident_angle_zero = epics.caget(get_address("pitchgi"))


# scan
scan("pitchgi", -0.6, -0.1, 101,
     1, # second
     experiment, entry.sampleposition,
     scan_dir
     )


