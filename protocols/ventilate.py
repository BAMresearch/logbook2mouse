# this code gets run at the start of every script (not at the start of every entry, but the whole script)
# use this code to check PVs, generators, etc. 
import logging
logger = logging.getLogger("measurement")
logger.setLevel(logging.INFO)
import epics
from time import sleep
from pandas import Timestamp
from periodictable import formula
from logbook2mouse.experiment import ExperimentVariables
from logbook2mouse.measure_config import move_motor


# Required Process Variables (PVs) for this protocol. These will be validated before execution.
required_pvs = [
    'ims:detx',
    'pressure_gauge:pressure',
    'portenta:do6',
]

# check that the PVs are reachable before we execute a script:
for pv in required_pvs:
    value = epics.caget(pv)
    if value is None:
        raise ConnectionError(f"PV '{pv}' is not reachable or has no value.")

experiment = ExperimentVariables(required_pvs)

move_motor("detx", 400, prefix = "ims")
epics.caput("portenta:do6", 0)
sleep(1)
epics.caput("portenta:do7", 1)

pressure = epics.caget("pressure_gauge:pressure")
while pressure < 1e3:
    sleep(1)
    pressure = epics.caget("pressure_gauge:pressure")
    print("current pressure:", pressure)

epics.caput("portenta:do7", 0)
