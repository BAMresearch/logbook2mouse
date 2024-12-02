# this code gets run at the start of every script (not at the start of every entry, but the whole script)
# use this code to check PVs, generators, etc. 
import logging
from epics import caget

logging.info('Starting entry for logbook roe {entry.row_index}, sampleID: {entry.sampleid}.')

# Required Process Variables (PVs) for this protocol. These will be validated before execution.
required_pvs = [
    'mc0:ysam',
    'mx0:zsam',
    'ims:detx',
    'ims:dety',
    'ims:detz',
    'ims:s1bot',
    'ims:s1top',
    'ims:s1hl',
    'ims:s1hr',
    'ims:s2bot',
    'ims:s2top',
    'ims:s2hl',
    'ims:s2hr',
    'ims:s3bot',
    'ims:s3top',
    'ims:s3hl',
    'ims:s3hr',
]

# check that the PVs are reachable before we execute a script:
for pv in required_pvs:
    value = caget(pv)
    if value is None:
        raise ConnectionError(f"PV '{pv}' is not reachable or has no value.")
    
# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# 20241201_standard_configurations.py

from epics import caput, caget

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
print(f"Starting measurement for sample {entry.sampleid} with temperature set to {temperature} degrees.")# in this script, put things that are to be run at the very end, 
# such as disabling temperature controllers, closing shutters, moving detector to detx=400, etc.

from epics import caput, caget
import logging

logging.info('Measurement entry complete for sample {entry.sampleid}.')
