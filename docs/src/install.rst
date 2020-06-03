
Installing VICE 
+++++++++++++++

At present, VICE is not installable via ``pip``. Instructions can be found 
`here`__. If you have already installed VICE and are looking for help getting 
started, usage guidelines can be found `here`__. 

__ `Installing from Source`_ 
__ usage_ 
.. _usage: https://github.com/astrobeard/VICEdev/blob/master/USAGE.rst.txt

Dependencies 
============

Primary
-------
The following dependencies must be satisfied for VICE to install properly: 

1. Cython_ >= 0.28.0 

2. Python_ >= 3.5 

3. Make_ >= 3.81 

4. gcc_ >= 4.6 or clang_ >= 3.6.0 

On macOS and linux distributions, it is likely that Make_ and one of gcc_ or 
clang_ come pre-installed. Users may install with alternative C compilers if 
they so choose, but VICE is only tested with gcc_ and clang_. 

.. _Cython: https://pypi.org/project/Cython/ 
.. _Python: https://www.python.org/downloads/ 
.. _Make: https://www.gnu.org/software/make/ 
.. _gcc: https://gcc.gnu.org/ 
.. _clang: https://clang.llvm.org/get_started.html 

Secondary 
---------
VICE will run independently of the following, but they enable additional 
features. 

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
.. _tutorial: https://github.com/astrobeard/VICEdev/blob/master/docs/QuickStartTutorial.ipynb 


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
To install VICE from source, first download the source code using a terminal 
and change directories into the source tree: 

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

Please note that users installing VICE to multiple versions of Python_ will 
likely have to run ``make clean`` between runs of the setup.py file. 
Following the installation, to run the tests and clean the source tree: 

:: 

	$ make tests 
	$ make clean 

Please also note that ``make tests`` runs VICE's tests in the user's default 
version of Python_. To force the tests to run in Python_ 3, run 
``make tests3``. Alternatively, the tests can be ran from within Python_ 
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
	VICE should **never** be installed from within a conda environment. In 
	this case, the installation process will run without errors, but the 
	compiled extensions will not be placed in the correct directory, 
	preventing VICE from running properly. This does not apply to the default 
	environment ``base`` associated with later versions of Python_ and 
	Anaconda_. 

	VICE will *run* within whatever conda environments users create; it is only 
	the installation process that this applies to. As noted `here`__, VICE is 
	implemented entirely independently of Anaconda_, and for this reason, it 
	does not make sense to install VICE in a conda environment anyway. 

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
ran from the terminal before ``vice`` or ``vice-docs`` can be ran from the 
command line. 

**Note**: If you have installed VICE with the ``--user`` option, it is likely 
that VICE has automatically modified your PATH, and that 
``source ~/.bash_profile`` is all that needs ran. 

**Note**: This applies to both ``vice`` and ``vice-docs`` command line entries. 

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

