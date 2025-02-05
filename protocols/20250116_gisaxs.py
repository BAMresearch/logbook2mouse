# 20250116_reflectivity.py

from logbook2mouse.scan import scan
from logbook2mouse.measure_config import (
    move_motor, move_motor_fromconfig, moveto_config,
    measure_at_config)
from logbook2mouse.file_management import work_directory, scan_counter_next
from logbook2mouse.experiment import get_address
from pathlib import Path
import epics

def get_float_parameter(entry, keyword, default):
    value = entry.additional_parameters.get(keyword, default)
    if type(value) == str:
        value = float(value)
    return value

configuration = entry.additional_parameters.get('configuration', None)
if configuration is not None:
    moveto_config(experiment.required_pvs,
                  config_no = configuration)


incident_angle = get_float_parameter(entry, 'incident_angle', 0.21)
repetitions = entry.additional_parameters.get('repetitions', None)
if repetitions is not None:
    repetitions = int(float(repetitions))

ymd = entry.date.strftime("%Y%m%d")
wd = Path(work_directory(entry))
aligned_data =  wd / f"{ymd}_{entry.batchnum}_{1}"
scan_dir = wd / f"{ymd}_{entry.batchnum}_{scan_counter_next(0, wd, entry)}"

# move to aligned position
for motor in ["ysam", "zheavy", "yawgi", "rollgi", "pitchgi"]:
    motorname, motorpos = move_motor_fromconfig(motor, imcrawfile=aligned_data/"im_craw.nxs",
                                                prefix=get_address(experiment, motor).split(":")[0]
                                                )
    entry.sampleposition[motor] = motorpos

incident_angle_zero = epics.caget(get_address(experiment, "pitchgi"))

# move to requested angle and measure
pitch = float(incident_angle_zero) - float(incident_angle)  # pitchgi axis is reversed
move_motor("pitchgi", pitch)
entry.sampleposition["pitchgi"] = float(pitch)

measure_at_config(
    config_no = configuration,
    entry = entry,
    experiment = experiment,
    repetitions = int(repetitions),
    duration = 600,
)


