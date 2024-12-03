# 20241201_standard_configurations.py

from epics import caput, caget
import logbook2mouse.measure_config as measure
import logbook2mouse.file_management as filemanagement

# Required additional parameters for this protocol, these need to be present in the logbook entry
required_params = ['temperature_setpoint']


# Example of setting some EPICS Process Variables (PVs)
caput('SAMPLE:POSITION:X', entry.positionx)
caput('SAMPLE:POSITION:Y', entry.positiony)
caput('SAMPLE:POSITION:Z', entry.positionz)

# Example of setting additional parameters
temperature = entry.additional_parameters.get('temperature_setpoint', None)
if temperature is not None:
    caput('SAMPLE:TEMP:SETPOINT', temperature)

# Verifying if the values were set correctly
current_x = caget('SAMPLE:POSITION:X')
current_y = caget('SAMPLE:POSITION:Y')
current_z = caget('SAMPLE:POSITION:Z')

print(f"Current sample position: X={current_x}, Y={current_y}, Z={current_z}")

# Simulate starting the measurement
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")