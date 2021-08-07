#!/usr/bin/env bash

if [ ! -z "$BASH" ] && [ ! -z "$BASH_SOURCE" ];
then
    scriptname="${BASH_SOURCE}";
elif  [ ! -z "${ZSH_NAME}" ] && [ ! -z "${(%):-%N}" ];
then
    scriptname="${(%):-%N}";
elif [ ! -z "${.sh.file}" ];
then
    scriptname="${.sh.file}"
else
    scriptname="${0}"
fi

SCRIPT_PATH=$(cd -- $(dirname "${scriptname}") && pwd)

if [ ! -d "${SCRIPT_PATH}/env" ]; 
then
    command -v python3 >/dev/null 2>&1 && PYTHONCMD=python3 || PYTHONCMD=python;
    ${PYTHONCMD} -m venv --prompt monorepo-python ${SCRIPT_PATH}/env \
    && source ${SCRIPT_PATH}/env/bin/activate \
    && python -m pip install --upgrade pip \
    && python -m pip install cookiecutter pre-commit pytest
fi

source ${SCRIPT_PATH}/env/bin/activate