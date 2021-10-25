r"""
VICE: Versatile Integrator for Chemical Evolution

* 77 elements on the periodic table
* Fast integration of one-zone models
* Enrichment from single stellar populations
* Highly flexible nucleosynthetic yield calculations
* User-defined mathematical forms describing:
	- Nucleosynthetic yields in simulations
	- Mixing processes in multi-zone models
	- Infall and star formation histories
	- The stellar initial mass function
	- The star formation law
	- Element-by-element infall metallicities
	- Type Ia supernova delay-time distributions

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
the command line by running ``vice --tutorial``. Other example scripts can
be found there as well.

Contents
--------
singlezone : ``object``
	Simulate a single-zone galactic chemical evolution model
multizone : ``object``
	Simulate a multi-zone galactic chemical evolution model
milkyway : ``object``
	A ``multizone`` object optimized for modeling the Milky Way.
output : ``object``
	Read and store output from ``singlezone`` simulations.
multioutput : ``object``
	Read and store output from ``multizone`` simulations.
migration : <module>
	Utilities for mixing prescriptions in multizone simulations.
single_stellar_population : <function>
	Simulate enrichment from a single conatal star cluster
cumulative_return_fraction : <function>
	Calculate the cumulative return fraction of a star cluster of known age
main_sequence_mass_fraction : <function>
	Calculate the main sequence mass fraction of a star cluster of known age
imf : <module>
	Built-in funcitonal forms of popular stellar initial mass functions.
mlr : ``object``
	Built-in popular function forms of the stellar mass-lifetime relationship.
	Also stores which form to adopt in chemical evolution models.
yields : <module>
	Calculate, access, and declare nucleosynthetic yield settings for use in
	simulations.
elements : <module>
	Access, and declare nucleosynthetic yield settings for use in simulations.
	Access other relevant information for each element such as the solar
	abundance or atomic number.
dataframe : ``object``
	A dictionary-like object with case-insensitive lookup and data storage.
history : <function>
	Reads in time-evolution of interstellar medium from singlezone simulation.
mdf : <function>
	Reads in stellar metallicity distribution from singlezone simulation.
stars : <function>
	Read in stellar population abundances from a multizone simulation output.
toolkit : <module>
	Generally useful utilities.

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
			"milkyway",
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
			if not version.isreleased:
				warnings.warn("Using un-released version of VICE", UserWarning)
			else:
				prerelease = False
				for item in [version.dev, version.alpha, version.beta,
					version.rc]:
					prerelease |= item is not None
					if prerelease: break
				if prerelease: warnings.warn("Using a pre-release of VICE",
					UserWarning)
			from .milkyway import milkyway
			from . import milkyway
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

