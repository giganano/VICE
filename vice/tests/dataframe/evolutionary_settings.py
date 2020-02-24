""" 
Test the evolutionary settings derived class 
""" 

from __future__ import absolute_import 
__all__ = ["test"] 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ...core.dataframe import evolutionary_settings 
from .._test_utils import moduletest 
from .._test_utils import unittest 


def test(run = True): 
	""" 
	Run all tests on the evolutionary_settings derived class 
	""" 
	test = moduletest("Evolutionary settings derived class") 
	test.new(unittest("Initialization", test_initialization)) 
	test.new(unittest("Setitem", test_setitem)) 
	if run: 
		test.run() 
	else: 
		return test 


def test_initialization(): 
	""" 
	Tests the initialization of the evolutionary_settings derived class 
	""" 
	global _TEST_FRAME_ 
	_TEST_FRAME_ = dict(zip(
		_RECOGNIZED_ELEMENTS_, 
		len(_RECOGNIZED_ELEMENTS_) * [0.]
	)) 
	try: 
		_TEST_FRAME_ = evolutionary_settings(_TEST_FRAME_, "test") 
	except: 
		return False 
	return isinstance(_TEST_FRAME_, evolutionary_settings) 


def test_setitem(): 
	""" 
	Tests the setitem function 
	""" 
	try: 
		for i in _RECOGNIZED_ELEMENTS_: 
			_TEST_FRAME_[i] = 0.5 
	except: 
		return False 
	if _TEST_FRAME_ == evolutionary_settings(dict(zip(
		_RECOGNIZED_ELEMENTS_, 
		len(_RECOGNIZED_ELEMENTS_) * [0.5] 
	)), "test"): 
		try: 
			for i in _RECOGNIZED_ELEMENTS_: 
				_TEST_FRAME_[i] = dummy 
		except: 
			return False 
		return _TEST_FRAME_ == evolutionary_settings(dict(zip(
			_RECOGNIZED_ELEMENTS_, 
			len(_RECOGNIZED_ELEMENTS_) * [dummy] 
		)), "test")  
	else: 
		return False 


def dummy(t): 
	""" 
	A dummy function of time 
	""" 
	return t**2 

