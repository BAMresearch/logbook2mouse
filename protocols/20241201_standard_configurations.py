# 20241201_standard_configurations.py

from epics import caget, caput
from logbook2mouse.measure_config import move_motor, measure_at_config
import logbook2mouse.file_management as filemanagement

logging.info(f'Starting entry for logbook row {entry.row_index}, sampleID: {entry.sampleid}.')

# Required additional parameters for this protocol, these need to be present in the logbook entry
required_params = ['temperature_setpoint']

# Configurations to measure
if "configuration" in entry.additional_parameters.keys():
    configuration = entry.additional_parameters['configuration']
# else:  # specify configuration manually here

# Example of setting some sample stage positions
current_y = move_motor('ysam', entry.samplepositions["ysam"])
current_z = move_motor('zsam', entry.samplepositions["zsam"])

# Example of setting additional parameters
temperature = entry.additional_parameters.get('temperature_setpoint', None)
if temperature is not None:
    # to do: use actual address of temperature controller
    caput('SAMPLE:TEMP:SETPOINT', temperature)

# Verifying if the values were set correctly
current_x = 0  # caget('SAMPLE:POSITION:X') - not available
current_y = caget('mc0:ysam')
current_z = caget('mc0:zsam')

print(f"Current sample position: X={current_x}, Y={current_y}, Z={current_z}")

# Simulate starting the measurement
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")

measure_at_config(config_no = configuration,
                  entry = entry,
                  required_pvs = required_pvs,
                  dEiger_connection = eiger,
                  duration=60,  # default: 600
                  )
