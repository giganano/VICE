
Installing VICE 
+++++++++++++++

Binary installers of the latest version of VICE for python versions 3.5-3.8 
on Mac OS X and Linux operating systems can be found on PyPI_. We recommend 
that VICE be installed in this manner by running ``pip install vice [--user]`` 
from a bash terminal. Users should add the ``--user`` flag if they do not have 
administrator privileges; this will install VICE to their ``~/.local`` 
directory. 

.. _PyPI: https://pypi.org/project/vice/ 

Designed for Unix system architectures, VICE does not function within a 
windows environment. Windows users should therefore install VICE within the 
`Windows Subsystem for Linux (WSL)`__. An `installation from source`__ on a 
windows machine should also be ran from within WSL. 

__ WSL_ 
__ `Installing from Source`_ 
.. _WSL: https://docs.microsoft.com/en-us/windows/wsl/install-win10 


Users who have or would like to modify VICE's source code should conduct a 
`from source installation`__; this also applies to users who would like to 
install for a development version of python, such as 3.9. Installing from 
source is also an alternative in the event that the PyPI_ installation fails 
for some reason. If you have already installed VICE and would like help 
getting started, usage guidelines and tutorials can be found 
`here`__. 

__ `Installing from Source`_ 
__ usage_ 
.. _usage: https://github.com/giganano/VICE/blob/master/docs/src/getting_started.rst

.. Contents:: 

Dependencies 
============
VICE has no *primary* runtime dependencies; that is, it does not require any 
external software to run properly. There are however a handful of features 
which are enabled when certain dependencies are satisfied, and we recommend 
users install them to make use of VICE to its full extent. These *secondary* 
dependencies are as follows: 

1. dill_ >= 0.2.0 
	dill_ allows VICE to save python functions with its output. This makes it 
	possible to reconstruct simulations from their output. 

2. matplotlib_ >= 2.0.0 
	matplotlib_ is necessary for the ``show`` function of the ``output`` 
	object. This is intended to allow users to visually inspect the results of 
	their simulations in ``ipython``, a ``jupyter notebook``, or something 
	similar without having to plot it themselves. This is included purely for 
	convenience, and is not intended to produce publication-quality figures. 

3. NumPy_ 
	VICE's tutorial_ and example code often make use of NumPy_, but the user 
	does not need NumPy_ to use VICE. 

.. _dill: https://pypi.org/project/dill/ 
.. _matplotlib: https://pypi.org/project/matplotlib/ 
.. _NumPy: https://pypi.org/project/numpy/ 
.. _tutorial: https://github.com/giganano/VICE/blob/master/examples/QuickStartTutorial.ipynb

A Note on Implementation 
------------------------
VICE is implemented in ANSI/ISO C and is wrapped using only standard library 
Python_ and Cython_. It is thus independent of the user's version of Anaconda_ 
(or lackthereof). It is numpy_- and pandas_-compatible, but neither numpy_- 
nor pandas_-dependent. That is, it will recognized user input from both numpy_ 
and pandas_ data types such as the numpy_ array or the pandas_ dataframe, but 
is designed to run independently of them. 

.. _Anaconda: https://www.anaconda.com/ 
.. _pandas: https://pypi.org/project/pandas/ 


Installing from Source  
======================
While VICE does not have any primary runtime dependencies, there are several 
compile-time dependencies that must be satisfied to install from source. They 
are as follows: 

1. Cython_ >= 0.28.0 

2. Python_ >= 3.5 

3. Make_ >= 3.81 

4. gcc_ >= 4.6 or clang_ >= 3.6.0 

On Mac OS X and Linux architectures, it is likely that Make_ and one of gcc_ 
or clang_ come pre-installed. Users may install with alternative C compilers 
if they so choose, but VICE is tested with only gcc_ and clang_. 

.. _Cython: https://pypi.org/project/Cython/ 
.. _Python: https://www.python.org/downloads/ 
.. _Make: https://www.gnu.org/software/make/ 
.. _gcc: https://gcc.gnu.org/ 
.. _clang: https://clang.llvm.org/get_started.html 

Once the build dependencies are satisfied, download the source code 
using a terminal and change directories into the source tree: 

:: 

	$ git clone https://github.com/giganano/VICE.git 
	$ cd VICE 

To install VICE, then run: 

:: 

	$ make 
	$ python setup.py build -j 4 install 

This will compile VICE on 4 CPUs in parallel and subsequently install. Users 
installing VICE on a system on which they do not have adminstrator's 
privileges should perform a local installation. This can be achieved with the 
``--user`` command-line argument: 

:: 

	$ python setup.py build -j 4 install --user 

Please note that users installing VICE to multiple versions of python will 
likely have to run ``make clean`` between runs of the setup.py file. 
Following the installation, to run the tests and clean the source tree: 

:: 

	$ make tests 
	$ make clean 

Please also note that ``make tests`` runs VICE's tests in the user's default 
version of python. To force the tests to run in python 3, run 
``make tests3``. Alternatively, the tests can be ran from within python 
itself: 

.. code:: python 

	import vice 
	vice.test() 

If you have issues installing or running VICE, please see the section on 
`Troubleshooting Your Build`_. If your installation was successful and you 
would like help getting started, usage guidelines can be found `here`__. 

__ usage_ 


Things to Avoid 
---------------

.. _condanote: 

1. conda Environments
	VICE should **never** be installed from source within a conda environment. 
	This only applies to from source installations; a binary installation from 
	PyPI_ should run properly within any conda environment provided the 
	version of python is supported. When installing from source in a conda 
	environment, the installation process will run without errors, but the 
	compiled extensions are not placed in the correct directory, preventing 
	VICE from running properly. This does not apply to the default environment 
	``base`` associated with later versions of python and Anaconda_. 

	VICE will *run* within whatever conda environments users create; it is only 
	the source installation process that this applies to. As noted `here`__, 
	VICE is implemented entirely independently of Anaconda_, and for this 
	reason, it does not make sense to install VICE from source in a conda 
	environment anyway. This is also true for installing from PyPI_ in a 
	conda environment, unless a specific version of python is required. 

	__ `A Note on Implementation`_ 

.. _parallelnote: 

2. Parallel Installations 
	Users installing VICE to multiple versions of python should not run the 
	setup.py file in separate terminals simultaneously; this will cause one of 
	the builds to fail. Likewise, users should not run the tests for multiple 
	versions of python simultaneously; it's likely this will caues a 
	``segmentation fault``. 


Additional Options 
------------------
By default, VICE will install verbosely, printing to the console. To turn this 
off, run a quiet installation: 

:: 

	$ python setup.py build -j 4 install -q 

or 

:: 

	$ python setup.py build -j 4 install --quiet 

To change the number of cores used to compile VICE: 

:: 

	$ python setup.py build -j <number of cores> install 

If you have modified VICE's source code and are reinstalling your modified 
version, there's no need to rebuild the entire package. Any number of 
extensions can be specified with the ``ext`` directive. For example, the 
following will rebuild the singlezone object, whose extension is 
``vice.core.singlezone._singlezone``: 

:: 

	$ python setup.py build install ext=vice.core.singlezone._singlezone 


Troubleshooting Your Build 
==========================
The following are a number of issues that can arise when installing VICE from 
source. If none of these options solve your problem, you may open an issue 
`here`__, or email VICE's primary author (James W. Johnson) at 
giganano9@gmail.com. 

__ issues_ 

ImportError After Installation 
------------------------------
`Did you install VICE from within a conda environment?`__ If not, please 
open an issue `here`__. 

__ condanote_ 
.. _issues: https://github.com/giganano/VICE/issues 
__ issues_ 


Running the setup.py File Failed
--------------------------------
`Did you run it for multiple versions of python simultaneously?`__ If not, 
please open an issue `here`__. 

__ parallelnote_ 
__ issues_ 


Running the Tests Resulted in a Segmentation Fault 
--------------------------------------------------
`Did you run the tests for multiple versions of python simultaneously?`__ 
If not, please open an issue `here`__. 

__ parallelnote_ 
__ issues_ 


VICE Isn't Running from the Command Line 
----------------------------------------
In this case, it is likely that the required files were copied somewhere that 
is not on your PATH. If re-installing VICE does not solve the problem, 
these files can simply be copied to a given directory. For example: 

:: 

	$ cp ./bin/* ~/.local/bin/ 

Will place both command line entries in the ``~/.local/bin/`` directory. This 
can be permanently added to your path by adding 

:: 

	export PATH=$HOME/.local/bin:$PATH 

to ``~/.bash_profile``. This will require ``source ~/.bash_profile`` to be 
ran from the terminal before ``vice`` can be ran from the 
command line. 

**Note**: If you have installed VICE with the ``--user`` option, it is likely 
that VICE has automatically modified your PATH, and that 
``source ~/.bash_profile`` is all that needs ran. 

More information on modifying your PATH can be found `here`__. 

If this does not fix the issue, please open an issue `here`__. 

.. _pathvariables: https://unix.stackexchange.com/questions/26047/how-to-correctly-add-a-path-to-path
__ pathvariables_ 
__ issues_ 


Compiler Failure 
----------------
This is usually an indication that the build should not be ran on multiple 
cores. First run ``make clean``, and subsequently ``make``. Then replace your 
previous command to run the setup.py file with: 

:: 

	$ python setup.py build install [--user] [--quiet] 

If you were not installing VICE on multiple cores to begin with, try 
installing without the ``build`` directive: 

:: 

	$ python setup.py install [--user] [--quiet] 

If neither of these recommendations fixed your problem, please open an 
issue `here`__. 

__ issues_ 

Uninstalling VICE 
=================
If you have installed VICE from PyPI_, it can be uninstalled from the terminal 
via ``pip uninstall vice``. When prompted, simply confirm that you would like 
the files removed. 

If you have installed from source, uninstalling requires a couple of steps. 
First, you must find the path to the directory that it was installed to. This 
can be done by launching python and running the following two lines: 

.. code:: python 

	import vice 
	print(vice.__path__) 

Note that there are *four* underscores in total: two each before and after 
``path``. This will print a single-element list containing a string denoting 
the name of the directory holding VICE's compiled extensions, of the format 
``/path/to/install/dir/vice``. Change into this directory, and remove the 
VICE tree: 

:: 

	$ cd /path/to/install/dir/ 
	$ rm -rf vice/ 

Then, check the remaining contents for an ``egg``. This will likely be of the 
format ``vice-<version number>.egg-info``. Remove this file as well: 

:: 

	$ rm -f vice-<version number>.egg-info 

Finally, the command line entry must be removed. The full path to this script 
can be found with the ``which`` command in the terminal: 

:: 

	$ which vice 

This will print the full path in the format ``/path/to/cmdline/entry/vice``. 
Pass it to the ``rm`` command as well: 

:: 

	$ rm -f /path/to/cmdline/entry/vice 

If this process completed without any errors, then VICE was successfully 
uninstalled. To double-check, rerunning ``which vice`` should now print 
nothing. 

