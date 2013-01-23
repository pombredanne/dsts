Development HOWTO
=================

Installing the package
----------------------

To install the library on the system, run:

    $ sudo python setup.py install

Using the package
-----------------

The following example illustrates to instantiate a suffix array from supplied string and store it in a string:

    >>> from dsts.suffix_array import SuffixArray
    >>> sarray = SuffixArray('memory', string='abcd5abc15abc')
    >>> print sarray.return_array_as_string()  # Print sorted array
    0 15abc
    1 5abc
    2 5abc15abc
    3 abc
    4 abc15abc
    5 abcd5abc15abc
    6 bc
    7 bc15abc
    8 bcd5abc15abc
    9 c
    10 c15abc
    11 cd5abc15abc
    12 d5abc15abc
    >>> sarray.return_lcp_array()  # Print LCP array
    [-1, 0, 4, 0, 3, 0, 0, 2, 0, 0, 1, 0, 0]

The suffix array can be searched as follows:

    >>> print sarray.search('abcd5')  # Return position of 'abcd5' substring
    >>> print sarray.search('abc15')  # Return position of 'abc15' substring

This returns the first instance found. All instances of the substring in the string can be found as follows:
    
    >>> print sarray.search_all('abc')  # Return all positions of 'abc'
    [10, 5, 0]

Examples illustrating how to identify repeating strings:

    >>> sarray.get_duplicates()
    []
    >>> sarray.find_all_duplicates()
    >>> sarray.get_duplicates()  # Get duplicates substrings (default length >= 2)
    [(u'5a', 4), (u'5a', 9), (u'5ab', 4), (u'5ab', 9), (u'5abc', 4), (u'5abc', 9), (u'ab', 0), (u'ab', 5), (u'ab', 10), (u'abc', 0), (u'abc', 5), (u'abc', 10), (u'bc', 1), (u'bc', 6), (u'bc', 11)]
    >>> sarray.ds.wipe_duplicates()
    >>> sarray.find_all_duplicates(min_length=3)
    >>> sarray.get_duplicates()
    [(u'5ab', 4), (u'5ab', 9), (u'5abc', 4), (u'5abc', 9), (u'abc', 0), (u'abc', 5), (u'abc', 10)]

Installing the development environment
--------------------------------------

The code comes with an installation script that setups an development environment allowing further changes to be made to the code or to run additional tests. This installation script automatically downloads and installs the necessary packages. The development environment is installed within a python virtual environment, which means it will not install any global packages and perform changes affecting the machine's python intrepretter.

After cloning the repository the development environment can be installed byrunning the following:

    $ scripts/install_dev_env.sh

The installation script requires virtualenv to be installed. 

This will create a symbolic link between in the lib directory pointing to the src directory. This allows one to import the data structures from a python intrepretter running in an activated virtual environment (see next session), e.g:

    >>> from dsts.suffix_array import SuffixArray

Activating the development environment
--------------------------------------

The development environment can be activated using the standard virtual environment scripts, which should have been installed when the development environment was installed, that is:

    $ source bin/activate

And to deactivate it:

    $ deactivate

Note, if you want to install the library outside the virtual environment using "python setup.py install" make sure to first deactivate the virtual environment, or run the installation command in a seperate shell.

Package management
------------------

The installation script installs the 'yolk' utility that can be used to query packages. If used in an activated development environment, yolk can be used to show all the packages that were installed to the environemnt by the installation script, as well as any added packages added manually by the user:

    $ yolk -l

It can also check if there are any packages that need to be upgraded as follows:

    $ yolk -U

For more instructions please check yolk's online documentation or refer to yolk's command documentationg:

    $ yolk --help

To upgrade all packages required by this package, run pip as folows:

    $ pip install --upgrade -r etc/requirements.txt

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
  * pep8 - http://www.python.org/dev/peps/pep-0008/
  * flake8 - https://bitbucket.org/tarek/flake8
  * pyflakes - https://launchpad.net/pyflakes
  * pylint - http://www.logilab.org/857
