""" 
Test the evolutionary settings derived class 
""" 

from __future__ import absolute_import 
__all__ = ["test"] 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ...core.dataframe import evolutionary_settings 
from .._test_utils import moduletest 
from .._test_utils import unittest 


@moduletest 
def test(): 
	""" 
	Run all tests on the evolutionary_settings derived class 
	""" 
	return ["Evolutionary settings derived class", 
		[ 
			test_initialization(), 
			test_setitem() 
		] 
	] 


@unittest 
def test_initialization(): 
	""" 
	Initialization unit test 
	""" 
	def test(): 
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
	return ["Initialization", test] 


@unittest 
def test_setitem(): 
	""" 
	__setitem__ unit test 
	""" 
	def test(): 
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
		else: 
			return False 
		return _TEST_FRAME_ == evolutionary_settings(dict(zip(
			_RECOGNIZED_ELEMENTS_, 
			len(_RECOGNIZED_ELEMENTS_) * [dummy] 
		)), "test")  
	return ["Setitem", test] 


def dummy(t): 
	""" 
	A dummy function of time 
	""" 
	return t**2 

