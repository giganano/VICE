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

	1. Docstrings embedded within the code 
	2. On PyPI 
	3. In PDF format 
	4. Tutorials and example scripts, available in the git repository 

The ``vice-docs`` command line entry will open VICE's documentation 
automatically. By default, this will open the user's web browser to the online 
documentation. Offline documentation can be accessed via the PDF by running 
``vice-docs --pdf``. Run ``vice-docs --help`` in a terminal for more 
information. 
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
			from .core.dataframe import base as dataframe 
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

