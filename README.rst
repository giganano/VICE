
VICE: Versatile Integrator for Chemical Evolution
=================================================

Overview
--------

VICE is a simple, user-friendly library for running numerical integrations of 
galactic chemical enrichment under the single-zone, instantaneous mixing 
approximation. It is designed to model the formation of elements by 
core-collapse supernovae, type Ia supernovae, and asymptotic giant branch 
stars. 

Installation
============

System Requirements
-------------------

1) ``Cython version >= 0.25.2``

2) ``Python version 2.6, 2.7, or >= 3.3``

3) ``Make version >= 3.80``

4) ``Clang >= 4.2.0 or gcc >= 4.6``

(Note that these values are currently estimates and the authors are still 
determining conducting tests for system requirements).

Preferred Install Method
------------------------

:: 

	$ git clone https://github.com/giganano/VICE.git
	$ cd VICE
	$ make
	$ python setup.py install [--user]
	$ make tests
	$ make clean
	$ [make]
	$ [python3 setup.py install [--user]]
	$ [make clean]
	$ [make tests3]
	$ [cd ..]
	$ [rm -rf VICE]

This is currently the only install method. VICE will soon be installable via 
pip. 

Implementation
==============

All integration sub-routines are written in ANSI/ISO C and are therefore 
completely cross-platform. This software is NumPy- and Pandas-compatible but 
neither NumPy- nor Pandas-dependent. That is, it will recognize user input 
from NumPy and Pandas data types but will run independently of these 
software packages. All internal data types are stored and handled using the 
C and Python standard libraries. The integration features are therefore 
independent of the user's version of Anaconda or lackthereof. 

The only feature in this software requiring the use of Anaconda is the 'show' 
function associated with 'output' data type, which the authors built using 
matplotlib. Use of this feature is therefore dependent on the user having 
installed matplotlib version 2.0.0 or later. 

Usage
=====

See under the docs/ for instructions and examples on how to use this library. 

Please submit bug reports to <giganano9@gmail.com>

LICENSE
=======

VICE is free software. You may use, redistribute, or modify as you see fit 
under the terms of the LICENSE. See LICENSE for copyright information. 
