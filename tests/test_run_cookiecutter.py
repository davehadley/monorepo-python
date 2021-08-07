import os
import shutil
import subprocess
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from typing import Any, Dict, Optional, Tuple

import pytest
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
        directory = _run_cookiecutter(Path(tmpdir), {"use_conda": "n"})
        templatepythondir = directory / "templates" / "python"
        examplepythondir = directory / "lib"
        assert templatepythondir.exists()
        setupscript = directory / "setup.sh"
        run(
            f"""
            . {setupscript.resolve()} \\
            && cookiecutter {templatepythondir} --output-dir {examplepythondir.resolve()} --no-input \\
            && example_monorepo_python_manage.py build \\
            && example_monorepo_python_manage.py test \\
            && example_monorepo_python_manage.py install
            """,
            check=True,
            shell=True,
            executable=shutil.which("bash"),
            cwd=tmpdir,
        )


def test_run_cookiecutter_template_packages_pass_tests():
    with TemporaryDirectory() as tmpdir:
        directory = _run_cookiecutter(Path(tmpdir), {"use_conda": "n"})
        for templatedir in (directory / "templates").iterdir():
            if templatedir.is_dir():
                run(
                    ["pytest", "tests"],
                    check=True,
                    cwd=templatedir,
                )


def test_run_cookiecutter_posix_shell_fails():
    with TemporaryDirectory() as tmpdir:
        directory = _run_cookiecutter(Path(tmpdir))
        setupscript = directory / "setup.sh"
        with pytest.raises(subprocess.CalledProcessError):
            run(
                f". {setupscript.resolve()}",
                check=True,
                shell=True,
                executable=shutil.which("dash"),
                cwd=tmpdir,
            )


# ksh does not currently work with conda (see: https://github.com/conda/conda/issues/7843)
@pytest.mark.parametrize(
    "shell_and_use_conda",
    [("bash", "n"), ("zsh", "n"), ("ksh", "n"), ("bash", "y"), ("zsh", "y")],
)
def test_run_cookiecutter_conda_and_shells(shell_and_use_conda: Tuple[str, str]):
    (shell, use_conda) = shell_and_use_conda
    with TemporaryDirectory() as tmpdir:
        directory = _run_cookiecutter(Path(tmpdir), {"use_conda": use_conda})
        assert directory.exists()
        setupscript = directory / "setup.sh"
        run(
            f". {setupscript.resolve()}",
            check=True,
            shell=True,
            executable=shutil.which(shell),
            cwd=tmpdir,
        )
