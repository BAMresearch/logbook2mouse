import attrs
from typing import List

from logbook2mouse.detector import DEiger

@attrs.define
class ExperimentVariables:
    required_pvs: List[str]
    eiger = DEiger()
    parrot_prefix: str = "pa0"
    image_processing_prefix: str = "image"

    def __attrs_post_init__(self):
        self.eiger.set_defaults()

def get_address(experiment, motorname):
    """Retrieve the pv address for a given motor name

    Motor names are checked against the end of the strings 
    in experiment.required_pvs.
    """
    
    for motor_address in experiment.required_pvs:
        if motor_address.endswith(motorname):
            return motor_address
