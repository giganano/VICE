# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ....._globals import _VERSION_ERROR_
from .....testing import moduletest
from .....testing import unittest
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from libc.stdlib cimport malloc, free
from . cimport _generic

_TIMES_ = [0.01 * i for i in range(1001)]


cdef class generic:

	r"""
	A class intended to run unit tests for quiescent cases. These are cases
	which should always produce no star formation and thus no elemental
	production.
	"""

	def __init__(self, **kwargs):
		if "name" in kwargs.keys(): del kwargs["name"]
		super().__init__(name = "test", **kwargs)
		self.prep(_TIMES_)
		self.open_output_dir(True)
		self._sz[0].n_outputs = len(_TIMES_)
		self._sz[0].output_times = <double *> malloc (self._sz[0].n_outputs *
			sizeof(double))
		for i in range(self._sz[0].n_outputs):
			self._sz[0].output_times[i] = _TIMES_[i]
		_generic.singlezone_setup(self._sz)
		_generic.singlezone_evolve_no_setup_no_clean(self._sz)
		_generic.normalize_MDF(self._sz)
		_generic.write_mdf_output(self._sz[0])

