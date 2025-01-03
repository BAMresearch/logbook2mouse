# this code gets run at the start of every script (not at the start of every entry, but the whole script)
# use this code to check PVs, generators, etc. 
import logging
logger = logging.getLogger("measurement")
logger.setLevel(logging.INFO)
from epics import caget
from pandas import Timestamp
import logbook2mouse.detector as detector
from logbook2mouse.logbook_reader import Logbook2MouseEntry
from logbook2mouse.project_reader import ProjectInfo, Sample, SampleComponent
from periodictable import formula
from logbook2mouse.experiment import ExperimentVariables


# Required Process Variables (PVs) for this protocol. These will be validated before execution.
required_pvs = [
    'mc0:ysam',
    'mc0:zsam',
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
    'ims:bsr',
    'ims:bsz',
    'source_cu:shutter',
    'detector_eiger:DetectorState',
    'pressure_gauge:pressure',
    'pa0:sample:proposal',
    'image:ratio',
]

# check that the PVs are reachable before we execute a script:
for pv in required_pvs:
    value = caget(pv)
    if value is None:
        raise ConnectionError(f"PV '{pv}' is not reachable or has no value.")

experiment = ExperimentVariables(required_pvs)
