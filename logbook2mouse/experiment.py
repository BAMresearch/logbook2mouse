import attrs
from typing import List
from pathlib import Path
from time import sleep
import epics
from logbook2mouse.detector import detector_wait_for_pv

@attrs.define
class ExperimentVariables:
    required_pvs: List[str]
    eiger_prefix: str = "eiger:cam1"
    parrot_prefix: str = "pa0"
    image_processing_prefix: str = "image"
    data_dir: Path = Path("~/data/")

    def __attrs_post_init__(self):
        detector_wait_for_pv("Restart", self)
        for i in range(2):
            detector_wait_for_pv("Initialize", self)
        epics.caput(f"{self.eiger_prefix}:SaveFiles", 1)
        epics.caput(f"{self.eiger_prefix}:FWEnable", 1)
        epics.caput(f"{self.eiger_prefix}:FWAutoRemove", 1)
        epics.caput(f"{self.eiger_prefix}:FWNamePattern", "eiger_$id")
        epics.caput(f"{self.eiger_prefix}:FWNImagesPerFile", 60)
        epics.caput(f"{self.eiger_prefix}:FilePath", "/tmp/current/")
        epics.caput(f"{self.eiger_prefix}:FilePerms", 422)
        epics.caput(f"{self.eiger_prefix}:SizeX", 1030)
        epics.caput(f"{self.eiger_prefix}:SizeY", 1065)
        epics.caput(f"{self.eiger_prefix}:TriggerMode", 0)  # internal serial
        epics.caput(f"{self.eiger_prefix}:ImageMode", 2)  # continuous

        
        
        
def get_address(experiment, motorname):
    """Retrieve the pv address for a given motor name

    Motor names are checked against the end of the strings 
    in experiment.required_pvs.
    """
    
    for motor_address in experiment.required_pvs:
        if motor_address.endswith(motorname):
            return motor_address
