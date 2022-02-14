#!/usr/bin/env python3
import re
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from subprocess import run
from typing import Callable, Iterable

_has_run_tests = False
_subpackages_directory_name = "lib"


def _main():
    args = _parseargs()
    args.func(args)


def _parseargs() -> Namespace:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(help="choose which task to run")
    for verb, func, verbhelp, extrargs, aliases in [
        ("build", _build, "Build packages", None, ["b"]),
        ("test", _test, "Test packages", None, ["t"]),
        ("install", _install, "Install packages", None, ["i"]),
        (
            "broadcast",
            _broadcast,
            "Run a command in all packages",
            _setbroadcastargs,
            ["bro"],
        ),
    ]:
        verbparser = subparsers.add_parser(verb, help=verbhelp, aliases=aliases)
        if extrargs:
            extrargs(verbparser)
        verbparser.add_argument(
            "packagename",
            nargs="*",
            type=str,
            default=None,
            help="Name of packages to include. If none set, all packages will be included.",
        )
        verbparser.set_defaults(func=func)
    return parser.parse_args()


def _test(args: Namespace) -> None:
    packagefilter = _package_filter_from_names(args.packagename)
    packages = Path(__file__).parent.parent / _subpackages_directory_name
    for packagedir in sorted(packages.iterdir()):
        if packagedir.is_dir() and packagefilter(packagedir):
            _run_poetry_tests(packagedir)
    if not _has_run_tests:
        print("No tests ran.", file=sys.stderr)
        sys.exit(1)
    return


def _build(args: Namespace) -> None:
    packagefilter = _package_filter_from_names(args.packagename)
    packages = Path(__file__).parent.parent / _subpackages_directory_name
    for packagedir in sorted(packages.iterdir()):
        if packagedir.is_dir() and packagefilter(packagedir):
            _run_poetry_build(packagedir)
    return


def _install(args: Namespace) -> None:
    packagefilter = _package_filter_from_names(args.packagename)
    packages = Path(__file__).parent.parent / _subpackages_directory_name
    for packagedir in sorted(packages.iterdir()):
        if packagedir.is_dir() and packagefilter(packagedir):
            _run_pip_install(packagedir)
    return


def _setbroadcastargs(parser: ArgumentParser) -> None:
    parser.add_argument(
        "command", help="Shell command to be run inside each sub-package.", type=str
    )
    return


def _broadcast(args: Namespace) -> None:
    packagefilter = _package_filter_from_names(args.packagename)
    packages = Path(__file__).parent.parent / _subpackages_directory_name
    for packagedir in sorted(packages.iterdir()):
        if packagedir.is_dir() and packagefilter(packagedir):
            print(f'---- Running "{args.command}" in {packagedir}')
            run(args.command, cwd=packagedir, check=True, shell=True)
    return


def _package_filter_from_names(names: Iterable[str]) -> Callable[[Path], bool]:
    patterns = list(names)

    def packagefilter(packagedir: Path) -> bool:
        if len(patterns) == 0:
            return True
        for pat in patterns:
            if re.match(pat, packagedir.name):
                return True
        return False

    return packagefilter


def _run_poetry_tests(directory: Path) -> None:
    if _is_poetry_package(directory) and (directory / "tests").exists():
        _announce_tests_running("poetry pytest", directory)
        run(["poetry", "run", "pytest", "tests"], cwd=directory, check=True)
    return


def _run_poetry_build(directory: Path) -> None:
    if _is_poetry_package(directory):
        print(f"---- Running poetry install in {directory}")
        run(["poetry", "install"], cwd=directory, check=True)
    return


def _run_pip_install(directory: Path) -> None:
    if _is_python_package(directory):
        print(f"---- Running pip install in {directory}")
        run(["pip", "install", "."], cwd=directory, check=True)
    return


def _is_poetry_package(directory: Path) -> bool:
    configfilepath = directory / "pyproject.toml"
    if configfilepath.exists():
        with open(configfilepath) as configfile:
            return "tool.poetry" in configfile.read()
    return False


def _is_python_package(directory: Path) -> bool:
    configfilepath = directory / "pyproject.toml"
    return configfilepath.exists()


def _announce_tests_running(type: str, directory: Path) -> None:
    print(f"---- Running {type} tests in {directory}")
    global _has_run_tests
    _has_run_tests = True
    return


if __name__ == "__main__":
    _main()
