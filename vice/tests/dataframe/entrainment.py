""" 
Tests the channel_entrainment derived class 
""" 

from __future__ import absolute_import 
__all__ = ["test"] 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ...core.dataframe import channel_entrainment 
from .._test_utils import moduletest 
from .._test_utils import unittest 


def test(run = True): 
	""" 
	Run all tests on the channel_entrainment derived class 
	""" 
	test = moduletest("Entrainment settings derived class") 
	test.new(unittest("Initialization", test_initialization)) 
	test.new(unittest("Setitem", test_setitem)) 
	if run: 
		test.run() 
	else: 
		return test 


def test_initialization(): 
	""" 
	Tests the initialization of the channel_entrainment derived class 
	""" 
	global _TEST_FRAME_ 
	_TEST_FRAME_ = dict(zip(
		_RECOGNIZED_ELEMENTS_, 
		len(_RECOGNIZED_ELEMENTS_) * [1.] 
	)) 
	try: 
		_TEST_FRAME_ = channel_entrainment(_TEST_FRAME_) 
	except: 
		return False 
	return isinstance(_TEST_FRAME_, channel_entrainment) 


def test_setitem(): 
	""" 
	Tests the __setitem__ function 
	""" 
	try: 
		for i in _RECOGNIZED_ELEMENTS_: 
			_TEST_FRAME_[i] = 0.5 
	except: 
		return False 
	return _TEST_FRAME_ == channel_entrainment(dict(zip(
		_RECOGNIZED_ELEMENTS_, 
		len(_RECOGNIZED_ELEMENTS_) * [0.5] 
	))) 

