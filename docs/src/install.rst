
.. _install:

Installing VICE
+++++++++++++++

On PyPI_ we provide pre-compiled binary installers and source distributions for
released versions of VICE.
To install the latest version, we recommend simply running

::

	$ python -m pip install vice [--user]

from the command line.
Users should add the ``--user`` flag if they do not have administrative
privileges on their current machine; this will install VICE to their
``~/.local`` directory.
To compile and install VICE from source using PyPI_, simply specify that you
do not want to use the binary using the ``--no-binary`` flag:

::

	$ python -m pip install vice [--user] --no-binary :all:


The option ``:all:`` above tells ``pip`` to install all of the packages in the
current call to ``pip install`` without binaries; when installing multiple
packages, this value can be specified as a comma-separated list.
Further details on the ``--no-binary`` option can be found in the associated
`documentation`__ for the ``pip install`` command.
Rather than downloading a pre-compiled binary, ``pip`` will download the source
distribution provided on PyPI_ and compile and install VICE on your machine.
``pip`` should also conduct an installation using the source distribution
automatically in the event that a pre-compiled binary is unavailable for a
user's operating system and CPU architecture.

__ pipinstalldocs_
.. _pipinstalldocs: https://pip.pypa.io/en/stable/cli/pip_install/
.. _PyPI: https://pypi.org/project/vice/

Additionally, previous versions available on PyPI can be installed by simply
specifying the version number:

::

	$ python -m pip install vice==<version number> [...]

Designed for systems with a Unix kernel, VICE does not function within a
windows environment.
Windows users should therefore install VICE within the
`Windows Subsystem for Linux (WSL)`__.
Provided that the call to ``pip`` is ran from within WSL, the pre-compiled
binary installer from PyPI_ should install VICE properly.
A `manual installation`__ on a windows machine must also be ran within
WSL.

__ WSL_
__ `Manual Installation`_
.. _WSL: https://docs.microsoft.com/en-us/windows/wsl/install-win10

For the current version, we provide pre-compiled binaries for Python_ versions
3.6-3.10 on computers with an x86_64 CPU architecture running Mac OS and Linux
operating systems.
We do not provide pre-compiled binaries for CPU architectures other than x86_64.
This includes Linux computers with Aarch64 hardware as well as the new ARM64
Apple Silicon computers (i.e. the M1 chip).
At present, the developers do not have the resources necessary to pre-compile
VICE for these machines, we apologize for the inconvenience.
Although VICE can be installed and ran on 32-bit hardware (e.g. i686 CPUs), we
strongly discourage running VICE on such machines.

Users who have or would like to modify VICE's source code must conduct a
`manual installation`__.
This also applies to users who would like to install a version of VICE that
is still under development (these can be found on various branches of its
`GitHub repository`__) as well as for versions of python still under
development.

__ `Manual Installation`_
__ repo_
.. _repo: https://github.com/giganano/VICE.git

Although it is generally not advised to mix package managers, this is not a
concern for VICE.
At present, a pre-compiled installation of VICE is not available through
conda_, though users who typically install their python packages and manage
their computing environments with conda_ can safely conduct their installation
of VICE using ``pip``.
`As noted below`__, VICE has no run-time dependencies, meaning that there is
no environment that would need solved in the event the installation were
conducted using conda_.
In this case, the package manager would simply see that the list of
dependencies is empty, then download the pre-compiled binary and install it.

__ `Dependencies`_
.. _conda: https://docs.conda.io/en/latest/

If you have already installed VICE and would like help getting started, we
recommend checking out VICE's tutorial_.
Further usage guidelines can be found :ref:`here <getting_started>`.

.. _tutorial: https://github.com/giganano/VICE/blob/main/examples/QuickStartTutorial.ipynb

.. Contents::

Dependencies
============
VICE has no *primary* run-time dependencies; that is, it does not require any
external software to run properly.
All that is required to run VICE is python itself.
There are however a handful of features which are enabled when certain
dependencies are satisfied, and we recommend users install them to make use of
VICE to its full extent.
These *secondary* dependencies are as follows:

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

A Note on Implementation
------------------------
VICE is implemented in ANSI/ISO C and is wrapped using only standard library
Python_ and Cython_. It is thus independent of the user's version of Anaconda_
(or lackthereof). It is NumPy_- and pandas_-compatible, but neither NumPy_-
nor pandas_-dependent. That is, it will recognize user input from both NumPy_
and pandas_ data types such as the NumPy_ array or the pandas_ dataframe, but
is designed to run independently of them.

.. _Anaconda: https://www.anaconda.com/
.. _pandas: https://pypi.org/project/pandas/


Manual Installation
===================
Users who have modified VICE's source code must compile and install their
updated version manually.
Otherwise, we recommend simply making use of ``pip`` as described above.
If you have already modified VICE's source code or plan to do so, we encourage
you to reach out to one of our :ref:`developers <contributors>` - we'd be happy
to consult with you to help VICE meet your needs!

While VICE does not have any primary run-time dependencies, there are a few
common compile-time dependencies that must be satisfied to install from source.
They are as follows:

1. Python_ >= 3.6

2. setuptools_ >= 18.0

3. Make_ >= 3.81

4. gcc_ >= 4.6 or clang_ >= 3.6.0

On Mac OS X and Linux architectures, it is likely that Make_ and one of gcc_
or clang_ come pre-installed. Users may install with alternative C compilers
if they so choose, but VICE is tested with only gcc_ and clang_.
While a sizable portion of VICE's source code is written in Cython_ and
requires Cython_ >= 0.29.0 to compile, this should be handled automatically by
setuptools_.
Nonetheless, it is always an easy option to install it manually via
``python -m pip install Cython>=0.29.0``.

.. _Cython: https://pypi.org/project/Cython/
.. _Python: https://www.python.org/downloads/
.. _Make: https://www.gnu.org/software/make/
.. _gcc: https://gcc.gnu.org/
.. _clang: https://clang.llvm.org/get_started.html
.. _setuptools: https://setuptools.readthedocs.io/en/latest/

Once the build dependencies are satisfied, download the source code
using a terminal and change directories into the source tree:

::

	$ git clone https://github.com/giganano/VICE.git
	$ cd VICE

From here, users may change to a specific branch if necessary.
For example, VICE's latest development version is on a branch named
``development``, and ``git checkout development`` will take you there.
To then compile and install VICE, simply run:

::

	$ make
	$ python setup.py build install [--user]

This will compile the source code under a directory named ``build``, and
subsequently install to the appropriate ``site-packages`` directory once
completed.
Users who do not have administrator's privileges on the system they're
conducting the installation should add the ``--user`` command-line argument,
which will conduct a local installation.

Following the installation, running VICE's unit tests (if desired) and
cleaning the source tree can be achieved with

::

	$ make tests
	$ make clean

Please note that users installing VICE to multiple versions of python will
likely have to run ``make clean`` between runs of the setup.py file.
The command ``make tests`` runs the unit tests in the current environment's
default version of python.
If a specific version of python is required, the tests can be ran from
within the interpreter itself easily:

.. code:: python

	import vice
	vice.test()

If you have issues installing or running VICE, please see the section on
`Troubleshooting Your Build`_. If your installation was successful and you
would like help getting started, usage guidelines can be found
:ref:`here <getting_started>`.


Additional Compile Options
--------------------------
VICE affords users flexibility in specifying how they'd like to compile from
source.

1. Parallelization
	Users may spread out the job of compiling VICE across multiple cores via
	the ``[-j N]`` command-line argument.
	For example,

	::

		$ python setup.py build -j 2 install [--user]

	will compile all extensions using 2 cores.
	**Warning**: See `note`__ below regarding parallel installations with the
	gcc_ C compiler.

__ gcc_parallel_note_

2. Suppress verbose output
	Users may suppress the printing of compiler commands to the consoler with
	the ``[-q --quiet]`` command-line argument.
	For example, when running

	::

		$ python setup.py build --quiet install [--user]

	the only lines printed to the console by the setup.py file will say that
	specific extensions are being cythonized.

3. Individual extensions
	If VICE's source code has already been compiled and is located in the
	``build`` directory, then the entire code base does not need to be
	re-compiled every time a small modification is made.
	The name of the extension, which can be determined via the relative path
	to the file, is all that is required.
	For example, the ``vice.singlezone`` object is linked to VICE's C library
	in the file ``vice/core/singlezone/_singlezone.pyx``, so the name of its
	extension is ``vice.core.singlezone._singlezone``.
	To recompile this extension only and reinstall with all previously
	compiled extensions, simply run

	::

		$ python setup.py build ext=vice.core.singlezone._singlezone install [--user]


Things to Avoid
---------------

.. _gcc_parallel_note:

1. Parallelization with the gcc_ compiler
	Users manually installing VICE with the gcc_ C compiler should omit the
	``[-j N]`` command-line argument from their call to VICE's ``setup.py``
	file (see `Additional Compile Options`_ above).
	In practice, the developer's find that gcc_ is not able to successfully
	complete compiling VICE across multiple cores.
	This should be a non-issue for those running Mac OS, as gcc_ must be
	installed and clang_ is the default compiler.
	For those on Linux, however, gcc_ is the default.

.. _simultaneous_note:

2. Simultaneous installations
	Users manually installing VICE from source for multiple versions of python
	should not run the setup.py file in separate terminals simultaneously; this
	will cause one of the builds to fail.
	Likewise, users should not run the tests for multiple versions of python
	simultaneously; this will almost certainly cause a ``segmentation fault``.

.. _condanote:


Troubleshooting Your Build
==========================
The following are a number of issues that can arise when manually installing
VICE.
If none of these options solve your problem, or if you attempted an
installation with ``pip`` as opposed to installing manually, please open an
issue `here`__.

__ issues_
.. _issues: https://github.com/giganano/VICE/issues

Running the setup.py File Failed
--------------------------------
`Did you run it for multiple versions of python simultaneously?`__
Alternatively,
`did you run a parallelized installation using the gcc C compiler?`__
If neither is the case, please open an issue `here`__.

__ gcc_parallel_note_
__ simultaneous_note_
__ issues_


Running the Tests Resulted in a Segmentation Fault
--------------------------------------------------
`Did you run the tests for multiple versions of python simultaneously?`__
If not, please open an issue `here`__.

__ simultaneous_note_
__ issues_


VICE Isn't Running from the Command Line
----------------------------------------
If ``vice`` doesn't run from the terminal after installing, first check that
``python3 -m vice`` runs; the two have the same functionality. If neither
work, then it's likely there was an issue with the installation, and we
recommend rerunning the install process, making sure that the instructions are
followed as closely as possible. If this still does not work, please open an
issue `here`__.

__ issues_

If ``python3 -m vice`` works, but ``vice`` does not, then it's likely that
that command line entry was copied to a directory not on your ``PATH``. The
simplest patch for this issue is to create an alias for ``vice`` mapping it to
the longer command. This can be done by adding the following line to your
``~/.bash_profile``:

::

	alias vice="python3 -m vice"

Then either run ``source ~/.bash_profile`` or restart your terminal for the
alias to take effect.

Alternatively, the proper file can simply be copied to any given directory in
your computer. If this directory is not on your ``PATH``, then your ``PATH``
must be modified to contain this file's new location. For example:

::

	$ cp ./bin/vice ~/.local/bin

This will place the command line entry in the ``~/.local/bin/`` directory,
which can be permanently added to your path by adding

::

	export PATH=$HOME/.local/bin:$PATH

to your ``~/.bash_profile``. As with the alias solution, this will require
either running ``source ~/.bash_profile`` or restarting your terminal to
take effect.

**Note**: If you have installed VICE with the ``--user`` option, it is likely
that VICE has automatically made the above modification to your ``PATH``, and
that either running ``source ~/.bash_profile`` or restarting your terminal is
all that is required after copying the file to ``~/.local/bin``. If you have
copied the file to a different directory, VICE will not have added that file
to your ``PATH``.

More information on modifying your PATH can be found `here`__.

If this does not fix the issue, please open an issue `here`__.

.. _pathvariables: https://unix.stackexchange.com/questions/26047/how-to-correctly-add-a-path-to-path
__ pathvariables_
__ issues_

An alternative workaround to this issue is to create an alias for ``vice`` by
adding the following line to


Compiler Failure
----------------
This is usually an indication that the build should not be ran on multiple
cores, which `is usually the case with the gcc C compiler`__.
First run ``make clean``, and subsequently ``make``. Then replace your
previous command to run the setup.py file with:

::

	$ python setup.py build install [--user] [--quiet]

If you were not installing VICE on multiple cores to begin with, try
installing without the ``build`` directive:

::

	$ python setup.py install [--user] [--quiet]

If neither of these recommendations fix your problem, please open an issue
`here`__.

__ gcc_parallel_note_
__ issues_

Uninstalling VICE
=================
If you have installed VICE from PyPI_, it can be uninstalled from the terminal
via ``pip uninstall vice``. When prompted, simply confirm that you would like
the files removed. If you have downloaded VICE's supplementary data for use
with the ``milkyway`` object, it is recommended that you remove these files
first by running

.. code:: python

	import vice
	vice.toolkit.hydrodisk.data._h277_remove()

before the ``pip uninstall vice`` command.

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
format ``vice-<version number>.egg-info``. Remove this directory as well:

::

	$ rm -rf vice-<version number>.egg-info

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
nothing, and attempting to import VICE into python should result in a
``ModuleNotFoundError``.

