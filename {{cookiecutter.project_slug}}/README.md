# {{cookiecutter.project_name}}

## Environment Setup

Run `source setup.sh` to setup the development environment.
This may be slow the first time that this is run as the virtual environment is created
and dependencies are installed.

## Creating an New Library

New packages are created with the cookiecutter templates in the templates directory.
For example, to create a new python package,
```
cd lib && cookiecutter ../templates/python
```

Local dependencies may be added with `poetry add --dev ../<dependency_package_name>`
from the within the package directory.

## Build and Test

Build all packages with:

```
{{cookiecutter.project_slug}}_manage.py build
```

Run all package tests with:

```
{{cookiecutter.project_slug}}_manage.py test
```

To run an arbitrary shell command inside each sub-package run:

```
{{cookiecutter.project_slug}}_manage.py broadcast "echo Your shell command"
```

See `{{cookiecutter.project_slug}}_manage.py --help` for more information. 