# monorepo-python

[![Main Build status](https://img.shields.io/github/workflow/status/davehadley/monorepo-python/ci/main?label=main)](https://github.com/davehadley/monorepo-python/tree/main)
[![Develop Build status](https://img.shields.io/github/workflow/status/davehadley/monorepo-python/ci/develop?label=develop)](https://github.com/davehadley/monorepo-python/tree/develop)
[![Last commit](https://img.shields.io/github/last-commit/davehadley/monorepo-python/develop)](https://github.com/davehadley/monorepo-python/tree/develop)

A [cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a 
monorepo containing several python packages. This repository structure is partially inspired by this [medium post](https://medium.com/opendoor-labs/our-python-monorepo-d34028f2b6fa).

## Usage

To use, install cookiecutter if you have not done so already,
```
pip install -U cookiecutter
```

Then:
```
cookiecutter https://www.github.com/davehadley/monorepo-python
```

## Package Structure

The generated package contains the following directories/files:
- `setup.sh` : a setup script to run before starting development. It handles creation of a python virtual environment.
- `bin/` : added to the path by the setup script and is a place to store scripts needed by all sub-packages.
- `bin/{{cookiecutter.project_slug}}.manage.py` : a script that runs build and test operations on all sub-packages.
- `lib/` : sub-packages of this mono-repo go in here.
- `templates/` : contains cookie-cutter templates used to generate new packages inside `lib/`.

See the inner [README.md](./{{cookiecutter.project_slug}}/README.md) for additional information.

## Testing this cookie cutter template

Tests are run with pytest. From the root directory of the package run:
```
source setup.sh && pytest tests
```

## Known Issues

### Language Settings on CentOS 7

On CentOS 7, when running the initial cookiecutter command you may run into an error:
```
RuntimeError: Click will abort further execution because Python was configured to use ASCII as encoding for the environment. Consult https://click.palletsprojects.com/unicode-support/ for mitigation steps.
``` 

To resolve this, check that your `LANG` and `LC_ALL` environment variables are set to
valid values. You can list the valid values with `locale -a`.

For example, setting LANG to:
```
export LANG=en_US.utf8
```
may solve the problem.
