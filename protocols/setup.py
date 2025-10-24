# this code gets run at the start of every script (not at the start of every entry, but the whole script)
# use this code to check PVs, generators, etc. 
import logging
logger = logging.getLogger("measurement")
logger.setLevel(logging.INFO)
from pathlib import Path
from epics import caget, caput
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
    # 'mc0:zheavy',
    # 'mc0:yawgi',
    # 'mc0:rollgi',
    # 'mc0:pitchgi',
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
    # 'source_cu:shutter',  # uncomment once the source is repaired
    'source_mo:shutter',
    'detector_eiger:DetectorState',  # detector control
    'pressure_gauge:pressure',  # chamber pressure sensor
    'portenta:t0', 'portenta:t1',  # temperature sensors
    'pa0:sample:proposal',  # metadata server aka parrot
    'image:ratio',  # image analysis ioc
]

# check that the PVs are reachable before we execute a script:
for pv in required_pvs:
    value = caget(pv)
    if value is None:
        raise ConnectionError(f"PV '{pv}' is not reachable or has no value.")

experiment = ExperimentVariables(required_pvs, data_dir = Path("/home/ws8665-epics/data/"))

# ensure motor positions are at least checked at the beginning of a measurement
caput("pa0:config:config_id", 999)
caput("pa0:exp:progress:measurements_completed", 0)
