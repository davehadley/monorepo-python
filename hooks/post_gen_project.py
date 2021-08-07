#!/usr/bin/env python
from pathlib import Path


def _main():
    directory = Path.cwd().resolve()
    if "{{ cookiecutter.use_conda }}" != "y":
        (directory / "environment.yml").unlink()
    return


if __name__ == "__main__":
    _main()
