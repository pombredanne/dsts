#! /bin/bash

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
parent_dir="$(dirname "$dir")"

# Install dev requirements
pip install -r ${parent_dir}/etc/requirements.txt # Install dev requirements

# Create symbolic link so testing packages can find source files
ln -s ${parent_dir}/dsts ${parent_dir}/lib/python2.7/site-packages/dsts
