#! /bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"  # Directory where this file resides, the scripts dir
root_dir="$(dirname "$script_dir")"   # Package root dir (scripts directory's parent directory)
package_name=${root_dir##*/} # Package name = package root dir
source_dir="${root_dir}/${package_name}" # Python source files location
lib_dir="${root_dir}/lib/python2.7/site-packages/${package_name}" # Virtual env's python lib dir
bin_dir="${root_dir}/bin" # Virtual env's python bin dir

# Install virtual environment
if command -v virtualenv; then 
	echo "Found virtualenv installed on system"
	virtualenv ${root_dir}
else
	echo "Error: Please install virtualenv on your system first"
	exit 1
fi

# Activate virtual environment
source ${bin_dir}/activate

# Install dev requirements
pip install -r ${root_dir}/etc/requirements.txt # Install dev requirements

# Stage the code
cd $root_dir
python setup.py develop

# If it does not exist, create symbolic link enabling pre-commit .git hook
symlink_target=${root_dir}/.git/hooks/pre-commit
if ! [ -L ${symlink_target} ]; then
	ln -s ${root_dir}/scripts/pre-commit ${symlink_target}
fi

# Clean egg-info directory created by distribute
if [ -d ${root_dir}/dsts.egg-info ]; then
	rm -rf ${root_dir}/dsts.egg-info
fi

# Deactivate virtual environment
deactivate
