# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ....._globals import _VERSION_ERROR_
from .....testing import moduletest
from .....testing import unittest
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from libc.stdlib cimport malloc, free
from . cimport _generic

_TIMES_ = [0.05 * i for i in range(201)]


@moduletest
def generic_test():
	r"""
	Runs a generic test on the multizone object. This runs the default case
	and makes assertions that should be true for all multizone objects.
	"""
	msg = "vice.core.multizone generic case : default parameters"
	try:
		_TEST_ = generic(n_zones = 5)
		_TEST_.run()
	except:
		return [msg, None]
	return [msg,
		[
			_TEST_.test_inject_tracers()
		]
	]


cdef class generic:

	r"""
	A class intended to run unit tests for generic multizone cases. These
	are cases which should always produce no stellar migration between zones.
	"""

	def __init__(self, **kwargs):
		if "name" in kwargs.keys(): del kwargs["name"]
		super().__init__(name = "test", **kwargs)

	def run(self):
		r"""
		Runs the simulation
		"""
		self.align_name_attributes()
		self.prep(_TIMES_)
		self.outfile_check(True)
		os.system("mkdir %s.vice" % (self.name))
		for i in range(self._mz[0].mig[0].n_zones):
			os.system("mkdir %s.vice" % (self._zones[i].name))
		self.setup_migration()
		_generic.multizone_setup(self._mz)
		_generic.multizone_evolve_full(self._mz)
		_generic.tracers_MDF(self._mz)
		_generic.write_multizone_mdf(self._mz[0])
		if not _generic.multizone_open_tracer_file(self._mz):
			_generic.write_tracers_header(self._mz[0])
			_generic.write_tracers_output(self._mz[0])
			_generic.multizone_close_tracer_file(self._mz)
		else:
			raise Exception

	@unittest
	def test_inject_tracers(self):
		r"""
		vice.src.multizone.tracer.inject_tracers generic test
		"""
		def test():
			return _generic.generic_test_inject_tracers(self._mz)
		return ["vice.src.multizone.tracer.inject_tracers", test]
