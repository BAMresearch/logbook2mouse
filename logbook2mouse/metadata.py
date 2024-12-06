import h5py
import os
import numpy as np
import caproto.threading.pyepics_compat as epics

def logbook2parrot(entry, parrot_prefix: str = "pa0"):
    for item in ["proposal", "sampleid", "sampos"]:
        value = getattr(entry, item)
        epics.caput(f"{parrot_prefix}:sample:{item}", value)
    epics.caput(f"{parrot_prefix}:exp:operator", entry.user)

def environment2parrot(experiment):
    if "pressure_gauge:pressure" in experiment.required_pvs:
        pressure = epics.caget("pressure_gauge:pressure")
        epics.caput(f"{experiment.parrot_prefix}:environment:pressure", pressure)

def meta_file_structure(h5file):
    h5file.attrs['default'] = "entry1"

    nxentry = h5file.create_group('entry1')
    nxentry.attrs['NX_class'] = 'NXentry'
    nxentry.attrs['default'] = 'instrument'

    expgroup = nxentry.create_group('experiment')
    for item in ["experiment_identifier", "operator", "logbook_date"]:
        expgroup.create_dataset(item, data="")

    nxinst = nxentry.create_group('instrument')
    nxinst.attrs['NX_class'] = 'NXinstrument'
    nxinst.create_dataset('configuration', data = 0)

    nxdet = nxinst.create_group('detector00')
    nxdet.attrs['NX_class'] = 'NXdetector'

    # initialize empty
    nxdet.create_dataset("count_time", data=0.0)

    nxsam = nxentry.create_group('sample')
    nxsam.attrs['NX_class'] = 'NXsample'
    nxsam.attrs['default'] = 'name'

    # initialize empty
    for item in ["name", "owner", "sampleid", "sampos"]:
        nxsam.create_dataset(item, data="", dtype=h5py.string_dtype())

    # saxslab

    nxsaxs = h5file.create_group('saxs')
    nxsaxslab = nxsaxs.create_group('Saxslab')

    # detector positions
    # initialize empty
    nxsaxslab.create_dataset("detx", data=0.0, dtype="f")
    nxsaxslab.create_dataset('dety', data=0.0, dtype="f")
    nxsaxslab.create_dataset('detz', data=0.0, dtype="f")

    # motor positions

    for motor in ["ysam", "zsam",
                  "zheavy", "pitchgi", "rollgi", "yawgi",
                  "bsr", "bsz"]:
        # initialize empty
        nxsaxslab.create_dataset(motor, data=0.0, dtype = "f")

    for direction in ["horizontal", "vertical"]:
        for i in range(1,4):
            for attribute in ["position", "gap"]:
                saxslabattr = f"{direction[0]}{attribute[0]}{i}"
                # initialize empty
                nxsaxslab.create_dataset(saxslabattr, data=0.0, dtype = "f")
            if direction == "horizontal":
                for attribute in ["hl", "hr"]:
                    saxslabattr = f"s{i}{attribute}"
                    # initialize empty
                    nxsaxslab.create_dataset(saxslabattr, data=0.0, dtype = "f")
            else:
                for attribute in ["top", "bot"]:
                    saxslabattr = f"s{i}{attribute}"
                    # initialize empty
                    nxsaxslab.create_dataset(saxslabattr, data=0.0, dtype = "f")

    # environment variables
    nxsaxslab.create_dataset("chamber_pressure", data=0.0, dtype="f")
    return h5file


def write_meta_nxs(store_location, parrot_prefix: str="pa0"):
    metafile = "im_craw.nxs"
    with h5py.File(os.path.join(store_location, metafile), 'w') as f:
        f = meta_file_structure(f)

        proposal = epics.caget(f"{parrot_prefix}:sample:proposal")
        dataset = f["/entry1/experiment/experiment_identifier"]
        dataset[...] = proposal

        for item in ["operator", "logbook_date"]:
            data = epics.caget(f"{parrot_prefix}:exp:{item}")
            dataset = f[f"/entry1/experiment/{item}"]
            dataset[...] = data

        configuration = epics.caget(f"{parrot_prefix}:config:config_id")
        dataset = f["/entry1/instrument/configuration"]
        dataset[...] = configuration

        count_time = epics.caget(f"{parrot_prefix}:exp:count_time")
        dataset = f["/entry1/instrument/detector00/count_time"]
        dataset[...] = count_time

        for item in ["owner", "sampleid", "sampos"]:
            value = epics.caget(f"{parrot_prefix}:sample:{item}")
            dataset = f[f"/entry1/sample/{item}"]
            dataset[...] = value

        samplename = epics.caget(f"{parrot_prefix}:sample:samplename")
        dataset = f["/entry1/sample/name"]
        dataset[...] = samplename

        for detmotor in ["detx", "dety", "detz"]:
            detdata = epics.caget(f"{parrot_prefix}:config:{detmotor}")
            dataset = f[f"/saxs/Saxslab/{detmotor}"]
            dataset[...] = detdata

        for bsmotor in ["bsr", "bsz"]:
            detdata = epics.caget(f"{parrot_prefix}:config:beamstop:{bsmotor}")
            dataset = f[f"/saxs/Saxslab/{bsmotor}"]
            dataset[...] = detdata

        # motor positions

        for motor in ["ysam", "zsam", "zheavy", "pitchgi", "rollgi", "yawgi"]:
            motor_data = epics.caget(f"{parrot_prefix}:environment:motors:{motor}")
            dataset = f[f"/saxs/Saxslab/{motor}"]
            dataset[...] = motor_data

        for direction in ["horizontal", "vertical"]:
            for i in range(1,4):
                for attribute in ["position", "gap"]:
                    saxslabattr = f"{direction[0]}{attribute[0]}{i}"
                    parrot_address = f"{parrot_prefix}:config:slits:{direction}{i}:{attribute}"
                    slit_data = epics.caget(parrot_address)
                    dataset = f[f"/saxs/Saxslab/{saxslabattr}"]
                    dataset[...] = slit_data
                if direction == "horizontal":
                    bladeattrs = ["hl", "hr"]
                else:
                    bladeattrs = ["top", "bot"]
                for attribute in bladeattrs:
                    saxslabattr = f"s{i}{attribute}"
                    parrot_address = f"{parrot_prefix}:config:slits:{direction}{i}:{attribute}"
                    slit_data = epics.caget(parrot_address)
                    dataset = f[f"/saxs/Saxslab/{saxslabattr}"]
                    dataset[...] = slit_data

        # environment variables
        pressure = epics.caget(f"{parrot_prefix}:environment:pressure")
        dataset = f["/saxs/Saxslab/chamber_pressure"]
        dataset[...] = pressure

