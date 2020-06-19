# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test", 
	"test_evaluate" 
] 
from ....testing import moduletest 
from ....testing import unittest 
from . cimport _repfunc 


@moduletest 
def test(): 
	r""" 
	vice.src.repfunc module test 
	""" 
	return ["vice.src.repfunc", 
		[ 
			test_evaluate() 
		] 
	] 


@unittest 
def test_evaluate(): 
	r""" 
	vice.src.repfunc.repfunc_evaluate unit test 
	""" 
	return ["vice.src.repfunc.repfunc_evalute", _repfunc.test_repfunc_evaluate] 

