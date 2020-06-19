r"""
VICE: Versatile Integrator for Chemical Evolution 

Provides
--------
- A dataframe object meant for case-insensitive lookup 
- Simulations of galactic chemical evolution models 
- Simulations of nucleosynthesis from single stellar populations 
- Built-in yield tables from nucleosynthesis studies 

How to Access the Documentation: 
--------------------------------
Documentation is available in several forms: 

	1. Online: http://vice-astro.readthedocs.io 
	2. In PDF format, available for download at the same address 
	3. In the docstrings embedded within the software 

Running ``vice --docs`` from the terminal will open the online documentation 
in the default web browser. 

First time users should go through VICE's QuickStartTutorial jupyter notebook, 
available under examples/ in the git repository. This can be launched from 
the command line by running ``vice --tutorial``. 

Example scripts can be found under examples/ in the git repository at 
http://github.com/giganano/VICE. 

Contents 
--------
singlezone : ``type`` 
	Simulate a single-zone galactic chemical evolution model 
output : ``type`` 
	Read and store output from single- and multi-zone simulations. 
single_stellar_population : <function> 
	Simulate enrichment from a single conatal star cluster 
cumulative_return_fraction : <function> 
	Calculate the cumulative return fraction of a star cluster of known age 
main_sequence_mass_fraction : <function> 
	Calculate the main sequence mass fraction of a star cluster of known age 
imf : <module> 
	Built-in funcitonal forms of popular stellar initial mass functions. 
yields : <module> 
	Calculate, access, and declare nucleosynthetic yield settings for use in 
	simulations. 
elements : <module> 
	Access, and declare nucleosynthetic yield settings for use in simulations. 
	Access other relevant information for each element such as the solar 
	abundance or atomic number. 
dataframe : ``type`` 
	An extension to the Python type ``dict`` to allow case-insensitivity. 
history : <function> 
	Reads in time-evolution of interstellar medium from singlezone simulation. 
mdf : <function> 
	Reads in stellar metallicity distribution from singlezone simulation. 

Built-In Dataframes 
-------------------
- atomic_number : The atomic number of each element 
- primordial : The abundance of each element following big bang nucleosynthesis. 
- solar_z : The abundance of each element in the sun. 
- sources : The primary astrophysical production channels of each element. 
- stable_isotopes : Lists of each elements' stable isotopes. 

Utilities
---------
- VisibleDeprecationWarning : A DeprecationWarning that is visible by default. 
- VisibleRuntimeWarning : A RuntimeWarning that is visible by default. 
- ScienceWarning : A Warning concerning scientific accuracy and precision. 
- test : Runs VICE's unit tests. 
- version : VICE's version breakdown. 
- __version__ : The version string. 
"""

from __future__ import absolute_import
import warnings 
import sys
import os
if sys.version_info[:2] < (3, 5): 
	raise RuntimeError("""This version of VICE requires python >= 3.5. \
Current version: %d.%d.%d.""" % (sys.version_info.major, 
		sys.version_info.minor, sys.version_info.micro)) 
else: pass 

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

		__author__ = "James W. Johnson <giganano9@gmail.com>" 
		__all__ = [
			"__author__", 
			"__version__", 
			"elements", 
			"yields", 
			"_globals", 
			"toolkit", 
			"ScienceWarning", 
			"VisibleRuntimeWarning", 
			"VisibleDeprecationWarning"
		] 

		try: 
			from .version import version 
			__version__ = str(version) 
			if not version.released: 
				warnings.warn("Using un-released version of VICE", UserWarning)
			from .core import * 
			from .core.dataframe import base as dataframe 
			from ._build_utils import * 
			from ._globals import ScienceWarning
			from ._globals import VisibleRuntimeWarning 
			from ._globals import VisibleDeprecationWarning 
			from . import elements 
			from . import yields 
			from . import toolkit 
			from .tests import test 
			__all__.extend(core.__all__) 
			__all__.extend(_build_utils.__all__) 
		except (ImportError, ModuleNotFoundError): 
			raise ImportError("""\
Error importing VICE. If you conducted this installation with pip, it is \
likely there is not a binary installer for this operating system and \
version of python. \

To solve this, use pip to uninstall VICE, and then install from source. If \
you have installed from source, see the section of the documentation entitled \
"Troubleshooting Your Build" at the following link: \

https://vice-astro.readthedocs.io/en/latest/install.html#troubleshooting-your-build
""")

