from pathlib import Path
import numpy as np
import pandas as pd
import attrs
from typing import Dict, List, Optional
import periodictable as pt
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def validate_density(instance, attribute, value):
    if value <= 0:
        raise ValueError(f"{attribute.name} must be a positive float.")


def nan_to_none(value):
    """Convert NaN to None."""
    return None if value is None or (isinstance(value, float) and np.isnan(value)) else value


def compute_mass_fraction(volume_fraction: float, density: float) -> float:
    """Compute mass fraction from volume fraction and density."""
    return volume_fraction * density if volume_fraction is not None else None


def compute_volume_fraction(mass_fraction: float, density: float) -> float:
    """Compute volume fraction from mass fraction and density."""
    return mass_fraction / density if mass_fraction is not None else None


@attrs.define
class ProjectInfo:
    name: str = attrs.field()
    organisation: str = attrs.field()
    email: str = attrs.field()
    title: str = attrs.field()
    description: str = attrs.field()
    public_release: bool = attrs.field(converter=lambda x: x.lower() == "yes")
    release_location: Optional[str] = attrs.field(default=None)
    co_authorship: bool = attrs.field(default=False, converter=lambda x: x.lower() == "yes")
    no_co_authorship_reason: Optional[str] = attrs.field(default=None)


@attrs.define
class SampleComponent:
    component_id: str = attrs.field()
    composition: str = attrs.field(validator=lambda _, __, value: pt.formula(value))
    density: float = attrs.field(validator=validate_density, default=1.0) # negative density to force user to provide it
    volume_fraction: Optional[float] = attrs.field(converter=nan_to_none, validator=attrs.validators.optional(attrs.validators.instance_of(float)), default=None)
    mass_fraction: Optional[float] = attrs.field(converter=nan_to_none, validator=attrs.validators.optional(attrs.validators.instance_of(float)), default=None)
    connection: Optional[str] = attrs.field(default=None)
    connected_to: Optional[str] = attrs.field(default=None)
    name: str = attrs.field(default="")

    def __attrs_post_init__(self):
        if self.volume_fraction is None and self.mass_fraction is not None:
            print(f"Computing volume fraction for component {self.component_id} using mass fraction {self.mass_fraction} and density {self.density}.")
            self.volume_fraction = compute_volume_fraction(self.mass_fraction, self.density)
        elif self.mass_fraction is None and self.volume_fraction is not None:
            print(f"Computing mass fraction for component {self.component_id} using volume fraction {self.volume_fraction} and density {self.density}.")
            self.mass_fraction = compute_mass_fraction(self.volume_fraction, self.density)

    def calculate_xray_properties(self, energy_keV: float) -> Dict[str, float]:
        """Calculate X-ray properties using the periodictable library."""
        material = pt.formula(self.composition)
        sld, mu = pt.xray_sld(material, energy=energy_keV, density=self.density)
        # mu = material.mass * self.density * sld.imag  # Absorption coefficient approximation
        return {"mu": mu, "sld": sld}


@attrs.define
class Sample:
    sample_id: str = attrs.field()
    sample_name: str = attrs.field()
    components: List[SampleComponent] = attrs.field(factory=list)

    def normalize_fractions(self):
        """Normalize volume and mass fractions to ensure their sum does not exceed 1."""
        total_volume = sum(
            c.volume_fraction for c in self.components if c.volume_fraction is not None
        )
        total_mass = sum(
            c.mass_fraction for c in self.components if c.mass_fraction is not None
        )

        # if total_volume > 1.0:
        for c in self.components:
            if c.volume_fraction is not None:
                c.volume_fraction /= total_volume

        # if total_mass > 1.0:
        for c in self.components:
            if c.mass_fraction is not None:
                c.mass_fraction /= total_mass

    def calculate_overall_properties(self, energy_keV: float) -> Dict[str, float]:
        """Calculate overall X-ray properties for the sample."""
        self.normalize_fractions()

        overall_mu = 0.0
        for c in self.components:
            print(c)
            props = c.calculate_xray_properties(energy_keV)
            vf = c.volume_fraction if c.volume_fraction is not None else 0
            overall_mu += props["mu"] * vf

        return {"overall_mu": overall_mu}


@attrs.define
class ExcelProjectReader:
    file_path: Path = attrs.field(validator=attrs.validators.instance_of(Path))
    project_info: ProjectInfo = attrs.field(init=False)
    samples: List[Sample] = attrs.field(init=False)

    def __attrs_post_init__(self):
        self.project_info = self._read_project_info()
        self.samples = self._read_samples()

    def _read_project_info(self) -> ProjectInfo:
        project_sheet = pd.read_excel(self.file_path, sheet_name=0, header=None, engine="openpyxl")
        return ProjectInfo(
            name=project_sheet.iloc[1, 1],
            organisation=project_sheet.iloc[2, 1],
            email=project_sheet.iloc[3, 1],
            title=project_sheet.iloc[6, 1],
            description=project_sheet.iloc[7, 1],
            public_release=project_sheet.iloc[8, 1],
            release_location=project_sheet.iloc[9, 1],
            co_authorship=project_sheet.iloc[10, 1],
            no_co_authorship_reason=project_sheet.iloc[11, 1] if len(project_sheet) > 11 else None,
        )

    def _read_samples(self) -> List[Sample]:
        samples_sheet = pd.read_excel(self.file_path, sheet_name=1, header=2, engine="openpyxl")
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

    # Project Information
    print(reader.project_info)

    # Sample Information
    for sample in reader.samples:
        print(sample)
        print(sample.calculate_overall_properties(energy_keV=8.05))  # Copper K-alpha energy
