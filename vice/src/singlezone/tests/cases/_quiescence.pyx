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
from . cimport _quiescence 
from libc.stdlib cimport malloc, free 

_TIMES_ = [0.01 * i for i in range(1001)] 


@moduletest 
def quiescence_test(): 
	r""" 
	Run a quiescence edge-case test. These are defined as parameter spaces 
	which yield no star formation, and thus no elemental production. This 
	module test ensures that these conditions are met. 
	""" 
	description = "vice.core.singlezone edge case: quiescence" 
	try: 
		_TEST_ = quiescence() 
	except: 
		return [description, None] # skip test 
	return [description, 
		[ 
			_TEST_.test_m_agb() 
		] 
	] 



cdef class quiescence: 

	r""" 
	A class intended to run unit tests for quiescent cases. These are cases 
	which should always produce no star formation and thus no elemental 
	production. 
	""" 

	def __init__(self): 
		super().__init__(name = "test", tau_star = lambda t: float("inf"))  
		self.prep(_TIMES_) 
		self.open_output_dir(True) 
		self._sz[0].n_outputs = len(_TIMES_) 
		self._sz[0].output_times = <double *> malloc (self._sz[0].n_outputs * 
			sizeof(double)) 
		for i in range(self._sz[0].n_outputs): 
			self._sz[0].output_times[i] = _TIMES_[i] 
		_quiescence.singlezone_setup(self._sz) 
		_quiescence.singlezone_evolve_no_setup_no_clean(self._sz) 
		_quiescence.normalize_MDF(self._sz) 
		_quiescence.write_mdf_output(self._sz[0]) 


	@unittest 
	def test_m_agb(self): 
		r""" 
		vice.src.singlezone.agb.m_agb quiescence test 
		""" 
		def test(): 
			return _quiescence.quiescence_test_m_AGB(self._sz) 
		return ["vice.src.singlezone.agb.m_agb", test] 

