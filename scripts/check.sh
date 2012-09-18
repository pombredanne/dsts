# Script checks for pep8 and pyflakes compliance

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
root_dir="$(dirname "$script_dir")"  # Package root dir 
package_name=${root_dir##*/} # Package name = package root dir
source_dir="${root_dir}/${package_name}" # Python source files location
tests_dir="${root_dir}/tests" # Additional python source files location for tests

# PEP8 ignore WARNINGS
ignore="E501"  # Ignore 80 character line limit

flake8 ${source_dir} ${tests_dir} --ignore=${ignore}
