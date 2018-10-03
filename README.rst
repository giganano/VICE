
|version| |MIT Licensed|

``VICE: Versatile Integrator for Chemical Evolution``
=====================================================

Overview
--------

``VICE`` is a simple, user-friendly library for running numerical integrations 
of galactic chemical enrichment under the single-zone, instantaneous mixing 
approximation. It is designed to model the formation of elements by 
core-collapse supernovae, type Ia supernovae, and asymptotic giant branch 
stars. 

Why You Should Use It
---------------------

``VICE`` is designed to recognize infall histories, gas histories, star 
formation histories, outflow models, outflow metallicity models, inflow 
metallicities, and star formation efficiency histories as callable functions 
of time, allowing for the integration of arbitrarily complex models under the 
single-zone approximation. It also allows the user to pass a function of 
time to specify their own SNe Ia delay-time distribution, and can handle 
user-specified fractional yields for both core-collapse and type Ia 
supernovae. On a system with a 2.7GHz Intel Core i5 processor with 8 GB of 
DDR3 RAM (e.g. a base-model 2015 Macbook Pro), an integration over the default 
parameter space with hyperfine timestepping (i.e. ~1 Myr timesteps) takes ~75 
MB of RAM and finishes in approximately 19.6 seconds. With only slightly 
coarser timestepping (i.e. ~5 Myr), the integration finishes on the same 
system in approximately 800 milliseconds. 

Installation
============

System Requirements
-------------------

``VICE`` supports linux and Mac OS X. Because ``VICE`` is implemented using 
only ``C`` and ``python`` standard libraries, it is technically entirely 
cross-platform. However, ``VICE`` is currently not packaged for installation 
on ``Windows``. Users can open a request at 
<https://github.com/giganano/VICE/issues> for ``Windows`` compatibility, and 
it will be fulfilled if there is sufficient demand. 

1) ``Cython version >= 0.25.2``

2) ``Python version 2.6, 2.7, or >= 3.3``

3) ``Make version >= 3.80``

4) ``Clang >= 4.2.0 or gcc >= 4.6``

Preferred Install Method
------------------------

We recommend users install ``VICE`` from a terminal using the following 
sequence of commands:

:: 

	$ git clone https://github.com/giganano/VICE.git
	$ cd VICE
	$ make
	$ python setup.py install [--user]
	$ [make clean]
	$ [make tests]
	$ [make]
	$ [python3 setup.py install [--user]]
	$ [make clean]
	$ [make tests3]
	$ [cd ..]
	$ [rm -rf VICE]


Optional elements of the installation process are bound in brackets. The 
option ``[--user]`` should be invoked when the user wishes to install to 
their ``~/.local/`` ``python`` library. The final lines are those which will 
install the ``python 3`` version of ``VICE`` and remove the local copy of 
``VICE``'s source code. 

If the user wishes to install both ``python 2`` and ``python 3`` versions of 
``VICE``, they must run ``make clean && make`` between calls to 
``python setup.py install [--user]``. Failing to do so will cause a 
compiler error during subsequent calls to the ``setup.py`` file. 
``make tests3`` runs the tests for only the ``python 3`` version of ``VICE``, 
while ``make tests`` runs them for ``python 2``. 

This is currently the only install method for ``VICE``. It is not installable 
via ``pip``. 

Implementation
==============

All integration sub-routines are written in ANSI/ISO C and are therefore 
completely cross-platform. This software is NumPy- and Pandas-compatible but 
neither NumPy- nor Pandas-dependent. That is, it will recognize user input 
from NumPy and Pandas data types but will run independently of these 
software packages. All internal data types are stored and handled using the 
C and Python standard libraries. The integration features are therefore 
independent of the user's version of Anaconda or lackthereof. 

The only feature in this software requiring the use of Anaconda is the ``show`` 
function associated with ``output`` class, which requires 
``matplotlib >= 2``. This function is however not a part of the integration 
features associated with chemical evolution modeling, and is purely intended 
so that the user may inspect the results of their integrations visually in 
``ipython`` without having to plot it themselves. 

Usage
=====

See under the docs/ for instructions and examples on how to use this library. 

For bug reports, users may either open an issue on the github webpage for 
this software <https://github.com/giganano/VICE>. Bug reports can also be 
emailed with the subject 'BUG in VICE' to <giganano9@gmail.com>.

LICENSE
=======

``VICE`` is free software. You may use, redistribute, or modify as you see fit 
under the terms of the LICENSE. See LICENSE for copyright information. 

..	|version| image:: https://img.shields.io/badge/version-1.0.0-blue.svg
	:target: https://img.shields.io/badge/version-1.0.0-blue.svg
	:alt: version
..	|MIT Licensed| image:: https://img.shields.io/badge/license-MIT-blue.svg
	:target: https://raw.githubusercontent.com/giganano/VICE/master/LICENSE
	:alt: MIT License
