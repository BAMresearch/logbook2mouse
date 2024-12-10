from pathlib import Path
import pandas as pd
import attrs
from typing import List, Dict, Optional
import periodictable 

@attrs.define
class ProjectInfo:
    name: str = attrs.field()
    organisation: str = attrs.field()
    email: str = attrs.field()
    title: str = attrs.field()
    description: str = attrs.field()
    public_release: Optional[str] = attrs.field(default=None)
    release_location: Optional[str] = attrs.field(default=None)
    co_authorship: Optional[str] = attrs.field(default=None)
    no_co_authorship_reason: Optional[str] = attrs.field(default=None)


@attrs.define
class SampleComponent:
    component_id: str = attrs.field()
    connection: Optional[str] = attrs.field(default=None)
    connected_to: Optional[str] = attrs.field(default=None)
    name: str = attrs.field(default='')
    composition: str = attrs.field(default='')
    density: float = attrs.field(default=1.0)
    volume_fraction: Optional[float] = attrs.field(default=None)
    mass_fraction: Optional[float] = attrs.field(default=None)


@attrs.define
class Sample:
    sample_id: str = attrs.field()
    sample_name: str = attrs.field()
    components: List[SampleComponent] = attrs.field(factory=list)


@attrs.define
class ExcelProjectReader:
    file_path: Path = attrs.field(validator=attrs.validators.instance_of(Path))
    project_info: ProjectInfo = attrs.field(init=False)
    samples: List[Sample] = attrs.field(init=False)

    def __attrs_post_init__(self):
        self.project_info = self._read_project_info()
        self.samples = self._read_samples()

    def _read_project_info(self) -> ProjectInfo:
        project_sheet = pd.read_excel(self.file_path, sheet_name=0, header=None, engine='openpyxl')
        return ProjectInfo(
            name=project_sheet.iloc[1, 1],
            organisation=project_sheet.iloc[2, 1],
            email=project_sheet.iloc[3, 1],
            title=project_sheet.iloc[6, 1],
            description=project_sheet.iloc[7, 1],
            public_release=project_sheet.iloc[8, 1],
            release_location=project_sheet.iloc[9, 1],
            co_authorship=project_sheet.iloc[10, 1] if len(project_sheet) > 10 else None,
            no_co_authorship_reason=project_sheet.iloc[11, 1] if len(project_sheet) > 11 else None,
        )

    def _read_samples(self) -> List[Sample]:
        samples_sheet = pd.read_excel(self.file_path, sheet_name=1, header=2, engine='openpyxl')
        sample_groups = []
        current_sample = None

        for _, row in samples_sheet.iterrows():
            if pd.notna(row["sampleId"]):  # Start of a new sample
                if current_sample:
                    sample_groups.append(current_sample)
                current_sample = [row]
            elif current_sample is not None:  # Continuation of the current sample
                current_sample.append(row)

        if current_sample:  # Add the last sample group
            sample_groups.append(current_sample)

        samples = []
        for group in sample_groups:
            sample_df = pd.DataFrame(group)
            sample_id = str(sample_df.iloc[0]["sampleId"])
            sample_name = sample_df.iloc[0]["sampleName"]

            components = [
                SampleComponent(
                    component_id=row["componentId"],
                    connection=row.get("componentConnection", None),
                    connected_to=row.get("componentConnectedTo", None),
                    name=row["componentName"],
                    composition=row["composition"],
                    density=row["density"],
                    volume_fraction=row.get("volFrac", None),
                    mass_fraction=row.get("massFrac", None),
                )
                for _, row in sample_df.iterrows()
                if pd.notna(row["componentId"])
            ]

            samples.append(Sample(sample_id=sample_id, sample_name=sample_name, components=components))

        return samples
    
if __name__ == "__main__":
    file_path = Path("project/Project_Form_5.0.xlsx")
    reader = ExcelProjectReader(file_path=file_path)

    # Access project information
    print(reader.project_info)

    # Access samples
    for sample in reader.samples:
        print(sample)