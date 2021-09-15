#!/usr/bin/env bash

if [ ! -z "$BASH" ] && [ ! -z "$BASH_SOURCE" ];
then
    scriptname="${BASH_SOURCE}";
elif  [ ! -z "${ZSH_NAME}" ] && [ ! -z "${(%):-%N}" ];
then
    scriptname="${(%):-%N}";
elif [ ! -z "$KSH_VERSION" ];
then
    scriptname="${.sh.file}"
else
    echo "Unsupported shell detected. Try: bash, zsh or ksh."
    return 1;
fi

SCRIPT_PATH=$(cd -- $(dirname "${scriptname}") && pwd)

{% if cookiecutter.use_conda == 'y' -%}

CONDABIN=${SCRIPT_PATH}/env/miniconda/bin
CONDAACTIVATE=${CONDABIN}/activate
CONDA=${CONDABIN}/mamba

# If conda is not installed, download miniconda
if ! command -v ${CONDA} &> /dev/null
then
    echo "conda not found at ${CONDA}"
    echo "script path is ${SCRIPT_PATH}"
    {{ cookiecutter.project_slug.upper() }}MINICONDA=${SCRIPT_PATH}/env/miniconda
    if [ ! -d "${{ cookiecutter.project_slug.upper() }}MINICONDA" ]
    then
        mkdir -p ${SCRIPT_PATH}/env
        cd ${SCRIPT_PATH}
        echo "Downloading miniconda..."
        case "$(uname -s)" in
            Darwin*)    OSKIND=MacOSX;;
            *)          OSKIND=Linux;;
        esac
        echo "Detected OS = ${OSKIND}"
        wget https://repo.continuum.io/miniconda/Miniconda3-latest-${OSKIND}-x86_64.sh -nv -O ${SCRIPT_PATH}/miniconda.sh \
        && bash ${SCRIPT_PATH}/miniconda.sh -b -p ${{ cookiecutter.project_slug.upper() }}MINICONDA \
        && . ${{ cookiecutter.project_slug.upper() }}MINICONDA/bin/activate \
        && conda config --set always_yes yes \
        && conda config --set env_prompt '({name}) ' \
        && conda update -q conda \
        && conda install mamba -c conda-forge \
        && rm miniconda.sh
    fi
    . ${{ cookiecutter.project_slug.upper() }}MINICONDA/bin/activate
    if ! command -v ${CONDA} &> /dev/null
    then
        echo "ERROR: cannot find conda command!"
        return 1
    fi
fi

# If environment does not exist, create it
{{ cookiecutter.project_slug.upper() }}CONDAENV=${SCRIPT_PATH}/env/{{ cookiecutter.project_slug.lower() }}
if [ ! -d "${{ cookiecutter.project_slug.upper() }}CONDAENV" ]
then 
    ${CONDA} env create -f environment.yml --prefix ${{ cookiecutter.project_slug.upper() }}CONDAENV
fi

# Activate the environment
. ${CONDAACTIVATE}
. activate ${{ cookiecutter.project_slug.upper() }}CONDAENV

# end setup-environment.
{% else -%}
if [ ! -d "${SCRIPT_PATH}/env" ]; 
then
    command -v python3 >/dev/null 2>&1 && PYTHONCMD=python3 || PYTHONCMD=python;
    ${PYTHONCMD} -m venv --prompt {{ cookiecutter.project_name.lower() }} ${SCRIPT_PATH}/env \
    && . ${SCRIPT_PATH}/env/bin/activate \
    && python -m pip install --upgrade pip \
    && python -m pip install poetry pre-commit
fi
. ${SCRIPT_PATH}/env/bin/activate
{% endif %}

export PATH=${SCRIPT_PATH}/bin:${PATH}

# Install pre-commit hooks if they have not already been installed
if test -d "${SCRIPT_PATH}/.git" && ! test -f "${SCRIPT_PATH}/.git/hooks/pre-commit";
then
    (cd ${SCRIPT_PATH}; pre-commit install)
fi