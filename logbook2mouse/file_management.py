import os
import logging
import numpy as np
from pathlib import Path

from logbook2mouse.logbook_reader import Logbook2MouseEntry
from logbook2mouse.experiment import ExperimentVariables

def work_directory(entry: Logbook2MouseEntry, experiment: ExperimentVariables) -> Path:
    timestamp = entry.date
    ymd = timestamp.strftime("%Y%m%d")
    work_directory = experiment.data_dir / str(timestamp.year) / ymd
    if os.path.exists(work_directory):
        logging.info(f"Measurement directory {ymd} already in use. Data will be added to this directory. ")
    else:
        os.mkdir(work_directory)
    return work_directory

def scan_counter_next(scan_counter, work_directory, entry):
    get_no = lambda dirname: int(dirname.split("_")[-1])
    ymd = entry.date.strftime('%Y%m%d')
    batch = entry.batchnum
    scan_numbers = np.array([get_no(d) for d in next(os.walk(work_directory))[1] if d.startswith(f"{ymd}_{batch}_")])
    if scan_numbers.size == 0:
        value = 0
    elif scan_counter <= np.max(scan_numbers):
        value = np.max(scan_numbers) + 1
    else:
        value = scan_counter
    return int(value)

def scan_counter_simple(scan_counter, work_directory):
    get_no = lambda dirname: int(dirname.split("_")[-1])
    scan_numbers = np.array([get_no(d) for d in next(os.walk(work_directory))[1] if d.startswith(f"scan_")])
    if scan_numbers.size == 0:
        value = 0
    elif scan_counter <= np.max(scan_numbers):
        value = np.max(scan_numbers) + 1
    else:
        value = scan_counter
    return int(value)
