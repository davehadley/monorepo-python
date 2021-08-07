# {{cookiecutter.project_name}}

## Environment Setup

Run `source setup.sh`.

## Creating an New Package

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
cookiecutter.slug_name_manage.py build
```

Run all package tests with:

```
{{cookiecutter.project_slug}}_manage.py test
```

See `{{cookiecutter.project_slug}}_manage.py --help` for more information. 

## Development Instructions

Please run `pre-commit install` before starting any development work.
