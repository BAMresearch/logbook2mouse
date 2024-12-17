# this code gets run at the start of every script (not at the start of every entry, but the whole script)
# use this code to check PVs, generators, etc. 
import logging
logger = logging.getLogger("measurement")
logger.setLevel(logging.INFO)
import epics
from pandas import Timestamp
import logbook2mouse.detector as detector
from logbook2mouse.logbook_reader import Logbook2MouseEntry
from logbook2mouse.project_reader import ProjectInfo, Sample, SampleComponent
from periodictable import formula
from logbook2mouse.experiment import ExperimentVariables


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

epics.caput("ims:detx", 400)
epics.caput("portenta:do7", 0)
epics.caput("portenta:do6", 1)
