#! /bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
root_dir="$(dirname "$script_dir")"   # Package root dir 
package_name=${parent_dir##*/} # Package name = package root dir
source_dir= ${parent_dir}/${package_name} # Python source files location

# Install virtual environment
virtualenv --no-site-packages ${root_dir}

# Activate virtual environment
source ${root_dir}/bin/activate

# Install dev requirements
pip install -r ${root_dir}/etc/requirements.txt # Install dev requirements

# Create symbolic link so testing packages can find source files
ln -s ${source_dir} ${root_dir}/lib/python2.7/site-packages/${package_name}

# Deactivate virtual environment
deactivate
