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


_TEST_FRAME_ = elemental_settings(dict(zip(
	_RECOGNIZED_ELEMENTS_, 
	len(_RECOGNIZED_ELEMENTS_) * [list(range(10))] 
)))  


def test(run = True): 
	""" 
	Tests the elemental_settings derived class of the VICE dataframe 
	""" 
	test = moduletest("Elemental settings derived class") 
	test.new(unittest("getitem", test_getitem)) 
	if run: 
		test.run() 
	else: 
		return test 


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

