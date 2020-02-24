""" 
Tests the saved_yields derived class 
""" 

from __future__ import absolute_import 
__all__ = ["test"] 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ...core.dataframe import saved_yields 
from .._test_utils import moduletest 
from .._test_utils import unittest 


def test(run = True): 
	""" 
	Run all tests on the saved_yields dataframe 
	""" 
	test = moduletest("Saved yields derived class") 
	test.new(unittest("Initialization", test_initialization)) 
	if run: 
		test.run() 
	else: 
		return test 


def test_initialization(): 
	""" 
	Tests the initialization of the dataframe 
	""" 
	# Designed to allow numbers, strings, and functions 
	global _TEST_FRAME_ 
	_TEST_FRAME_ = { 
		"c": 	1.e-3, 
		"n": 	"test", 
		"o": 	lambda x: 0.1 * x 
	} 
	try: 
		_TEST_FRAME_ = saved_yields(_TEST_FRAME_, "test")  
	except: 
		return False 
	return isinstance(_TEST_FRAME_, saved_yields)  

