# Logbook2Mouse

This library reads a measurement logbook and associated project/sample information
and generates a script for a SAXS instrument. Currently still under development.

## Installation

```bash
python3.12 -m venv .venv
pip install -e .
```

## before using... 

Note that the logbook contains a second sheet with motor positions for sample stages. 
This is now set up so that you can have an arbitrary number of columns (motors) for a given stage position ID. 
That should allow for the use of alternative stages such as the GISAXS stage for experiments, which has five motors
instead of the normal two cartesian stages we have. 

Secondly, the script retrieves project and sample information from the project/sample sheets. These must therefore 
be present before you run the logbook2mouse script. This is done on purpose to ensure these project/sample sheets
are actually used and filled in, as they also allow us to track our experiments better. 

The project/sample sheets live in a separate directory structure, whcih must be organized by [year]/[proposalid].xlsx
The proposal file name (used as the ProposalID) *must* start with the four-digit year. In our lab, we use the format
[YYYY][nnn].xlsx for these proposal sheets, but in principle you're free to use how you adapt the second part of the
filename. 

### a word on specifying sample composition
The samples must have the components specified, with an atomic composition and a density estimate (not a range!). 
Please be careful to ensure the compositions and densities are machine-interpretable, so atomic compositions should
be specified like (C2H4)213NaCl(H2O)5 and not (C2H4)n(H2O)x because we don't know what n and x are... Estimates are 
good enough if you don't know precisely. 

The same holds for density esimates. Don't write a range (1.4 - 1.6) or (~1.2), because this cannot be interpreted. 
Stick to a single representative value when you can. Again, use a reasonable estimate.

## Usage

```bash
usage: __main__.py [-h] [-v] [--log_file LOG_FILE] [-V] [-c]
                   logbook_file protocols_directory project_base_path output_script_file

Logbook to Measurement Script Generator

positional arguments:
  logbook_file         Path to the logbook Excel file
  protocols_directory  Path to the directory containing protocol files
  project_base_path    Path to the base project directory (i.e. from where you have the project
                       sheets organized by [year]/[proposalid].xlsx)
  output_script_file   Path to save the generated measurement script to

options:
  -h, --help           show this help message and exit
  -v, --verbosity      Increase output verbosity (e.g., -v for INFO, -vv for DEBUG)
  --log_file LOG_FILE  Path to the optional logging output file
  -V, --validate       Validate the generated script before execution
  -c, --collate        Collate the measurements by configuration
```

Example with test spreadsheets:
```bash
python -m logbook2mouse logbook/Logbook_MOUSE.xlsx protocols tests/testdata/projects test_script.py
```

### the `--collate` option

When `--collate` is one of the command-line arguments `logbook2mouse`
sorts the measurements by configuration. This option saves motor
movements. 

Note that this option will finish all measurements at each
configuration before moving to the next, even if their series date is
different. 

For in-situ measurements avoid this option to proceed row by row. 

## Protocols and protocol keyword-value combinations

### the `setup.py` protocol 

The `setup` protocol is prepended to the measurement script. Its role
is to define and verify the connection to the needed EPICS PVs in the
`required_pvs` list.

Change this list to reflect your setup as needed.

### measurement protocols



## Data and configuration files

