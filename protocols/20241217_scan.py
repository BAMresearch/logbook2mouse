# 20241217_scan.py

from logbook2mouse.scan import scan, move_to_sampleposition

logging.info(f'Starting entry for logbook row {entry.row_index}, sampleID: {entry.sampleid}.')

# Configurations to measure
if "configuration" in entry.additional_parameters.keys():
    configuration = entry.additional_parameters['configuration']
# else:  # specify configuration manually here

# Simulate starting the measurement
print(f"Starting measurement for sample {entry.proposal}-{entry.sampleid} in configuration {configuration}.")

# blank and transmission measurements are included
move_to_sampleposition(experiment, entry)
scan("ysam", -3, 3, 11, 1, experiment, entry, store_location = Path("/tmp/scan"))
