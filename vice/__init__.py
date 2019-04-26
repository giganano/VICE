# This file, included with the VICE package, is protected under the terms of the 
# associated MIT License, and any use or redistribution of this file in original 
# or altered form is subject to the copyright terms therein. 

"""
VICE: Versatile Integrator for Chemical Evolution
=================================================
A software built for numerical integration of single-zone chemical evolution 
models. 

See LICENSE for copyright information and citation requirements. 

Documentation for this package is available in two forms: 
	1) In the docstrings of the objects and functions
	2) Under docs/ in VICE's git repository at: 
		<https://github.com/giganano/VICE/tree/master/docs>

We recommend first-time users visit the git repository to obtain copies of the 
User's Guide and Science Documentation. Under the docs/ directory, they will 
find a QuickStartTutorial.ipynb notebook intended for quick familiarization 
with the structure of VICE. 

It is also recommended that VICE users install the package dill, an extension 
of the python standard library package pickle. This enables VICE to encode 
functional attributes with its output, and can be achieved via pip. 

In all docstrings, examples of code are represented by three > signs:

	>>> a = 5
	>>> a += 10


Included Features
=================

The VICE Dataframe 
------------------
	A data storing object meant for case-insensitive lookup 

	Instances of this class included with VICE:
	-------------------------------------------
		atomic_number: 
			The number of protons in the nucles of each recognized element 
		ccsne_yields: 
			User-specified yield settings from core collapse supernovae 
		sneia_yields: 
			User-specified yield settings from type Ia supernovae 
		solar_z: 
			The solar abundance by mass of each element calibrated by Asplund 
			et al. (2009), ARA&A, 47, 481
		sources: 
			The dominant enrichment sources for each element 

Classes 
-------
	singlezone: 
		Run simulations of single-zone galactic chemical evolution models 
	output: 
		Handle the output of the integrator class 

Functions 
---------
	agb_yield_grid: 
		Returns a built-in mass-metallicity yield grid for a given element 
	fractional_cc_yield: 
		Returns an IMF-integrated yield for a given element from core-collapse 
		supernovae 
	fractional_ia_yield: 
		Returns an IMF-integrated yield for a give nelement from type Ia 
		supernovae 
	history: 
		Read in simulation output containing the time-evolution of the ISM 
	mdf: 
		Read in the stellar metallicity distribution function from a simulation 
	mirror: 
		Given an output object, returns an integrator with the same properties 
		as that which produced the output 
	single_ia_yield: 
		Returns the mass of a given element produced by a single instance of 
		a type Ia supernova on average 
	single_stellar_population: 
		Returns the mass of a given element produced over time by a single 
		episode of star formation

Command Line 
============
VICE also allows users to run simulations of simple evolutionary histories 
directly from the command line. Type "vice -h" in a terminal for instructions 
on how to do so. 
"""

from __future__ import absolute_import
import warnings 
import sys
import os

__author__ = "James W. Johnson <giganano9@gmail.com>"

try: 
	__VICE_SETUP__ 
except NameError:
	__VICE_SETUP__ = False

if __VICE_SETUP__: 
	from ._build_utils import *
	_LONG_DESCRIPTION_ = __doc__
else:
	try:
		from .version import version as __version__
		from .version import release as __release
	except: 
		message = "Error importing VICE. You should not try to run VICE from " 
		message += "within its source directory. Please exit the VICE source "
		message += "tree and relaunch your python interpreter from there." 
		raise ImportError(message)

	if not __release: 
		warnings.warn("Using un-released version of VICE", UserWarning)

	__all__ = ["__author__", "__version__"]

	from .core import * 
	from .data import * 
	from ._build_utils import *

	__all__.extend(core.__all__)
	__all__.extend(data.__all__)
	__all__.extend(_build_utils.__all__)

	"""
	Remove locally imported variables that aren't needed, but leave the user 
	the ability to call vice.warnings to get only VICE to keep quiet and let 
	the rest of python raise warnings. 
	"""
	del core
	del data
	del _build_utils
	del version
	del __release
	del absolute_import
	del sys
	del os

