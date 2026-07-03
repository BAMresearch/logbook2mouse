import attrs
from typing import List
from pathlib import Path
from time import sleep
import epics


def detector_wait_for_pv(pv, experiment, value=True, reply="Done"):
    epics.caput(f"{experiment.eiger_prefix}:{pv}", value)
    sleep(0.1)
    restart_pv = epics.caget(f"{experiment.eiger_prefix}:{pv}", as_string=True)
    while restart_pv != reply:
        sleep(1)
        restart_pv = epics.caget(f"{experiment.eiger_prefix}:{pv}", as_string=True)
    return 1


def detector_wait_for_status(pv, experiment, value=True, status="Done"):
    epics.caput(f"{experiment.eiger_prefix}:{pv}", value)
    sleep(0.1)
    status_pv = epics.caget(
        f"{experiment.eiger_prefix}:StatusMessage_RBV", as_string=True
    )
    while status_pv != reply:
        sleep(1)
        status_pv = epics.caget(
            f"{experiment.eiger_prefix}:StatusMessage_RBV", as_string=True
        )
    return 1


@attrs.define
class ExperimentVariables:
    required_pvs: List[str]
    eiger_prefix: str = "eiger:cam1"
    parrot_prefix: str = "pa0"
    image_processing_prefix: str = "image"
    roi_prefix: str = "eiger:ROIStat1:1"
    data_dir: Path = Path("~/data/")

    def __attrs_post_init__(self):
        detector_wait_for_pv("Restart", self)
        for i in range(2):
            detector_wait_for_pv("Initialize", self)
        epics.caput(f"{self.eiger_prefix}:FWClear", 1, wait=True)
        epics.caput(f"{self.eiger_prefix}:SaveFiles", 1, wait=True)
        epics.caput(f"{self.eiger_prefix}:FWEnable", 1, wait=True)
        epics.caput(f"{self.eiger_prefix}:FWAutoRemove", 1, wait=True)
        epics.caput(f"{self.eiger_prefix}:FWNamePattern", "eiger_$id", wait=True)
        epics.caput(f"{self.eiger_prefix}:FWNImagesPerFile", 60, wait=True)
        epics.caput(f"{self.eiger_prefix}:FilePath", "/tmp/current/", wait=True)
        epics.caput(f"{self.eiger_prefix}:FilePerms", 422, wait=True)
        epics.caput(f"{self.eiger_prefix}:SizeX", 1030, wait=True)
        epics.caput(f"{self.eiger_prefix}:SizeY", 1065, wait=True)
        epics.caput(f"{self.eiger_prefix}:TriggerMode", 0, wait=True)  # internal serial
        epics.caput(f"{self.eiger_prefix}:ImageMode", 2, wait=True)  # continuous\
        epics.caput(f"{self.eiger_prefix}:AcquireTime", 10, wait=True)
        epics.caput(f"{self.eiger_prefix}:AcquirePeriod", 10, wait=True)
        epics.caput(f"{self.eiger_prefix}:FlatfieldApplied", False, wait=True)
        # additional streaming and ROI capabilities
        epics.caput(f"{self.eiger_prefix}:StreamEnable", 1, wait=True)
        detector_prefix = self.eiger_prefix.split(":")[0]
        epics.caput(f"{detector_prefix}:ROIStat1:EnableCallbacks", 1, wait=True)
        epics.caput(f"{detector_prefix}:ROIStat1:1:Use", 1, wait=True)
        epics.caput(f"{detector_prefix}:ROIStat1:1:MinX", 480, wait=True)
        epics.caput(f"{detector_prefix}:ROIStat1:1:SizeX", 40, wait=True)
        epics.caput(f"{detector_prefix}:ROIStat1:1:MinY", 985, wait=True)
        epics.caput(f"{detector_prefix}:ROIStat1:1:SizeY", 50, wait=True)


def get_address(experiment, motorname):
    """Retrieve the pv address for a given motor name

    Motor names are checked against the end of the strings
    in experiment.required_pvs.
    """

    for motor_address in experiment.required_pvs:
        if motor_address.endswith(motorname):
            return motor_address
