
VICE: Versatile Integrator for Chemical Evolution
=================================================

**Overview**
VICE is a simple, user-friendly library for running numerical integrations of 
galactic chemical enrichment under the single-zone, instantaneous mixing 
approximation. It is designed to model the formation of elements by 
core-collapse supernovae, type Ia supernovae, and asymptotic giant branch 
stars. 

All integration sub-routines are written in ANSI/ISO C and are therefore 
completely cross-platform. The authors wrapped these features for Python 
compatibility using Cython version 0.25.2, and have implemented Python 
variables using version 2.7.13. This software is NumPy- and Pandas-compatible 
but neither NumPy- nor Pandas-dependent. That is, it will recognize user input 
from NumPy and Pandas data types but will run independently of these software 
packages. All internal data types are stored and handled using the C and 
Python standard libraries. The integration features are therefore independent 
of the user's version of Anaconda or lackthereof. Based on this build, VICE 
requires Python version 2.6, 2.7, 3.3, or later. 

The only feature in this software requiring the use of Anaconda is the 'show' 
function associated with 'output' data type, which the authors built using 
matplotlib. Use of this feature is therefore dependent on the user having 
installed matplotlib version 2.0.0 or later. 

See under the docs/ for instructions on how to use this library. 

VICE is free software. You may use, redistribute, or modify as you see fit 
under the terms of the LICENSE. See LICENSE for copyright information. 
