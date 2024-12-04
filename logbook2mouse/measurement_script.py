import importlib.util
import os
import attrs
from pathlib import Path
from typing import List
from epics import caget

from logbook2mouse.logbook_reader import Logbook2MouseEntry
from logbook2mouse.measure_config import standard_configurations

@attrs.define
class MeasurementScript:
    entries: List[Logbook2MouseEntry]
    protocols_directory: Path
    output_script_path: Path
    output_directory: Path = attrs.field(init=False)

    def __attrs_post_init__(self):
        self.output_directory = self.output_script_path.parent
        assert self.output_directory.exists(), f"Output directory does not exist: {self.output_directory}"
        assert self.protocols_directory.exists(), f"Protocols directory does not exist: {self.protocols_directory}"

    def generate_script(self):
        script_lines = []

        # Script startup
        script_lines += self.load_protocol_template(protocol_path=self.protocols_directory/'setup.py')

        # For every entry in the logbook
        for entry in self.entries:
            # Include the measurement protocol template for this entry
            script_lines += f"entry = {entry}"
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
