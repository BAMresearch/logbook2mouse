# 20241201_standard_configurations.py

from epics import caput, caget
import logbook2mouse.measure_config as measure
import logbook2mouse.file_management as filemanagement

# Required additional parameters for this protocol, these need to be present in the logbook entry
required_params = ['temperature_setpoint']

# Configurations to measure
configurations = [127]

# Example of setting some EPICS Process Variables (PVs)
# caput('SAMPLE:POSITION:X', entry.positionx)
caput('mc0:ysam', entry.positiony)
caput('mc0:zsam', entry.positionz)

# Example of setting additional parameters
temperature = entry.additional_parameters.get('temperature_setpoint', None)
if temperature is not None:
    caput('SAMPLE:TEMP:SETPOINT', temperature)

# Verifying if the values were set correctly
current_x = 0  # caget('SAMPLE:POSITION:X')
current_y = caget('mc0:ysam')
current_z = caget('mc0:zsam')

print(f"Current sample position: X={current_x}, Y={current_y}, Z={current_z}")

# Simulate starting the measurement
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")

store_location = filemanagement.work_directory(entry.date)
for config in configurations:
    measure.measure_at_config(config_no = config,
                              entry = entry,
                              required_pvs = required_pvs,
                              dEiger_connection = eiger
                              )
