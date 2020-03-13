# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = ["test"] 
from ._test_utils import moduletest 
from ._test_utils import unittest 
from . cimport _callback 


@moduletest 
def test(): 
	""" 
	Tests the callback object function evaluations 
	""" 
	return ["Callback objects", 
		[ 
			test_callback1_evaluate(), 
			test_callback2_evaluate() 
		] 
	] 


@unittest 
def test_callback1_evaluate(): 
	""" 
	Tests the callback evaluation with one parameter at vice/src/callback.h 
	""" 
	return ["1 argument", _callback.test_callback_1arg_evaluate] 


@unittest 
def test_callback2_evaluate(): 
	""" 
	Tests the callback evaluation with two parameters at vice/src/callback.h 
	""" 
	return ["2 arguments", _callback.test_callback_2arg_evaluate] 

