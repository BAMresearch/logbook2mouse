import os
import sys
import time
from pathlib import Path
from shutil import move, copyfile
from time import sleep
import hdf5plugin
import h5py
import numpy as np
import logging
from attrs import define, field, validators
from .deigerclient import DEigerClient
import logbook2mouse.file_management as filemanagement
import logbook2mouse.metadata as meta

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
        self.client.setDetectorConfig("photon_energy", 8000)
        self.client.setDetectorConfig("count_time", 1)
        self.client.setDetectorConfig("frame_time", 1.1)
        self.empty_data_store()
        self.client.setFileWriterConfig("name_pattern", "eiger_$id")
        self.client.setDetectorConfig("compression", "bslz4")


def send_detector_command(DEiger, command, **kwargs):
    if command == "trigger":
        if "duration" in kwargs.keys():
            response = DEiger.sendDetectorCommand(command, timeout=kwargs["timeout"])
        else:
            response = DEiger.sendDetectorCommand(command)
    else:
        response = DEiger.sendDetectorCommand(command)
    success = len(response.keys())
    if success:
        return 0


def exposition(DEiger, duration=1):
    print("Arming detector..." + " "*30, end="\r", flush=True)
    send_detector_command(DEiger, "arm")
    send_detector_command(DEiger, "trigger", timeout=duration)
    for i in range(duration,0,-1):
        print(f"\r{i} seconds remaining for the current exposure  ",
              end='\r', flush=True)
        time.sleep(1)
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


def measurement(experiment, duration: int = 1, store_location: Path = Path(".")):
    DEiger = experiment.eiger
    DEiger.client.setDetectorConfig("count_time", duration)
    frame_time = DEiger.frame_time
    DEiger.client.setDetectorConfig("frame_time", frame_time)
    nimages_per_file = DEiger.nimages_per_file
    DEiger.client.setFileWriterConfig("nimages_per_file", nimages_per_file)
    n_files, n_images = filemanagement.nfiles(duration, frame_time, nimages_per_file)
    DEiger.client.setDetectorConfig("nimages", n_images)
    measurement_done(DEiger, duration=duration, n_files=n_files)

    last_available_data = DEiger.client.fileWriterFiles()[: n_files - 1]  # order
    # is:
    # datafile,
    # masterfile
    last_available_master = DEiger.client.fileWriterFiles()[n_files - 1]
    logging.info(f"downloading dataset {last_available_data}")

    # parse file number for GISAXS_ dir
    # measurement_no = last_available_master.split("_")[1]
    # alternative: check whether the number can be queried from the detector
    # (via listDetectorConfigParams(self) on the DEigerclient)

    if not os.path.exists(store_location):
        os.mkdir(store_location)

    for item in last_available_data:
        DEiger.client.fileWriterSave(item, store_location)
    copyfile(
        os.path.join(store_location, item),
        Path("/home/ws8665-epics/scan-using-epics-ioc/.current/current.h5"),
    )
    DEiger.client.fileWriterSave(last_available_master, store_location)

    # get current snapshot of chamber pressure, temperature, ...
    # this is recorded at the end of the measurement time
    meta.environment2parrot(experiment)
    # write metadata file
    meta.write_meta_nxs(store_location)

    data = None
    for fname in last_available_data:
        with h5py.File(os.path.join(store_location, fname)) as f:
            if data is None:
                data = np.array(f["entry/data/data"])
            else:
                data += np.array(f["entry/data/data"])
        data_masked = np.where((data >= 0) & (data <= 1e9), data, 0)

    for fname in [*last_available_data, last_available_master]:
        # clean files from detector server
        DEiger.client.fileWriterFiles(fname, method="DELETE")

    logging.info(f"max in image: {np.max(data_masked)}")
    flux = np.sum(data_masked) / duration
    logging.info(f"flux: {flux} cts/s")
    return data_masked


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
