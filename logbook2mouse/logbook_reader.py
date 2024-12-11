from pathlib import Path
import pandas as pd
import attrs
from typing import Dict, Generator, List, Optional, Union
from .project_reader import ProjectReader, Sample, ProjectInfo

# Convenience functions for date formatting
def convert_date_to_string(date: pd.Timestamp) -> str:
    return date.strftime("%Y%m%d")

def extract_year_from_date(date: pd.Timestamp) -> int:
    return date.year

def optional_converter(converter):
    return lambda x: converter(x) if pd.notna(x) else None

@attrs.define
class Logbook2MouseEntry:
    int_field = lambda: attrs.field(converter=int, validator=attrs.validators.instance_of(int))
    float_field = lambda: attrs.field(converter=float, validator=attrs.validators.instance_of(float))
    str_field = lambda: attrs.field(converter=str, validator=attrs.validators.instance_of(str))
    datetime_field = lambda: attrs.field(converter=pd.to_datetime, validator=attrs.validators.instance_of(pd.Timestamp))
    optional_str_field = lambda: attrs.field(converter=optional_converter(str), validator=attrs.validators.optional(attrs.validators.instance_of(str)))
    optional_int_field = lambda: attrs.field(converter=optional_converter(int), validator=attrs.validators.optional(attrs.validators.instance_of(int)))
    optional_float_field = lambda: attrs.field(converter=optional_converter(float), validator=attrs.validators.optional(attrs.validators.instance_of(float)))
    optional_datetime_field = lambda: attrs.field(converter=optional_converter(pd.to_datetime), validator=attrs.validators.optional(attrs.validators.instance_of(pd.Timestamp)))

    row_index: int = attrs.field(validator=attrs.validators.instance_of(int))
    converttoscript: int = int_field()
    date: pd.Timestamp = datetime_field()
    proposal: str = str_field()
    sampleid: str = str_field()
    user: str = str_field()
    batchnum: int = int_field()
    bgdate: Optional[pd.Timestamp] = optional_datetime_field()
    bgnumber: Optional[int] = optional_int_field()
    dbgdate: Optional[pd.Timestamp] = optional_datetime_field()
    dbgnumber: Optional[int] = optional_int_field()
    matrixfraction: float = float_field()
    samplethickness: float = float_field()
    mu: float = float_field()
    sampos: str = str_field()
    positionx: float = float_field()
    positiony: float = float_field()
    positionz: float = float_field()
    blankpositiony: Optional[float] = optional_float_field()
    blankpositionz: Optional[float] = optional_float_field()
    protocol: str = str_field()
    procpipeline: Optional[str] = optional_str_field()
    maskdate: Optional[pd.Timestamp] = optional_datetime_field()
    notes: Optional[str] = optional_str_field()
    additional_parameters: Dict[str, str] = attrs.field(converter=lambda x: {str(k): str(v) for k, v in x.items()}, validator=attrs.validators.instance_of(dict))

    @classmethod
    def from_series(cls, series: pd.Series):
        # Use the series to create the entry by passing it directly to the constructor
        predefined_fields = [
            "converttoscript", "date", "Proposal", "sampleid", "User", "batchnum", 
            "bgdate", "bgnumber", "dbgdate", "dbgnumber", "matrixfraction", 
            "samplethickness", "mu", "sampos", "positionx", "positiony", "positionz", 
            "blankpositiony", "blankpositionz", "protocol", "procpipeline", "maskdate", "notes",
        ]

        additional_parameters = dict(zip(series.filter(like="key").values, series.filter(like="val").values))
        
        return cls(
            row_index=series.name,
            converttoscript=series["converttoscript"],
            date=series["date"],
            proposal=series["Proposal"],
            sampleid=series["sampleid"],
            user=series["User"],
            batchnum=series["batchnum"],
            bgdate=series["bgdate"],
            bgnumber=series["bgnumber"],
            dbgdate=series["dbgdate"],
            dbgnumber=series["dbgnumber"],
            matrixfraction=series["matrixfraction"],
            samplethickness=series["samplethickness"],
            mu=series["mu"],
            sampos=series["sampos"],
            positionx=series["positionx"],
            positiony=series["positiony"],
            positionz=series["positionz"],
            blankpositiony=series["blankpositiony"],
            blankpositionz=series["blankpositionz"],
            protocol=series["protocol"],
            procpipeline=series["procpipeline"],
            maskdate=series["maskdate"],
            notes=series["notes"],
            additional_parameters=additional_parameters
        )

@attrs.define
class Logbook2MouseReader:
    file_path: Path = attrs.field(validator=[attrs.validators.instance_of(Path), lambda inst, attr, value: value.is_file() or ValueError(f"Logbook file: {value} does not exist.")])
    project_base_path: Path = attrs.field(validator=[attrs.validators.instance_of(Path), lambda inst, attr, value: value.is_dir() or ValueError(f"Base project directory: {value} cannot be accessed.")])
    entries: List[Logbook2MouseEntry] = attrs.field(init=False, factory=list) # entries
    projects: List[ProjectInfo] = attrs.field(init=False, factory=list) # their associated projects (most of which will be the same)
    samples: List[Sample] = attrs.field(init=False, factory=list) # their associated samples
    _preloaded_projects: Dict[str, ProjectInfo] = attrs.field(init=False, factory=dict) # cache for preloaded projects. key is the project ID

    def __attrs_post_init__(self):
        self.entries = self.get_entries()
        self.gather_projects
        self.projects = [self.get_project(entry.proposal) for entry in self.entries]
        self.samples = [self.get_sample(entry.proposal, entry.sampleid) for entry in self.entries]
        
    def read_logbook(self) -> pd.DataFrame:
        # Specify column types and converters for custom conversion if needed
        dtype_spec = {
            "converttoscript": "Int64",
            "date": "datetime64[ns]",
            "Proposal": "string",
            "sampleid": "string",
            "User": "string",
            "batchnum": "Int64",
            "bgdate": "datetime64[ns]",
            "bgnumber": "Int64",
            "dbgdate": "datetime64[ns]",
            "dbgnumber": "Int64",
            "matrixfraction": "float",
            "samplethickness": "float",
            "mu": "float",
            "sampos": "string",
            "positionx": "float",
            "positiony": "float",
            "positionz": "float",
            "blankpositiony": "float",
            "blankpositionz": "float",
            "protocol": "string",
            "procpipeline": "string",
            "maskdate": "datetime64[ns]",
            "notes": "string"
        }

        try:
            df = pd.read_excel(
                self.file_path,
                header=2,
                engine="openpyxl",
                usecols=lambda x: x not in ["Unnamed: 0", None],
                parse_dates=["date", "bgdate", "dbgdate", "maskdate"],
                dtype=dtype_spec,
                na_values=None #["NA", "N/A", "-", " "]
            )

        except FileNotFoundError:
            raise ValueError(f"File {self.file_path} not found.")
        except pd.errors.EmptyDataError:
            raise ValueError("Excel file is empty or contains no data.")
        except Exception as e:
            raise ValueError(f"An error occurred while reading the Excel file: {e}")

        # drop rows that are mostly blank
        df = df.dropna(axis=0, thresh=2)
        return df

    def get_entries(self) -> List[Logbook2MouseEntry]:
        df = self.read_logbook()
        # entries = []
        entries = [Logbook2MouseEntry.from_series(row) for _, row in df.iterrows() if row["converttoscript"] == 1]

        return entries

    def get_project(self, projectID) -> ProjectInfo:
        if projectID in self._preloaded_projects:
            return self._preloaded_projects[projectID]
        else:
            project_file = self.project_base_path / f"{projectID}.xlsx"
            if project_file.is_file():
                project = ProjectReader(file_path=project_file).project_info
                self._preloaded_projects[projectID] = project
                return project
            else:
                raise FileNotFoundError(f"Project file {project_file} not found.")

    def gather_projects(self) -> List[ProjectInfo]:
        projects = []
        for entry in self.entries:
            # just load them in the cache so we have them available
            _ = self.get_project(entry.proposal)

    def get_sample(self, projectID, sampleID) -> Sample:
        project = self.get_project(projectID)
        return next((s for s in project.samples if s.sample_id == sampleID), None)

    def entries_iterator(self) -> Generator[Logbook2MouseEntry, None, None]:
        for idx, entry in self.entries.items():
            yield idx, entry
