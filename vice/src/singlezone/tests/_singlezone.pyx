# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ....testing import moduletest
from ....testing import unittest

from libc.stdlib cimport malloc, free
from libc.string cimport strcpy
from . cimport _singlezone
from . cimport _element
from . cimport _sneia
from . cimport _io
from . cimport _ism
from . cimport _mdf

_TEST_DT_ = 0.01
_TEST_TIMES_ = [_TEST_DT_ * i for i in range(101)]


@moduletest
def test():
	r"""
	vice.src.singlezone.singlezone module test
	"""
	return ["vice.src.singlezone",
		[
			test_singlezone(run = False),
			test_element(run = False),
			test_ism(run = False),
			test_mdf(run = False),
			test_sneia(run = False)
		]
	]


@moduletest
def test_singlezone():
	r"""
	vice.src.singlezone.singlezone module test
	"""
	try:
		_TEST_ = singlezone_tester()
	except:
		return ["vice.src.singlezone.singlezone", None]
	return ["vice.src.singlezone.singlezone",
		[
			_TEST_.test_singlezone_address(),
			_TEST_.test_singlezone_n_timesteps(),
			_TEST_.test_singlezone_setup(),
			_TEST_.test_singlezone_evolve()
		]
	]


@moduletest
def test_element():
	r"""
	vice.src.singlezone.element module test
	"""
	try:
		_TEST_ = singlezone_tester()
	except:
		return ["vice.src.singlezone.element", None]
	return ["vice.src.singlezone.element",
		[
			_TEST_.test_element_malloc_Z()
		]
	]


@moduletest
def test_ism():
	r"""
	vice.src.singlezone.ism module test
	"""
	try:
		_TEST_ = singlezone_tester()
	except:
		return ["vice.src.singlezone.ism", None]
	return ["vice.src.singlezone.ism",
		[
			_TEST_.test_ism_setup_gas_evolution(),
			_TEST_.test_ism_update_gas_evolution()
		]
	]


@moduletest
def test_mdf():
	r"""
	vice.src.singlezone.mdf module test
	"""
	try:
		_TEST_ = singlezone_tester()
	except:
		return ["vice.src.singlezone.mdf", None]
	return ["vice.src.singlezone.mdf",
		[
			_TEST_.test_mdf_setup_MDF()
		]
	]


@moduletest
def test_sneia():
	r"""
	vice.src.singlezone.sneia module test
	"""
	try:
		_TEST_ = singlezone_tester()
	except:
		return ["vice.src.singlezone.sneia", None]
	return ["vice.src.singlezone.sneia",
		[
			_TEST_.test_sneia_setup_RIa()
		]
	]


cdef class singlezone_tester:

	r"""
	The c_singlezone class is subclassed here to give these routines access to
	the SINGLEZONE *_sz attribute.
	"""

	def __init__(self):
		super().__init__(name = "test", dt = _TEST_DT_)
		self._reset_prep()


	def _reset_prep(self):
		self.prep(_TEST_TIMES_)
		self.open_output_dir(True)
		self._sz[0].n_outputs = len(_TEST_TIMES_)
		self._sz[0].output_times = <double *> malloc (self._sz[0].n_outputs *
			sizeof(double))
		for i in range(self._sz[0].n_outputs):
			self._sz[0].output_times[i] = _TEST_TIMES_[i]

	@unittest
	def test_singlezone_address(self):
		r"""
		vice.src.singlezone.singlezone.singlezone_address unit test
		"""
		def test():
			return _singlezone.singlezone_address(self._sz) == <long> (
				<void *> self._sz)
		return ["vice.src.singlezone.singlezone.singlezone_address", test]

	@unittest
	def test_singlezone_n_timesteps(self):
		r"""
		vice.src.singlezone.singlezone.n_timesteps unit test
		"""
		def test():
			return _singlezone.n_timesteps(self._sz[0]) == 110
		return ["vice.src.singlezone.singlezone.n_timesteps", test]

	@unittest
	def test_singlezone_setup(self):
		r"""
		vice.src.singlezone.singlezone.singlezone_setup unit test
		"""
		def test():
			result = 1 - _singlezone.singlezone_setup(self._sz)
			_singlezone.singlezone_cancel(self._sz)
			return result
		return ["vice.src.singlezone.singlezone.singlezone_setup", test]

	@unittest
	def test_singlezone_evolve(self):
		r"""
		vice.src.singlezone.singlezone.singlezone_evolve unit test
		"""
		def test():
			self._reset_prep()
			return 1 - _singlezone.singlezone_evolve(self._sz)
		return ["vice.src.singlezone.singlezone.singlezone_evolve", test]

	@unittest
	def test_element_malloc_Z(self):
		r"""
		vice.src.singlezone.element.malloc_Z unit test
		"""
		def test():
			if 1 - _element.malloc_Z(self._sz[0].elements[0], 10):
				free(self._sz[0].elements[0][0].Z)
				return True
			else:
				return False
		return ["vice.src.singlezone.element.malloc_Z", test]

	@unittest
	def test_ism_setup_gas_evolution(self):
		r"""
		vice.src.singlezone.ism.setup_gas_evolution unit test
		"""
		def test():
			self._sz[0].timestep = 0
			try:
				strcpy(self._sz[0].ism[0].mode, "gas")
				assert _ism.setup_gas_evolution(self._sz) == 0
				strcpy(self._sz[0].ism[0].mode, "ifr")
				assert _ism.setup_gas_evolution(self._sz) == 0
				strcpy(self._sz[0].ism[0].mode, "sfr")
				assert _ism.setup_gas_evolution(self._sz) == 0
			except:
				return False
			return True
		return ["vice.src.singlezone.ism.setup_gas_evolution", test]

	@unittest
	def test_ism_update_gas_evolution(self):
		r"""
		vice.src.singlezone.ism.update_gas_evolution unit test
		"""
		def test():
			if _singlezone.singlezone_setup(self._sz): return False
			try:
				strcpy(self._sz[0].ism[0].mode, "gas")
				assert _ism.update_gas_evolution(self._sz) == 0
				strcpy(self._sz[0].ism[0].mode, "ifr")
				assert _ism.update_gas_evolution(self._sz) == 0
				strcpy(self._sz[0].ism[0].mode, "sfr")
				assert _ism.update_gas_evolution(self._sz) == 0
			except:
				return False
			return True
		return ["vice.src.singlezone.ism.update_gas_evolution", test]

	@unittest
	def test_mdf_setup_MDF(self):
		r"""
		vice.src.singlezone.mdf.setup_MDF unit test
		"""
		def test():
			return 1 - _mdf.setup_MDF(self._sz)
		return ["vice.src.singlezone.mdf.setup_MDF", test]

	@unittest
	def test_sneia_setup_RIa(self):
		r"""
		vice.src.singlezone.sneia.setup_RIa unit test
		"""
		def test():
			return 1 - _sneia.setup_RIa(self._sz)
		return ["vice.src.singlezone.sneia.setup_RIa", test]

	@unittest
	def test_singlezone_open_files(self):
		r"""
		vice.src.io.singlezone.singlezone_open_files unit test
		"""
		def test():
			result = 1 - _io.singlezone_open_files(self._sz)
			if result: _io.singlezone_close_files(self._sz)
			return result
		return ["vice.src.io.singlezone.singlezone_open_files", test]

