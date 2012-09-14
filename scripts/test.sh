#! /bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
root_dir="$(dirname "$script_dir")"   # Package root dir

echo
echo Staging the files:
echo ------------------
cd $root_dir
python setup.py install
echo
echo Running testing suit:
echo ---------------------
nosetests -v --with-coverage --cover-tests
