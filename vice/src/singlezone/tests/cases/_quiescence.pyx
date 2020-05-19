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
def tau_star_inf(): 
	r""" 
	Runs a quiescence edge-case tests on a simulation in which the attribute 
	tau_star is set to infinity. 
	""" 
	return [
		"vice.core.singlezone edge case : quiescence [tau_star = infinity]", 
		quiescence_test(tau_star = lambda t: float("inf"), 
			smoothing = 10)  
	] 


def quiescence_test(**kwargs): 
	r""" 
	Run a quiescence edge-case test. These are defined as parameter spaces 
	which yield no star formation, and thus no elemental production. This 
	module test ensures that these conditions are met. 

	Parameters 
	----------
	kwargs : varying types 
		The keyword arguments to set as attributes of the singlezone class. 
		Assumed to produce quiescence. 

	Returns 
	-------
	tests : list 
		The unit tests to return as a part of the moduletest object. 
		None if the quiescence class can not be instantiated. 
	""" 
	try: 
		_TEST_ = quiescence(**kwargs)  
	except: 
		return None 
	return [ 
		_TEST_.test_m_agb(), 
		_TEST_.test_m_ccsne(), 
		_TEST_.test_update_element_mass(), 
		_TEST_.test_onH(), 
		_TEST_.test_update_gas_evolution(), 
		_TEST_.test_get_outflow_rate(), 
		_TEST_.test_singlezone_unretained() 
	] 



cdef class quiescence: 

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

	@unittest 
	def test_m_ccsne(self): 
		r""" 
		vice.src.singlezone.ccsne.m_ccsne quiescence test 
		""" 
		def test(): 
			return _quiescence.quiescence_test_m_ccsne(self._sz) 
		return ["vice.src.singlezone.ccsne.m_ccsne", test] 

	@unittest 
	def test_update_element_mass(self): 
		r""" 
		vice.src.singlezone.element.update_element_mass quiescence test 
		""" 
		def test(): 
			return _quiescence.quiescence_test_update_element_mass(self._sz) 
		return ["vice.src.singlezone.element.update_element_mass", test] 

	@unittest 
	def test_onH(self): 
		r""" vice.src.singlezone.element.onH quiescence test 
		""" 
		def test(): 
			return _quiescence.quiescence_test_onH(self._sz) 
		return ["vice.src.singlezone.element.onH", test] 

	@unittest 
	def test_update_gas_evolution(self): 
		r""" 
		vice.src.singlezone.ism.update_gas_evolution quiescence test 
		""" 
		def test(): 
			return _quiescence.quiescence_test_update_gas_evolution(self._sz) 
		return ["vice.src.singlezone.ism.update_gas_evolution", test] 

	@unittest 
	def test_get_outflow_rate(self): 
		r""" 
		vice.src.singlezone.ism.get_outflow_rate quiescence test 
		""" 
		def test(): 
			return _quiescence.quiescence_test_get_outflow_rate(self._sz) 
		return ["vice.src.singlezone.ism.get_outflow_rate", test] 

	@unittest 
	def test_singlezone_unretained(self): 
		r""" 
		vice.src.singlezone.ism.singlezone_unretained quiescence test 
		""" 
		def test(): 
			return _quiescence.quiescence_test_singlezone_unretained(self._sz) 
		return ["vice.src.singlezone.ism.singlezone_unretained", test] 

