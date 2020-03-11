
from __future__ import absolute_import 
__all__ = ["test"] 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ..._globals import _VERSION_ERROR_ 
from ...core.dataframe._builtin_dataframes import atomic_number 
from ...core.dataframe._builtin_dataframes import sources 
from ...core.dataframe._builtin_dataframes import solar_z 
from ...core.dataframe._builtin_dataframes import primordial  
from .._test_utils import moduletest 
from .._test_utils import unittest 
import numbers 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 


@moduletest 
def test(): 
	""" 
	Test the built-in dataframes 
	""" 
	return ["Built-in Dataframes", 
		[ 
			test_atomic_number(), 
			test_sources(), 
			test_solar_z(), 
			test_primordial() 
		] 
	] 


@unittest 
def test_atomic_number(): 
	""" 
	Atomic number built-in dataframe unit test 
	""" 
	def test():  
		"""" 
		Test the atomic number dataframe 
		""" 
		try: 
			for i in _RECOGNIZED_ELEMENTS_: 
				assert isinstance(atomic_number[i], numbers.Number) 
				assert atomic_number[i] % 1 == 0 
		except: 
			return False 
		return True 
	return ["Atomic number", test] 


@unittest 
def test_sources(): 
	""" 
	Sources built-in dataframe unit test 
	""" 
	def test(): 
		""" 
		Test the sources dataframe 
		""" 
		try: 
			for i in _RECOGNIZED_ELEMENTS_: 
				assert isinstance(sources[i], list) 
				assert all(map(lambda x: isinstance(x, strcomp), sources[i])) 
		except: 
			return False 
		return True 
	return ["Sources", test] 


@unittest 
def test_solar_z(): 
	""" 
	Solar_z built-in dataframe unit test 
	""" 
	def test(): 
		""" 
		Test the solar_z dataframe 
		""" 
		try: 
			for i in _RECOGNIZED_ELEMENTS_: 
				assert isinstance(solar_z[i], numbers.Number) 
				assert 0 < solar_z[i] < 1 
		except: 
			return False 
		return True 
	return ["Solar Z", test] 


@unittest 
def test_primordial(): 
	""" 
	Primordial_z built-in dataframe unit test 
	""" 
	def test(): 
		""" 
		Test the primordial abundances dataframe 
		""" 
		try: 
			for i in _RECOGNIZED_ELEMENTS_: 
				assert isinstance(primordial[i], numbers.Number) 
				if i == "he": 
					assert primordial[i] > 0 
				else: 
					assert primordial[i] == 0 
		except: 
			return False 
		return True 
	return ["Primordial Z", test] 

