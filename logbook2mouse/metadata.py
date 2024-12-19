import h5py
import os
import numpy as np
import caproto.threading.pyepics_compat as epics

def logbook2parrot(entry, parrot_prefix: str = "pa0"):
    for item in ["proposal", "sampleid", "sampos", "matrixfraction", "samplethickness"]:
        value = getattr(entry, item)
        epics.caput(f"{parrot_prefix}:sample:{item}", value)
    mu_sample = entry.sample.calculate_overall_properties(energy_keV = 8.050)["overall_mu"]
    epics.caput(f"{parrot_prefix}:sample:overall_mu", mu_sample)
    for item in ["batchnum", "user", "protocol", "procpipeline"]:
        value = getattr(entry, item)
        epics.caput(f"{parrot_prefix}:exp:{item}", value)
    epics.caput(f"{parrot_prefix}:exp:additional_parameters",
                entry.additional_parameters.__repr__().encode("utf-8"))
    epics.caput(f"{parrot_prefix}:sample:samplename", entry.sample.sample_name)
    epics.caput(f"{parrot_prefix}:sample:owner", entry.project.name)

def environment2parrot(experiment):
    if "pressure_gauge:pressure" in experiment.required_pvs:
        pressure = epics.caget("pressure_gauge:pressure")
        epics.caput(f"{experiment.parrot_prefix}:environment:pressure", pressure)
    if "portenta:t0" in experiment.required_pvs:
        temperature0 = epics.caget("portenta:t0")
        epics.caput(
            f"{experiment.parrot_prefix}:environment:environment_temperature",
            temperature0)
    if "portenta:t1" in experiment.required_pvs:
        temperature1 = epics.caget("portenta:t1")
        epics.caput(
            f"{experiment.parrot_prefix}:environment:stage_temperature",
            temperature1)
    # X-ray source
    if "source_cu:shutter" in required_pvs:
        source_name = "source_cu"
    else:
        source_name = "source_mo"
    epics.caput(f"{experiment.parrot_prefix}:config:source",
                source_name
                )

    for item in ["shutter", "current", "voltage"]:
        data = epics.caget(f"{source_name}:{item}")
        epics.caput(
            f"{experiment.parrot_prefix}:config:{source_name}:{item}",
            data)

def meta_file_structure(h5file):
    h5file.attrs['default'] = "entry1"

    nxentry = h5file.create_group('entry1')
    nxentry.attrs['NX_class'] = 'NXentry'
    nxentry.attrs['default'] = 'instrument'

    expgroup = nxentry.create_group('experiment')
    for item in ["experiment_identifier", "user", "logbook_date",
                 "protocol", "procpipeline", "additional_parameters",
                 "shutter"]:
        expgroup.create_dataset(item, data="")
    expgroup.create_dataset("batchnum", 0)
    for item in ["stage_temperature", "environment_temperature"]:
        temp = expgroup.create_dataset(item, data=0.0)

    nxinst = nxentry.create_group('instrument')
    nxinst.attrs['NX_class'] = 'NXinstrument'
    nxinst.create_dataset('configuration', data = 0)

    nxdet = nxinst.create_group('detector00')
    nxdet.attrs['NX_class'] = 'NXdetector'

    nxdet.create_dataset("count_time", data=0.0)

    # X-ray source
    nxsource = nxinst.create_group('source')
    nxsource.attrs['NX_class'] = 'NXsource'
    nxsource.create_dataset("type", data = "Fixed Tube X-ray")
    nxsource.create_dataset("probe", data = "x-ray")
    nxsource.create_dataset("name", data = "none")
    current = nxsource.create_dataset("current", data = 0.0)
    current.attrs['units'] = "mA"
    voltage = nxsource.create_dataset("voltage", data = 0.0)
    voltage.attrs['units'] = "kV"

    nxsam = nxentry.create_group('sample')
    nxsam.attrs['NX_class'] = 'NXsample'
    nxsam.attrs['default'] = 'name'

    # initialize empty
    for item in ["name", "owner", "sampos"]:
        nxsam.create_dataset(item, data="", dtype=h5py.string_dtype())
    for item in ["matrixfraction", "samplethickness", "overall_mu"]:
        nxsam.create_dataset(item, data=0.0, dtype=float)
    nxsam.create_dataset("sampleid", data=0, dtype=int)

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
                  "bsr", "bsz", "dual"]:
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

        for item in ["user", "logbook_date", "batchnum",
                     "protocol", "procpipeline"]:
            data = epics.caget(f"{parrot_prefix}:exp:{item}")
            dataset = f[f"/entry1/experiment/{item}"]
            dataset[...] = data

        # X-ray source
        source_name = epics.caget(f"{parrot_prefix}:config:source",
                                  as_string = True)
        dataset = f["/entry1/instrument/source/name"]
        dataset[...] = source_name

        for item in ["current", "voltage"]:
            data = epics.caget(f"{parrot_prefix}:config:{source_name}:{item}")
            dataset = f[f"/entry1/instrument/source/{item}"]
            dataset[...] = data

        shutter_state = epics.caget(f"{parrot_prefix}:config:{source_name}:shutter",
                                    as_string = True)
        dataset = f["/entry1/experiment/shutter"]
        dataset[...] = shutter_state

        # save additional parameters - to fix: contains \x00 before every character
        value = epics.caget(f"{parrot_prefix}:exp:additional_parameters")
        #value = value.tobytes().encode('ASCII')
        value = value.tobytes().decode('utf-8')
        dataset = f[f"/entry1/experiment/additional_parameters"]
        dataset[...] = value.__repr__()

        configuration = epics.caget(f"{parrot_prefix}:config:config_id")
        dataset = f["/entry1/instrument/configuration"]
        dataset[...] = configuration

        count_time = epics.caget(f"{parrot_prefix}:exp:count_time")
        dataset = f["/entry1/instrument/detector00/count_time"]
        dataset[...] = count_time

        for item in ["owner", "sampleid", "sampos",
                     "matrixfraction", "samplethickness", "overall_mu"]:
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

        dualdata = epics.caget(f"{parrot_prefix}:config:dual")
        dataset = f[f"/saxs/Saxslab/dual"]
        dataset[...] = dualdata

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
        for item in ["stage_temperature", "environment_temperature"]:
            temp = epics.caget(f"{parrot_prefix}:environment:{item}")
            dataset = f[f"/entry1/experiment/{item}"]
            dataset[...] = temp
        pressure = epics.caget(f"{parrot_prefix}:environment:pressure")
        dataset = f["/saxs/Saxslab/chamber_pressure"]
        dataset[...] = pressure

