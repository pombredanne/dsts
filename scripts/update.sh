#! /bin/bash

# Reads requirements file and updates prerequisite packages to newer versions

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
parent_dir="$(dirname "$dir")"

# Install dev requirements
pip install --upgrade -r ${parent_dir}/etc/requirements.txt # Install dev requirements

