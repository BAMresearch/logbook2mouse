import os
import unittest
import pandas as pd
from logbook2mouse.logbook_reader import Logbook2MouseReader, Logbook2MouseEntry, extract_year_from_date, convert_date_to_string
from pathlib import Path
from unittest.mock import patch
import shutil
import sys

from logbook2mouse.measurement_script import MeasurementScript

import logging

logger = logging.getLogger("logbook2mouse")

class TestMeasurementScript(unittest.TestCase):

    def setUp(self):
        # Using the provided Excel file for testing
        self.file_path = Path("logbook/Logbook_MOUSE.xlsx")
        self.reader = Logbook2MouseReader(self.file_path, project_base_path=Path("tests/testdata/projects"))
        self.output_directory = Path("tests/output")
        self.script = MeasurementScript(self.reader.entries, protocol_directory=Path('protocols'), output_filepath=self.output_directory)

    def test_validation(self):
        # Test the validation process
        try:
            self.script.validate()
        except Exception as e:
            self.fail(f"Validation failed with exception: {e}")

    def tearDown(self):
        # Cleanup code if necessary
        output_file = self.output_directory / "measurement_script.txt"
        if output_file.exists():
            output_file.unlink()
        if self.output_directory.exists():
            os.rmdir(self.output_directory)

class TestLogbook2Mouse(unittest.TestCase):

    def setUp(self):
        # Using the provided Excel file for testing
        self.file_path = Path("logbook/Logbook_MOUSE.xlsx")

    def test_read_logbook_and_generate_script(self):
        reader = Logbook2MouseReader(self.file_path, project_base_path=Path("tests/testdata/projects"))

        # Check if the correct number of entries is generated
        self.assertGreater(len(reader.entries), 0, "No entries found where converttoscript is set to 1")

        # Check data types of the entries
        for entry in reader.entries:
            logger.info(f"Checking entry at row {entry.row_index}")
            self.assertIsInstance(entry, Logbook2MouseEntry)
            self.assertIsInstance(entry.converttoscript, int)
            self.assertIsInstance(entry.date, pd.Timestamp)
            self.assertIsInstance(entry.proposal, str)
            self.assertIsInstance(entry.sampleid, str)
            self.assertIsInstance(entry.user, str)
            self.assertIsInstance(entry.batchnum, int)
            self.assertTrue(isinstance(entry.bgdate, pd.Timestamp) or entry.bgdate is None)
            self.assertTrue(isinstance(entry.bgnumber, int) or entry.bgnumber is None)
            self.assertTrue(isinstance(entry.dbgdate, pd.Timestamp) or entry.dbgdate is None)
            self.assertTrue(isinstance(entry.dbgnumber, int) or entry.dbgnumber is None)
            self.assertIsInstance(entry.matrixfraction, float)
            self.assertIsInstance(entry.samplethickness, float)
            # self.assertIsInstance(entry.mu, float)
            self.assertIsInstance(entry.sampos, str)
            # self.assertIsInstance(entry.positionx, float)
            # self.assertIsInstance(entry.positiony, float)
            # self.assertIsInstance(entry.positionz, float)
            # self.assertTrue(isinstance(entry.blankpositiony, float) or entry.blankpositiony is None)
            # self.assertTrue(isinstance(entry.blankpositionz, float) or entry.blankpositionz is None)
            self.assertIsInstance(entry.protocol, str)
            self.assertTrue(isinstance(entry.procpipeline, str) or entry.procpipeline is None)
            # self.assertTrue(isinstance(entry.maskdate, pd.Timestamp) or entry.maskdate is None)
            self.assertTrue(isinstance(entry.notes, str) or entry.notes is None)
            self.assertIsInstance(entry.additional_parameters, dict)

    def test_convert_date_to_string(self):
        # Test the convenience function to convert date to string
        date = pd.Timestamp("2023-03-15")
        date_str = convert_date_to_string(date)
        self.assertEqual(date_str, "20230315", "Date conversion to string failed")

    def test_extract_year_from_date(self):
        # Test the convenience function to extract year from date
        date = pd.Timestamp("2023-03-15")
        year = extract_year_from_date(date)
        self.assertEqual(year, 2023, "Year extraction from date failed")

    def tearDown(self):
        # Cleanup code if necessary
        pass


class TestLogbook2MouseMain(unittest.TestCase):

    def setUp(self):
        # Set up paths for testing
        self.test_logbook = Path("logbook") / "Logbook_MOUSE.xlsx"
        self.protocols_directory = Path("protocols") / "protocols"
        self.project_base_directory = Path("tests") / "testdata" / "projects"
        self.output_script_file = Path("tests") / "output" / "measurement_script.txt"
        
        # Create dummy data for the tests
        self.protocols_directory.mkdir(parents=True, exist_ok=True)
        self.output_script_file.parent.mkdir(parents=True, exist_ok=True)

        # Create a dummy protocol file
        protocol_file = self.protocols_directory / "protocol1.py"
        with open(protocol_file, 'w') as f:
            f.write("def execute_protocol(entry): pass")

    def test_main_script(self):
        # Mock sys.argv to simulate command line arguments
        test_args = [
            "logbook2mouse",  # Simulate the module name
            str(self.test_logbook),  # Logbook file argument
            str(self.protocols_directory),  # Protocols directory argument
            str(self.project_base_directory),  # Project base directory argument
            str(self.output_script_file),  # Output script file argument
            "-vv",  # Verbosity flag for DEBUG
            "--log_file", "tests/log_output.log"  # Log file output
        ]

        with patch.object(sys, 'argv', test_args):
            from logbook2mouse.__main__ import parse_args, configure_logging

            # Test argument parsing
            args = parse_args()
            self.assertEqual(str(args.logbook_file), str(self.test_logbook))
            self.assertEqual(str(args.protocols_directory), str(self.protocols_directory))
            self.assertEqual(str(args.output_script_file), str(self.output_script_file))
            self.assertEqual(args.verbosity, 2)
            self.assertEqual(args.log_file, "tests/log_output.log")

            # Test logger configuration
            logger = configure_logging(
                log_level=logging.DEBUG,
                log_to_file=True,
                log_file_path="tests/log_output.log"
            )
            self.assertEqual(logger.level, logging.DEBUG)
            self.assertTrue(any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers))

            # Test executing the __main__ script logic
            try:
                # Simulate script execution by calling the relevant methods
                reader = Logbook2MouseReader(Path(args.logbook_file), project_base_path=Path(args.project_base_path))
                script = MeasurementScript(
                    entries=list(reader.entries.values()),
                    output_directory=Path(args.protocols_directory)
                )
                script.save_script(args.output_script_file)

                # Check that output script was created successfully
                self.assertTrue(self.output_script_file.is_file(), "Output script file was not created")

            except Exception as e:
                self.fail(f"An error occurred during the execution of the main script: {e}")

    def tearDown(self):
        # Clean up created files and directories
        if self.output_script_file.is_file():
            self.output_script_file.unlink()
        if Path("tests/log_output.log").is_file():
            Path("tests/log_output.log").unlink()

if __name__ == "__main__":
    unittest.main()
