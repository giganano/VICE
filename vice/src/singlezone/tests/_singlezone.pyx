# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ....testing import moduletest 
from ....testing import unittest 

from libc.stdlib cimport malloc, free 
from . cimport _singlezone 

_TEST_DT_ = 0.01 
_TEST_TIMES_ = [_TEST_DT_ * i for i in range(101)] 


@moduletest 
def test(): 
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
			_TEST_.test_singlezone_stellar_mass() 
		] 
	] 


cdef class singlezone_tester: 

	r""" 
	The c_singlezone class is subclassed here to give these routines access to 
	the SINGLEZONE *_sz attribute. 
	""" 

	def __init__(self): 
		super().__init__(name = "test", dt = _TEST_DT_) 
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
			test_time = 10
			test_dt = 0.01 
			self._sz[0].output_times = <double *> malloc (10 * sizeof(double)) 
			self._sz[0].output_times[9] = 10 
			self._sz[0].n_outputs = 10 
			self._sz[0].dt = test_dt 
			result = _singlezone.n_timesteps(self._sz[0]) == (test_time / 
				test_dt + _singlezone.BUFFER) 
			free(self._sz[0].output_times) 
			return result 
		return ["vice.src.singlezone.singlezone.n_timesteps", test] 

	@unittest 
	def test_singlezone_stellar_mass(self): 
		r""" 
		vice.src.singlezone.singlezone.singlezone_stellar_mass unit test 
		""" 
		def test(): 
			self._sz[0].ism[0].star_formation_history = <double *> malloc (
				_singlezone.n_timesteps(self._sz[0]) * sizeof(double)) 
			self._sz[0].ssp[0].crf = <double *> malloc (
				_singlezone.n_timesteps(self._sz[0]) * sizeof(double)) 
			for i in range(_singlezone.n_timesteps(self._sz[0])): 
				self._sz[0].ism[0].star_formation_history[i] = 1 
				self._sz[0].ssp[0].crf[i] = 0 
			self._sz[0].timestep = self._sz[0].n_outputs 
			return (abs(_singlezone.singlezone_stellar_mass(self._sz[0]) -
				(self._sz[0].n_outputs) * self._sz[0].dt) <= 1.e-15) 
		return ["vice.src.singlezone.singlezone.singlezone_stellar_mass", test] 


