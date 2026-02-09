import os
import sys
import time
import numpy as np
from pathlib import Path
from shutil import move, copyfile
from time import sleep
import hdf5plugin
import h5py
import logging
import logbook2mouse.file_management as filemanagement
import logbook2mouse.metadata as meta
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
    status_pv = epics.caget(f"{experiment.eiger_prefix}:StatusMessage_RBV", as_string=True)
    while status_pv != status:
        sleep(1)
        status_pv = epics.caget(f"{experiment.eiger_prefix}:StatusMessage_RBV", as_string=True)
    return 1


def measurement(experiment, duration: float = 1.0, store_location: Path = Path(".")):
    # calculate number of images from requested duration and frame time
    frame_time = epics.caget(f"{experiment.eiger_prefix}:AcquirePeriod")
    nimages = np.ceil(duration/frame_time )
    epics.caput(f"{experiment.eiger_prefix}:NumImages", nimages)
    #epics.caput(f"{experiment.eiger_prefix}:Configure", True)
    det_status = epics.caget(f"{experiment.eiger_prefix}:State_RBV", as_string=True)
    while det_status != "idle":
        sleep(.1)
        det_status = epics.caget(f"{experiment.eiger_prefix}:State_RBV", as_string=True)
    # prepare approximate countdown
    # countdown_pv = f"{experiment.eiger_prefix}:SecondsRemaining"
    # trigger once idle
    epics.caput(f"{experiment.eiger_prefix}:Acquire", True)
    sleep(.1)
    is_triggered = epics.caget(f"{experiment.eiger_prefix}:Acquire_RBV", as_string=True)
    remaining_time = duration
    while is_triggered != "Done":
        # wait for trigger flag to go off
        sleep(1)
        remaining_time -= 1
        is_triggered = epics.caget(f"{experiment.eiger_prefix}:Acquire_RBV", as_string=True)
        print(f"\r{remaining_time} seconds remaining for the current exposure  ",
              end='\r', flush=True)

    # get current snapshot of chamber pressure, temperature, ...
    # this is recorded at the end of the measurement time
    meta.environment2parrot(experiment)
    # write metadata file
    meta.write_meta_nxs(store_location)

    frompath = Path("/tmp/current/")
    pattern = epics.caget(f"{experiment.eiger_prefix}:FWNamePattern", as_string=True).split("_")[0]
    os.makedirs(store_location, exist_ok = True)
    for fpath in frompath.glob(f"{pattern}*.h5"):
        move(fpath, store_location)

