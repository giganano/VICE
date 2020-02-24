""" 
Test the elemental_settings derived class 
""" 

from __future__ import absolute_import 
__all__ = ["test"] 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ...core.dataframe import elemental_settings 
from ...core.dataframe import base 
from .._test_utils import moduletest 
from .._test_utils import unittest 


def test(run = True): 
	""" 
	Tests the elemental_settings derived class of the VICE dataframe 
	""" 
	test = moduletest("Elemental settings derived class") 
	test.new(unittest("Initialization", test_initialization)) 
	test.new(unittest("Getitem", test_getitem)) 
	test.new(unittest("Remove", test_remove)) 
	if run: 
		test.run() 
	else: 
		return test 


def test_initialization(): 
	""" 
	Tests the initialization of the elemental_settings derived class 
	""" 
	global _TEST_FRAME_ 
	_TEST_FRAME_ = dict(zip(
		_RECOGNIZED_ELEMENTS_, 
		len(_RECOGNIZED_ELEMENTS_) * [list(range(10))] 
	)) 
	try: 
		_TEST_FRAME_ = elemental_settings(_TEST_FRAME_) 
	except: 
		return False 
	return isinstance(_TEST_FRAME_, elemental_settings) 


def test_getitem(): 
	""" 
	Tests the getitem function 
	""" 
	try: 
		for i in _RECOGNIZED_ELEMENTS_: 
			assert _TEST_FRAME_[i] == list(range(10)) 
	except: 
		return False 
	return True 


def test_remove(): 
	""" 
	Tests the remove function, which should always throw a TypeError 
	""" 
	try: 
		_TEST_FRAME_.remove(_RECOGNIZED_ELEMENTS_[0]) 
	except TypeError: 
		return True 
	except: 
		return False 
	return False 

