import os
import logging
import numpy as np
from pathlib import Path

def work_directory(entry, basedir = Path("/home/ws8665-epics/data/")) -> Path:
    timestamp = entry.date
    ymd = timestamp.strftime("%Y%m%d")
    work_directory = basedir / str(timestamp.year) / ymd
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

def nfiles(duration: int, frame_time: int, nimages_per_file: int) -> tuple[int]:
    "calculate the number of expected files for a given duration"
    nimages = duration // frame_time
    if duration % frame_time > 0:
        nimages += 1
    duration = (nimages*frame_time + 3)*1.01 # same as in SL.py
    n_files = nimages // nimages_per_file
    if nimages % nimages_per_file > 0:
        n_files += 1
    n_files += 1  # master file
    return n_files, nimages
