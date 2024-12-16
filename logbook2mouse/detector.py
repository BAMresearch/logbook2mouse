import os
import sys
import time
from pathlib import Path
from shutil import move, copyfile
from time import sleep
from threading import Thread
import hdf5plugin
import h5py
import numpy as np
import logging
from attrs import define, field, validators
from DEigerClient import DEigerClient
import logbook2mouse.file_management as filemanagement
import logbook2mouse.metadata as meta
import epics

@define
class DEiger:
    dcu_ip: str = field(
        default="172.17.1.2",
        validator=validators.optional(validators.instance_of(str)),
    )

    frame_time = 10

    nimages_per_file = 60

    client: DEigerClient = field(init=False)

    def __attrs_post_init__(self):
        self.client = DEigerClient(self.dcu_ip)

    def empty_data_store(self):
        self.client.sendFileWriterCommand("clear")
        # writing of files needs to be enabled again after
        self.client.setFileWriterConfig("mode", "enabled")

    def set_defaults(self):
        logging.info("taking back detector control from spec")
        self.client.sendSystemCommand("restart")
        self.client.sendDetectorCommand("initialize")
        self.client.setDetectorConfig("photon_energy", 8050)
        self.client.setDetectorConfig("count_time", 1)
        self.client.setDetectorConfig("frame_time", 10.0)
        self.empty_data_store()
        self.client.setFileWriterConfig("name_pattern", "eiger_$id")
        self.client.setDetectorConfig("compression", "bslz4")


def send_detector_command(DEiger, command, **kwargs):
    response = DEiger.sendDetectorCommand(command)
    success = len(response.keys())
    if success:
        return 0


def countdown(duration):
    for i in range(duration,0,-1):
        print(f"\r{i} seconds remaining for the current exposure  ",
              end='\r', flush=True)
        time.sleep(1)
    return 0

def exposition(DEiger, duration=1):
    def send_trigger():
        send_detector_command(DEiger, "trigger")

    countdown_fcn = lambda: countdown(duration)

    print("Arming detector..." + " "*30, end="\r", flush=True)
    send_detector_command(DEiger, "arm")
    thread_detector = Thread(target=send_trigger)
    thread_counter = Thread(target=countdown_fcn)
    thread_detector.start()
    thread_counter.start()
    while thread_detector.is_alive():
        sleep(.2)
    print("Disarming detector..." + " "*30, end="\r", flush=True)
    send_detector_command(DEiger, "disarm")
    return "exposition done"


def measurement_done(DEiger, duration=1, n_files=1):
    data_before = DEiger.client.fileWriterFiles()
    logging.info(f"Expected number of files: {n_files}")
    exposition_complete = exposition(DEiger.client, duration=duration)
    data_current = DEiger.client.fileWriterFiles()
    # await asyncio.sleep(duration)
    while len(data_current) < len(data_before) + n_files:
        sleep(0.2)
        data_current = DEiger.client.fileWriterFiles()
    return "data uploaded"


def measurement(experiment, duration: float = 1.0, store_location: Path = Path(".")):
    epics.caput(f"{experiment.eiger_prefix}:CountTime", duration)
    det_state = epics.caget(f"{experiment.eiger_prefix}:DetectorState")
    print(det_state)
    while det_state != "idle":
        sleep(.1)
        det_state = epics.caget(f"{experiment.eiger_prefix}:DetectorState")
    # trigger once idle
    epics.caput(f"{experiment.eiger_prefix}:Trigger", True)
    sleep(.1)
    is_triggered = epics.caget(f"{experiment.eiger_prefix}:Trigger_RBV")
    while is_triggered:
        # wait for trigger flag to go off
        sleep(.1)
        is_triggered = epics.caget(f"{experiment.eiger_prefix}:Trigger_RBV")

    frompath = Path("/tmp/current/")
    pattern = epics.caget(f"{experiment.eiger_prefix}:OutputFilePrefix")
    os.makedirs(store_location, exist_ok = True)
    for fpath in frompath.glob(f"{pattern}*.h5"):
        move(fpath, store_location)
    print("measurement done")


def measurement_roi(
    DEiger,
    roi=(slice(400, 600), slice(400, 600)),
    duration: int = 1,
    store_location: Path = Path("."),
):
    data = measurement(DEiger, duration=duration, store_location=store_location)
    result = data[roi]
    logging.info(f"measurement summary (max in ROI): {np.max(result)} cts")
    return result
