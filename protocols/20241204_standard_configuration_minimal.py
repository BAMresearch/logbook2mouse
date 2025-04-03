# 20241204_standard_configuration_minimal.py

from logbook2mouse.measure_config import measure_at_config

logging.info(f'Starting entry for logbook row {entry.row_index}, sampleID: {entry.sampleid}.')

# Configurations to measure
configuration = int(entry.additional_parameters.get('configuration', 125))
duration = int(float(entry.additional_parameters.get('duration', 600)))
repetitions = entry.additional_parameters.get('repetitions', None)
if repetitions is not None:
    repetitions = int(float(repetitions))
# else:  # specify configuration manually here

# Simulate starting the measurement
print(f"Starting measurement for sample {entry.proposal}-{entry.sampleid} in configuration {configuration}.")

# blank and transmission measurements are included
measure_at_config(config_no = configuration,
                  entry = entry,
                  experiment = experiment,
                  duration=duration,  # default: 600
                  repetitions=repetitions  # default: determined by config number
                  )
