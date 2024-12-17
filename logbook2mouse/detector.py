import os
import sys
import time
from pathlib import Path
from shutil import move, copyfile
from time import sleep
import hdf5plugin
import h5py
import logging
import logbook2mouse.file_management as filemanagement
import logbook2mouse.metadata as meta
import epics

def measurement(experiment, duration: float = 1.0, store_location: Path = Path(".")):
    epics.caput(f"{experiment.eiger_prefix}:CountTime", duration)
    epics.caput(f"{experiment.eiger_prefix}:Configure", True)
    det_status = epics.caget(f"{experiment.eiger_prefix}:DetectorState")
    while det_status != "idle":
        sleep(.1)
        det_status = epics.caget(f"{experiment.eiger_prefix}:DetectorState")
    # prepare approximate countdown
    countdown_pv = f"{experiment.eiger_prefix}:SecondsRemaining"
    # trigger once idle
    epics.caput(f"{experiment.eiger_prefix}:Trigger", True)
    sleep(.1)
    is_triggered = epics.caget(f"{experiment.eiger_prefix}:Trigger_RBV")
    while is_triggered:
        # wait for trigger flag to go off
        sleep(1)
        is_triggered = epics.caget(f"{experiment.eiger_prefix}:Trigger_RBV")
        print(f"\r{epics.caget(countdown_pv)} seconds remaining for the current exposure  ",
              end='\r', flush=True)

    # get current snapshot of chamber pressure, temperature, ...
    # this is recorded at the end of the measurement time
    meta.environment2parrot(experiment)
    # write metadata file
    meta.write_meta_nxs(store_location)

    frompath = Path("/tmp/current/")
    pattern = epics.caget(f"{experiment.eiger_prefix}:OutputFilePrefix")
    os.makedirs(store_location, exist_ok = True)
    for fpath in frompath.glob(f"{pattern}*.h5"):
        move(fpath, store_location)

