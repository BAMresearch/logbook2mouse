import importlib.util
import os, copy
import attrs
from pathlib import Path
from typing import List
from epics import caget
import pandas as pd

from logbook2mouse.logbook_reader import Logbook2MouseEntry
from logbook2mouse.measure_config import standard_configurations

@attrs.define
class MeasurementScript:
    entries: List[Logbook2MouseEntry]
    protocols_directory: Path
    output_script_path: Path
    output_directory: Path = attrs.field(init=False)
    collate: bool

    def __attrs_post_init__(self):
        self.output_directory = self.output_script_path.parent
        assert self.output_directory.exists(), f"Output directory does not exist: {self.output_directory}"
        assert self.protocols_directory.exists(), f"Protocols directory does not exist: {self.protocols_directory}"

    def collate_configurations(self):
        """
        Generate configurations to be measured and collect in dataframe.

        The command-line argument '--collate' dictates whether all measurements
        for one configuration are done before moving to the next one.
        In terms of the data frame returned, the configurations are the rows
        of the dataframe with this option.

        The resulting dataframe is converted into the measurement script
        in left-to-right reading order.

        Example:

            input:

            line number | sample     | ... | key1           | var1      |
            1           | sample 1   | ... | configurations | standard  |
            2           | sample 2   | ... | configurations | standard  |
            3           | sample 3   | ... | configurations | capillary |
            4           | sample 4   | ... | configuration  | 251       |


            output with self.collate = True: - measure everything at a given config first

            configuration number
             |
             v  | line 1   | line 2   | line 3   | line 4   | <- logbook line
            151 | sample 1 | sample 2 |          |          |
            123 | sample 1 | sample 2 |          |          |
            125 | sample 1 | sample 2 |          |          |
            127 | sample 1 | sample 2 |          |          |
            110 |          |          | sample 3 |          |
            113 |          |          | sample 3 |          |
            115 |          |          | sample 3 |          |
            117 |          |          | sample 3 |          |
            251 |          |          |          | sample 4 |


            output with self.collate = False - measure everthing for a given sample at once

            logbook line
            |
            v | 151      | 123      | 125      | 127      | 110      | 113      | 115      | 117      | 251  <- configuration
            1 | sample 1 | sample 1 | sample 1 | sample 1 |          |          |          |          |
            2 | sample 2 | sample 2 | sample 2 | sample 2 |          |          |          |          |
            3 | sample 1 | sample 2 |          |          | sample 3 | sample 3 | sample 3 | sample 3 |
            4 | sample 1 | sample 2 |          |          |          |          |          |          | sample 4


        Returns:
            pd.DataFrame[Logbook2MouseEntry]

        """
        measurement_matrix = {}
        for entry in self.entries:
            parsed_entries = {}
            if "configurations" in entry.additional_parameters.keys():
                # shortcuts for standard measurements for powders and liquids
                configurations = standard_configurations(entry.additional_parameters.get("configurations"))
                for config in configurations:
                    new_entry = copy.deepcopy(entry)
                    new_entry.additional_parameters["configuration"] = config
                    parsed_entries[config] = new_entry
            elif "configuration" in entry.additional_parameters.keys():
                # single requested configuration
                parsed_entries[entry.additional_parameters["configuration"]] = entry
            else:
                # let's not call a configuration number 0 in the future...
                parsed_entries[0] = entry
            measurement_matrix[entry.row_index] = parsed_entries
        if self.collate == True:
            df = pd.DataFrame.from_dict(measurement_matrix, orient = "columns")
        else:
            df = pd.DataFrame.from_dict(measurement_matrix, orient = "index")
        return df

    def generate_script(self):
        script_lines = []

        # Script startup
        script_lines += self.load_protocol_template(protocol_path=self.protocols_directory/'setup.py')

        entry_df = self.collate_configurations()
        for r, row in entry_df.iterrows():
            for e, entry in row.items():
                if type(entry) == Logbook2MouseEntry:
                    print(f"Generating measurement script for ymd {entry.date}, sample position {entry.sampos}, configuration {entry.additional_parameters['configuration']}")
                    script_lines += f"entry = {entry}" + "\n"
                    script_lines += self.load_protocol_template(entry)

        # Script shutdown
        script_lines += self.load_protocol_template(protocol_path=self.protocols_directory/'teardown.py')

        return "".join(script_lines)

    def load_protocol_template(self, entry: Logbook2MouseEntry | None = None, protocol_path:Path | None = None) -> List[str]:
        """
        Load the protocol template as a list of lines from the protocols directory.
        """
        if entry is not None: 
            protocol_path = self.protocols_directory / entry.protocol
        else: 
            assert protocol_path is not None, "Either entry or protocol_path must be provided."

        assert protocol_path.is_file(), f"Protocol file {protocol_path} not found."

        try:
            with open(protocol_path, 'r') as file:
                template_lines = file.readlines()
            return template_lines

        except Exception as e:
            return [f"# Error while loading protocol {protocol_path}: {e}"]

    def validate(self):
        """Validates that all necessary components for execution are available."""
        # Validate output directory
        if not self.output_directory.exists():
            print(f"Output directory does not exist: {self.output_directory}. It will be created.")
            os.makedirs(self.output_directory, exist_ok=True)

        # Validate each logbook entry
        for entry in self.entries:
            # Validate protocol file existence
            protocol_path = Path(self.protocols_directory, entry.protocol)
            if not protocol_path.is_file():
                raise FileNotFoundError(f"Protocol file {entry.protocol} not found for sample {entry.sampleid}.")

            # Validate EPICS PVs (mocked PV names as examples)
            required_pvs = [
                'SAMPLE:POSITION:X',
                'SAMPLE:POSITION:Y',
                'SAMPLE:POSITION:Z',
                'SAMPLE:TEMP:SETPOINT'
            ]
            for pv in required_pvs:
                value = caget(pv)
                if value is None:
                    raise ConnectionError(f"PV '{pv}' is not reachable or has no value.")

            # Validate required additional parameters are provided in entry
            required_params = ['temperature_setpoint']
            for param in required_params:
                if param not in entry.additional_parameters:
                    raise ValueError(f"Missing required parameter '{param}' for sample {entry.sampleid}.")

    def save_script(self, output_file: Path | str) -> None:
        script_content = self.generate_script()
        with open(output_file, 'w') as f:
            f.write(script_content)
