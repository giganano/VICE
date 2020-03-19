"""
VICE: Versatile Integrator for Chemical Evolution
=================================================
A software built for numerical integration of single-zone chemical evolution 
models. 

Documentation for this package is available in several forms: 
	1) In the docstrings of the objects and functions 
	2) A user's guide, available at: 
	https://github.com/giganano/VICE/tree/master/docs/users_guide.pdf 
	3) Science documentation, available at: 
	https://github.com/giganano/VICE/tree/master/docs/science_documentation.pdf

Users may also access the documentation from after installing VICE by running 
'vice-docs' from the command line. Run 'vice-docs --help' for more information. 

We recommend first-time users visit the git repository to obtain copies of the 
User's Guide and Science Documentation. Under the docs/ directory, they will 
also find a QuickStartTutorial.ipynb notebook intended for quick 
familiarization with the structure of VICE. 

It is also recommended that VICE users install the package dill, an extension 
of the python standard library package pickle. This enables VICE to encode 
functional attributes with its output, and can be achieved via pip. 

In all docstrings, examples of code are represented by three > signs:

	>>> a = 5
	>>> a += 10


Included Features
=================
::	A dataframe object meant for case-insensitive lookup. 
::	Simulations of galactic chemical enrichment under the single-zone 
	approximation with support for user-specified parameters, many of which 
	can be functions of time.  
::	Simulations of enrichment from single stellar populations 
::	Built-in yield tables from two recent studies of nucleosynthetic yields 
	from asymptotic giant branch stars. 
::	Calculations of IMF-integrated nucleosynthetic yields from both core 
	collapse and type Ia supernovae. 
:: 	User-specified yields from core-collapse supernovae, which may be callable 
	functions of metallicity. 
::	User-specified yields from type Ia supernovae. 
::	A command-line entry allowing users to run simulations of simple 
	evoluationary histories directly from a linux terminal. 
::	A custom warning class (ScienceWarning) separating warnings about 
	scientific accuracy and precision from those purely related to code. 

LICENSE 
======= 
VICE is open-source software released under the MIT license. See LICENSE for 
further details and copyright information. 

Citing
====== 
If usage of this software leads to a publication, please cite Johnson & 
Weinberg (2019), arXiv:1911.02598. 
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
try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 

if __VICE_SETUP__: 
	from .src import * 
	from ._build_utils import * 
	_LONG_DESCRIPTION_ = __doc__
else:
	if "vice" in os.listdir(os.getcwd()): 
		raise ImportError("""\
Error importing VICE. VICE is a pre-compiled package and cannot be ran from \
its source directory, because the compiled objects are not stored here. Please \
exit the VICE source tree and relaunch your python interpreter from there. \
""") 
	else: 

		__all__ = [
			"__author__", 
			"__version__", 
			"modeling", 
			"elements", 
			"yields", 
			"_globals", 
			"ScienceWarning", 
			"VisibleDeprecationWarning"
		]  

		try: 
			from .version import version as __version__
			from .version import release as __release
			if not __release: 
				warnings.warn("Using un-released version of VICE", UserWarning)
			from .core import * 
			from ._build_utils import * 
			from ._globals import ScienceWarning
			from ._globals import VisibleDeprecationWarning 
			from . import modeling 
			from . import elements 
			from . import yields 
			from .tests import test 
		except (ImportError, ModuleNotFoundError): 
			raise ImportError("""\
Error importing VICE. If you have attempted an alternate installation method, \
please visit https://github.com/giganano/VICE.git and follow the preferred \
installation method. \

To troubleshoot your build, see VICE's source code repository at \
https://github.com/giganano/VICE.git and click on "Troubleshoot Your Build" \
under "Install VICE." \
""")

	__all__.extend(core.__all__)
	__all__.extend(_build_utils.__all__)

	"""
	Remove locally imported variables that aren't needed, but leave the user 
	the ability to call vice.warnings to get only VICE to keep quiet and let 
	the rest of python raise warnings. 
	"""
	del core
	del _build_utils
	del version
	del __release
	del absolute_import
	del sys
	del os

