import os
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from typing import Any, Dict, Optional

from cookiecutter.main import cookiecutter

_project_path = Path(__file__).parent.parent.resolve()


def _run_cookiecutter(
    cwd: Path, extra_context: Optional[Dict[str, Any]] = None
) -> Path:
    initial = Path.cwd()
    try:
        os.chdir(cwd)
        outputdir = cookiecutter(
            str(_project_path), no_input=True, extra_context=extra_context
        )
        return Path(outputdir)
    finally:
        os.chdir(initial)


def test_run_cookiecutter_python_template():
    with TemporaryDirectory() as tmpdir:
        directory = _run_cookiecutter(Path(tmpdir))
        # import pdb; pdb.set_trace();
        run(
            ["poetry", "install"],
            check=True,
            cwd=directory,
        )
        run(
            ["poetry", "run", "pytest", "tests"],
            check=True,
            cwd=directory,
        )
