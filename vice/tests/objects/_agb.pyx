# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [ 
	"test_agb_grid_constructor", 
	"test_agb_grid_destructor" 
] 
from .._test_utils import unittest 
from . cimport _agb 


@unittest 
def test_agb_grid_constructor(): 
	""" 
	Tests the AGB yield grid constructor function at vice/src/objects/agb.h 
	""" 
	return ["AGB yield grid constructor", _agb.test_agb_yield_grid_initialize]  


@unittest 
def test_agb_grid_destructor(): 
	""" 
	Tests the AGB yield grid destructor function at vice/src/objects/agb.h 
	""" 
	return ["AGB yield grid destructor", _agb.test_agb_yield_grid_free] 

