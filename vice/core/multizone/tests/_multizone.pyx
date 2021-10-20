# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = ["test"]
from ....testing import moduletest
from ....testing import unittest
import os

from libc.string cimport strcmp
from . cimport _multizone
from .._migration cimport mig_specs


@moduletest
def test():
	r"""
	vice.core.multizone module test
	"""
	try:
		_TEST_ = multizone_tester()
	except:
		return ["vice.core.multizone", None]
	return ["vice.core.multizone",
		[
			_TEST_.test_name_setter(),
			_TEST_.test_n_stars_setter(),
			_TEST_.test_verbose_setter(),
			_TEST_.test_simple_setter(),
			_TEST_.test_migration_setter(),
			_TEST_.test_prep(),
			_TEST_.test_outfile_check()
		]
	]


cdef class multizone_tester:

	r"""
	The c_multizone class is subclassed here to give these routines access to
	the MULTIZONE *_mz attribute.
	"""

	def __init__(self):
		super().__init__(**{})


	@unittest
	def test_name_setter(self):
		r"""
		vice.core.multizone.name.setter unit test
		"""
		def test():
			try:
				self.name = "test"
			except:
				return False
			return not strcmp(self._mz[0].name, "test.vice")
		return ["vice.core.multizone.name.setter", test]


	@unittest
	def test_n_stars_setter(self):
		r"""
		vice.core.multizone.n_stars.setter unit test
		"""
		def test():
			try:
				self.n_tracers = 2
			except:
				return False
			return self.n_tracers == 2
		return ["vice.core.multizone.n_stars.setter", test]


	@unittest
	def test_verbose_setter(self):
		r"""
		vice.core.multizone.verbose.setter unit test
		"""
		def test():
			try:
				self.verbose = True
			except:
				return False
			return self.verbose
		return ["vice.core.multizone.verbose.setter", test]


	@unittest
	def test_simple_setter(self):
		r"""
		vice.core.multizone.simple.setter unit test
		"""
		def test():
			try:
				self.simple = True
			except:
				return False
			return self.simple
		return ["vice.core.multizone.simple.setter", test]


	@unittest
	def test_migration_setter(self):
		r"""
		vice.core.multizone.migration.setter unit test
		"""
		def test():
			try:
				test_mig_specs = mig_specs(self.n_zones)
			except:
				return None
			try:
				self.migration = test_mig_specs
			except:
				return False
			return self.migration == test_mig_specs
		return ["vice.core.multizone.migration.setter", test]


	@unittest
	def test_prep(self):
		r"""
		vice.core.multizone.prep unit test
		"""
		def test():
			try:
				test_times = [0.1 * i for i in range(10)]
				self.prep(test_times)
			except:
				return False
			status = True
			for i in range(self.n_zones):
				status &= (
					<void *> self._mz[0].zones[i][0].output_times is not NULL
				)
				status &= (
					self._mz[0].zones[i][0].n_outputs ==
					<unsigned long> len(test_times)
				)
				status &= (
					self._mz[0].zones[i][0].ism[0].mass == self.zones[i].Mg0
				)
				status &= (
					<void *> self._mz[0].zones[i][0].ism[0].eta is not NULL
				)
				status &= (
					<void *> self._mz[0].zones[i][0].ism[0].enh is not NULL
				)
				status &= (
					<void *> self._mz[0].zones[i][0].ism[0].tau_star is not
					NULL
				)
				status &= (
					<void *> self._mz[0].zones[i][0].ism[0].specified is not
					NULL
				)
			return status
		return ["vice.core.multizone.prep", test]


	@unittest
	def test_outfile_check(self):
		r"""
		vice.core.multizone.outfile_check unit test
		"""
		def test():
			try:
				self.name = "test"
				self.outfile_check(True)
			except:
				return False
			if "test.vice" in os.listdir(os.getcwd()):
				# Sometimes Linux leaves behind .nfs files that can't be
				# removed, giving the message that the device or resource
				# is busy. If the test.vice directory is still there, the test
				# can still pass if only those files are present.
				status = True
				for root, dirs, files in os.walk("test.vice"):
					for f in files:
						status &= f.startswith(".nfs")
						if not status: break
					if not status: break
				return status
			else:
				return True
		return ["vice.core.multizone.outfile_check", test]


