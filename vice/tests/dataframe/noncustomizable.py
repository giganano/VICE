""" 
Tests the noncustomizable derived class 
""" 

from __future__ import absolute_import 
__all__ = ["test"] 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ...core.dataframe import noncustomizable 
from .._test_utils import moduletest 
from .._test_utils import unittest 


def test(run = True): 
	""" 
	Run all tests on the noncustomizable derived class 
	""" 
	test = moduletest("Noncustomizable derived class") 
	test.new(unittest("Initialization", test_initialization)) 
	test.new(unittest("Setitem", test_setitem)) 
	if run: 
		test.run() 
	else: 
		return test 


def test_initialization(): 
	""" 
	Tests the initialization of the noncustomizable derived class 
	""" 
	global _TEST_FRAME_ 
	_TEST_FRAME_ = dict(zip(
		_RECOGNIZED_ELEMENTS_, 
		len(_RECOGNIZED_ELEMENTS_) * [1.] 
	)) 
	try: 
		_TEST_FRAME_ = noncustomizable(_TEST_FRAME_, "test") 
	except: 
		return False 
	return isinstance(_TEST_FRAME_, noncustomizable) 


def test_setitem(): 
	""" 
	Test the setitem function, which should always throw a TypeError 
	""" 
	try: 
		_TEST_FRAME_[_RECOGNIZED_ELEMENTS_[0]] = 0.5 
	except TypeError: 
		return True 
	except: 
		return False 
	return False 

