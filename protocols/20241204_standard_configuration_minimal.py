# 20241204_standard_configuration_minimal.py

from logbook2mouse.measure_config import measure_at_config

logging.info(f'Starting entry for logbook row {entry.row_index}, sampleID: {entry.sampleid}.')

# Configurations to measure
if "configuration" in entry.additional_parameters.keys():
    configuration = entry.additional_parameters['configuration']
# else:  # specify configuration manually here

# Simulate starting the measurement
print(f"Starting measurement for sample {entry.proposal}-{entry.sampleid} in configuration {configuration}.")

# blank and transmission measurements are included
measure_at_config(config_no = configuration,
                  entry = entry,
                  experiment = experiment,
                  duration=10,  # default: 600
                  # repetitions=16  # default: determined by config number
                  )
