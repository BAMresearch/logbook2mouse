# put startup commands here, check power levels of generator, vacuum levels, etc.
logging.info('Starting entry for logbook roe 3, sampleID: 1.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 1.)
logging.info('Starting entry for logbook roe 4, sampleID: 1.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 1.)
logging.info('Starting entry for logbook roe 5, sampleID: 2.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 2.)
logging.info('Starting entry for logbook roe 6, sampleID: 4.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 4.)
logging.info('Starting entry for logbook roe 7, sampleID: 4.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 4.)
logging.info('Starting entry for logbook roe 8, sampleID: 8.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 8.)
logging.info('Starting entry for logbook roe 9, sampleID: 9.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 9.)
logging.info('Starting entry for logbook roe 10, sampleID: 10.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 10.)
logging.info('Starting entry for logbook roe 11, sampleID: 11.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 11.)
logging.info('Starting entry for logbook roe 12, sampleID: 12.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 12.)
logging.info('Starting entry for logbook roe 13, sampleID: 13.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 13.)
logging.info('Starting entry for logbook roe 14, sampleID: 14.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 14.)
logging.info('Starting entry for logbook roe 16, sampleID: 1.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 1.)
logging.info('Starting entry for logbook roe 17, sampleID: 1.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 1.)
logging.info('Starting entry for logbook roe 18, sampleID: 2.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 2.)
logging.info('Starting entry for logbook roe 19, sampleID: 4.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 4.)
logging.info('Starting entry for logbook roe 20, sampleID: 4.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 4.)
logging.info('Starting entry for logbook roe 21, sampleID: 8.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 8.)
logging.info('Starting entry for logbook roe 22, sampleID: 9.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 9.)
logging.info('Starting entry for logbook roe 23, sampleID: 10.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 10.)
logging.info('Starting entry for logbook roe 24, sampleID: 11.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 11.)
logging.info('Starting entry for logbook roe 25, sampleID: 12.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 12.)
logging.info('Starting entry for logbook roe 26, sampleID: 13.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 13.)
logging.info('Starting entry for logbook roe 27, sampleID: 14.
# 20241201_standard_configurations.py



from epics import caput, caget



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
logging.info('Measurement entry complete for sample 14.)
logging.info('end of measurement script.')