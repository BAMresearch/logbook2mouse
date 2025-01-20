# 20250109_alignment.py

from logbook2mouse.measure_config import (
    move_motor, move_to_sampleposition, moveto_config,
    measure_at_config)
from logbook2mouse.file_management import work_directory
import mouse_alignment_routines.alignment as align
from pathlib import Path
import os

# design needs:
# - have approximate sample length (and width?) somewhere
# - package with functions specific to scan analysis. this has no place in logbook2mouse
# - what modifications from branch 2_multisampleholder are worth keeping?
# - how to store alignment result
#   + just in nxs file? -> need to label this file
#   + create sampleposition dict from nxs file (?)

configuration = entry.additional_parameters.get('configuration', None)
if configuration is not None:
    moveto_config(experiment.required_pvs,
                  config_no = configuration)

def get_float_parameter(entry, keyword, default):
    value = entry.additional_parameters.get(keyword, default)
    if type(value) == str:
        value = float(value)
    return value

samplelength = get_float_parameter(entry, 'samplelength', 30.)
samplewidth = get_float_parameter(entry, 'samplewidth', samplelength)

# define where to save scans
ymd = entry.date.strftime("%Y%m%d")
scan_dir = Path(work_directory(entry)) / f"{ymd}_{entry.batchnum}_{0}" / "scans"
os.makedirs(scan_dir / "scan_0", exist_ok=True)

move_to_sampleposition(experiment, entry.sampleposition)
# does this also set the sample name? Don't think so

# initial value for vertical position
start_z, sigma = align.zheavy_center(experiment, (-1.0, 1.0), 31, entry.sampleposition,
                                     scan_dir)
entry.sampleposition["zheavy"] = start_z
print("initial zheavy center:", start_z)
move_to_sampleposition(experiment, entry.sampleposition)

# center horizontal wafer position (with blocked beam)
entry.sampleposition["zheavy"] = start_z + 0.5
move_motor("zheavy", start_z + 0.5, prefix="mc0")
y_center = align.horizontal_center(experiment,
                                   (-0.5*samplewidth*1.25,
                                    +0.5*samplewidth*1.25), 31,
                                   entry.sampleposition,
                                   scan_dir)
entry.sampleposition["zheavy"] = start_z

# could determine samplewidth here
print("ysam center:", y_center)
entry.sampleposition["ysam"] = y_center
move_to_sampleposition(experiment, entry.sampleposition)

pitch_center, center = align.pitch_align(experiment, start_z=start_z,
                                         start_pitch=0,
                                         sigma_beam=sigma,
                                         halfsample=0.5*samplelength,
                                         sampleposition=entry.sampleposition,
                                         store_location=scan_dir)
entry.sampleposition["zheavy"] = center
move_motor("zheavy", center, prefix="mc0")
entry.sampleposition["pitchgi"] = pitch_center
move_motor("pitchgi", pitch_center, prefix="mc0")

rolloffset = 0.9*halfsample
roll_center = align.roll_align(experiment, y_center, sigma, 0.5*samplewidth*0.75, centerofrotation = 31,
                               sampleposition=entry.sampleposition,
                               store_location=scan_dir)
entry.sampleposition["rollgi"] = roll_center

pitch_center, center = align.pitch_align(experiment, start_z=center,
                                         start_pitch=pitch_center,
                                         sigma_beam=sigma,
                                         halfsample=halfsample,
                                         sampleposition=entry.sampleposition,
                                         store_location=scan_dir)
entry.sampleposition["zheavy"] = center
move_motor("zheavy", center, prefix="mc0")
entry.sampleposition["pitchgi"] = pitch_center
move_motor("pitchgi", pitch_center, prefix="mc0")
logging.info(f"horizontal position pitch: {pitch_center}°")
logging.info(f"sample surface, vertical position: {center} mm")

# measure once at this position - this should make the first measurement of each sample the reference
if configuration is not None:
    measure_at_config(configuration,
                      entry,
                      experiment,
                      repetitions=1,
                      duration=60,
                      )
