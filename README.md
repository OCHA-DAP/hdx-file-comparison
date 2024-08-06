# HDX File Comparison

## Overview

This is proof of concept code to check tabular data files for changes at the cell level.
In addition it also includes code to compare outputs from two different instances of HDX HAPI.


## Installation

## Usage

```shell
Usage: hdx-compare [OPTIONS] COMMAND [ARGS]...

  Tools for comparing files from HAPI and HDX

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  compare   Compare files
  download  Download HDX HAPI responses as CSV files
  process   Download and compare files from the hapi and hapi-temporary...
```

## Contributions

For developers the code should be cloned installed from the [GitHub repo](https://github.com/OCHA-DAP/hdx-file-comparison), and a virtual enviroment created:

```shell
python -m venv venv
source venv/Scripts/activate
```

And then an editable installation created:

```shell
pip install -e .
```

New features should be developed against a GitHub issue on a separate branch with a name starting `GH[issue number]_`. `PULL_REQUEST_TEMPLATE.md` should be used in preparing pull requests. Versioning is updated manually in `pyproject.toml` and is described in the template, in brief it is CalVer `YYYY.MM.Micro`.

## Publication

Publication to PyPI is done automatically when a release is created.
