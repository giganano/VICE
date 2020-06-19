# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import 
__all__ = [
	"test_repfunc_constructor", 
	"test_repfunc_destructor" 
] 
from ....testing import unittest 
from . cimport _repfunc 


@unittest 
def test_repfunc_constructor(): 
	r""" 
	Tests the repaired function constructor at vice/src/objects/repfunc.h 
	""" 
	return ["vice.src.objects.repfunc constructor", 
		_repfunc.test_repfunc_initialize] 


@unittest 
def test_repfunc_destructor(): 
	r""" 
	Tests the repaired function destructor at vice/src/objects/repfunc.h 
	""" 
	return ["vice.src.objects.repfunc destructor", 
		_repfunc.test_repfunc_free] 

