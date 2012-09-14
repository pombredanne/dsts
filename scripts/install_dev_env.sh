#! /bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
root_dir="$(dirname "$script_dir")"   # Package root dir 
package_name=${root_dir##*/} # Package name = package root dir
source_dir="${root_dir}/${package_name}" # Python source files location
lib_dir="${root_dir}/lib/python2.7/site-packages/${package_name}" # Virtual env's python lib dir
bin_dir="${root_dir}/bin" # Virtual env's python bin dir

# Install virtual environment
virtualenv ${root_dir}

# Activate virtual environment
source ${bin_dir}/activate

# Install dev requirements
pip install -r ${root_dir}/etc/requirements.txt # Install dev requirements

# Stage the code
cd $root_dir
python setup.py install

# Deactivate virtual environment
deactivate
