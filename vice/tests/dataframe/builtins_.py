
from __future__ import absolute_import 
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


def test(run = True): 
	""" 
	Test the built-in dataframes 
	""" 
	test = moduletest("Built-in Dataframes") 
	test.new(unittest("Atomic number", test_atomic_number)) 
	test.new(unittest("Sources", test_sources)) 
	test.new(unittest("Solar Z", test_solar_z)) 
	test.new(unittest("Primordial Z", test_primordial)) 
	if run: 
		test.run() 
	else: 
		return test 


def test_atomic_number(): 
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


def test_sources(): 
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


def test_solar_z(): 
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


def test_primordial(): 
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

