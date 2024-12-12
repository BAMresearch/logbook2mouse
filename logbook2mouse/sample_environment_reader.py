from pathlib import Path
import pandas as pd
from typing import Dict

class SampleEnvironmentReader:
    def __init__(self, file_path: Path):
        """
        Initialize the SampleEnvironmentReader with the path to the logbook file.
        :param file_path: Path to the Excel file containing the logbook data.
        """
        if not file_path.is_file():
            raise FileNotFoundError(f"File {file_path} not found.")
        self.file_path = file_path

    def read_sample_environment(self) -> Dict[str, Dict[str, float]]:
        """
        Reads the 'Sample Environments' sheet and generates a dictionary
        mapping each sampos to its motor values.
        :return: Dictionary with sampos as keys and motor value dictionaries as values.
        """
        try:
            # Load the 'Sample Environments' sheet
            sheet = pd.read_excel(
                self.file_path,
                sheet_name="Sample Environments",
                header=2,  # Start reading from the 3rd row for headers
                engine="openpyxl"
            )

            # Start processing from the second column onwards
            sheet = sheet.iloc[:, 1:]

            # Drop rows where the 'sampos' column (second column) is empty
            sheet = sheet.dropna(subset=["sampos"])

            # Extract motor names from the header row (second column onwards)
            motor_names = sheet.columns[1:]

            # Generate the sampos dictionary
            sampos_data = {}
            for _, row in sheet.iterrows():
                sampos = row["sampos"]
                motor_values = {motor: row[motor] for motor in motor_names if pd.notna(row[motor])}
                sampos_data[sampos] = motor_values

            return sampos_data

        except Exception as e:
            raise ValueError(f"An error occurred while processing the 'Sample Environments' sheet: {e}")


# Example Usage
if __name__ == "__main__":
    file_path = Path("logbook/Logbook_MOUSE.xlsx")  # Replace with your file path
    reader = SampleEnvironmentReader(file_path=file_path)
    sampos_data = reader.read_sample_environment()
    print(sampos_data)
