""" 
Tests the noncustomizable derived class 
""" 

from __future__ import absolute_import 
__all__ = ["test"] 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ...core.dataframe import noncustomizable 
from .._test_utils import moduletest 
from .._test_utils import unittest 


@moduletest 
def test(): 
	""" 
	Run all tests on the noncustomizable derived class 
	""" 
	return ["Noncustomizable derived class", 
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
	return ["Initialization", test] 


@unittest 
def test_setitem(): 
	""" 
	__setitem__ unit test 
	""" 
	def test(): 
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
	return ["Setitem", test] 

