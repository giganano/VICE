"""
This package implements the python wrapper of the singlezone object. Source
code can be found at vice/src/singlezone.h and accompanying files.
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	import warnings
	__all__ = ["singlezone", "test"]
	from .singlezone import singlezone
	from .tests import test
else:
	pass
