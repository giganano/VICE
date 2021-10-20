"""
This package implements the python wrapper of the singlezone object. Source
code can be found at vice/src/multizone.h and accompanying files.
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:
	__all__ = ["multizone", "migration", "test"]
	from .multizone import multizone
	from . import migration
	from .tests import test
else:
	pass
