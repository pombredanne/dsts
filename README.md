Development HOWTO
=================

Installing the package
----------------------

To install the library on the system, run:

sudo python setup.py install

Installing the development environment
--------------------------------------

The code comes with an installation script that setups an development environment allowing further changes to be made to the code or to run additional tests. This installation script automatically downloads and installs the necessary packages. The development environment is installed within a python virtual environment, which means it will not install any global packages and perform changes affecting the machine's python intrepretter.

After cloning the repository the development environment can be installed byrunning the following:

$ scripts/install_dev_env.sh

The installation script requires virtualenv to be installed. 

This will create a symbolic link between in the lib directory pointing to the src directory. This allows one to import the data structures from a python intrepretter running in an activated virtual environment, e.g:

"from dsts.suffix_array import SuffixArray"

Activating the development environment
--------------------------------------

The development environment can be activated using the standard virtual environment scripts, which should have been installed when the development environment was installed, that is:

$ source bin/activate

And to deactivate it:

$ deactivate

Note, if you want to install the library outside the virtual environment using "python setup.py install" make sure to first deactivate the virtual environment, or run the installation command in a seperate shell.

Running the test suit
---------------------

Once the development environment has been installed one can run a test suit on the suffix array. The test suit relies on the nosetest framework which should have been installed by the installation script.

To run tests:

$ nosetests

Also, nosetests can be used to show the tested coverage of the code. The coverage package is also installed automatically in the virtual environment by the installation script.

$nosetests --with-coverage

For more verbosity, showing the tests:

$nosetests -v --with-coverage

See notetest for more information (http://nose.readthedocs.org/en/latest/).

In order to test the latest code, one needs to stage it in the virtual environment lib/ directory. This can be done by running "python setup.py install" (without sudo), while the environment is activated. To save having to stage the code everytime one needs to run the tests, the following testing script can be used:

$scripts/test.sh

Pep8, flake8, pyflakes, pylint compliance
---------------------------------

In order to insure good quality code in this package, a number of code compliance and analysis packages are used. 

There is a git pre-commit hook in the script directory. The installation of the virtual environment enables this hook by making a symbolic link to the .git directory. This script checks stages files for PEP8 compliance before commiting staged files.

One of the scripts can be used to check for pep8 and pyflakes (using the flake8) compliance:

$scripts/check.sh

In addition the installation script also installed the pylint package, which also can be used to improve the code.

More information can be found regarding the packages can be found here:
pep8 - http://www.python.org/dev/peps/pep-0008/
flake8 - https://bitbucket.org/tarek/flake8
pyflakes - https://launchpad.net/pyflakes
pylint - http://www.logilab.org/857
