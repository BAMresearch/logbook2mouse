import attrs
from typing import List

import epics

@attrs.define
class ExperimentVariables:
    required_pvs: List[str]
    eiger_prefix: str = "detector_eiger"
    parrot_prefix: str = "pa0"
    image_processing_prefix: str = "image"

    def __attrs_post_init__(self):
        epics.caput(f"{self.eiger_prefix}:Initialize", True)

def get_address(experiment, motorname):
    """Retrieve the pv address for a given motor name

    Motor names are checked against the end of the strings 
    in experiment.required_pvs.
    """
    
    for motor_address in experiment.required_pvs:
        if motor_address.endswith(motorname):
            return motor_address
