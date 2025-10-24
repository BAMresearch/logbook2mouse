# 20250109_alignment.py

from logbook2mouse.measure_config import (
    move_motor, move_to_sampleposition, moveto_config,
    measure_at_config)
from logbook2mouse.file_management import work_directory
from logbook2mouse.scan import scan
import mouse_alignment_routines.alignment as align
import mouse_alignment_routines.transmission_models as transmission_models
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
    moveto_config(experiment,
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
scan_dir = Path(work_directory(entry, experiment)) / f"{ymd}_{entry.batchnum}_{0}" / "scans"
os.makedirs(scan_dir / "scan_0", exist_ok=True)

move_to_sampleposition(experiment, entry.sampleposition)
# does this also set the sample name? Don't think so

# initial value for vertical position
zheavymodel = transmission_models.ZheavyModel(center=entry.sampleposition["zheavy"])
pitchmodel = transmission_models.PitchModel()
res, zheavymodel = align.zheavy_center(experiment, (-1.0, 1.0), 31, entry.sampleposition,
                                       zheavymodel,
                                       scan_dir)
start_z = res["center"]
beam_sigma = res["sigma"]
entry.sampleposition["zheavy"] = start_z
zheavymodel.parameters["center"].set(value = start_z)
zheavymodel.parameters["sigma"].set(value = beam_sigma)
print("initial zheavy center:", start_z)
move_to_sampleposition(experiment, entry.sampleposition)

# center horizontal wafer position (with blocked beam)
entry.sampleposition["zheavy"] = start_z + 0.5
move_to_sampleposition(experiment, entry.sampleposition)
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

sampleposition, zheavymodel, pitchmodel = align.pitch_align(experiment,
                                                            zheavymodel, pitchmodel, 
                                                            halfsample=0.5*samplelength,
                                                            sampleposition=entry.sampleposition,
                                                            store_location=scan_dir)
entry.sampleposition = sampleposition
move_to_sampleposition(experiment, entry.sampleposition)

roll_offset = 3 # mm - otherwise it won't work with GI4
roll_center, new_z = align.roll_align(experiment, y_center, beam_sigma, roll_offset,
                                      centerofrotation = 37.3141,
                                      sampleposition=entry.sampleposition,
                                      zheavymodel=zheavymodel,
                                      store_location=scan_dir)
entry.sampleposition["rollgi"] = roll_center
move_to_sampleposition(experiment, entry.sampleposition)
res, zheavymodel = align.zheavy_center(experiment, (-1.0, 1.0), 31,
                                 entry.sampleposition, zheavymodel, scan_dir)
entry.sampleposition["zheavy"] = res["center"]

# test roll alignment - transmission should be a constant 0.5 ideally
move_to_sampleposition(experiment, entry.sampleposition)
scan("ysam", -1*roll_offset,
     roll_offset, 31, 1, experiment, entry.sampleposition,
     store_location=scan_dir)

sampleposition, zheavymodel, pitchmodel = align.pitch_align(experiment,
                                                            zheavymodel, pitchmodel, 
                                                            halfsample=0.5*samplelength,
                                                            sampleposition=entry.sampleposition,
                                                            store_location=scan_dir)
entry.sampleposition = sampleposition
move_to_sampleposition(experiment, entry.sampleposition)

logging.info(f"horizontal position pitch: {entry.sampleposition['pitchgi']}°")
logging.info(f"sample surface, vertical position: {entry.sampleposition['zheavy']} mm")
move_to_sampleposition(experiment, entry.sampleposition)

# measure once at this position - this should make the first measurement of each sample the reference
if configuration is not None:
    measure_at_config(configuration,
                      entry,
                      experiment,
                      repetitions=1,
                      duration=60,
                      )
