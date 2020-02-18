# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_ccsn_yield_grid_reader" 
] 
from .._test_utils import unittest 
from . cimport _ccsne 


def test_ccsn_yield_grid_reader(): 
	""" 
	Tests the CCSN yield grid reader at vice/src/io/ccsne.h 
	""" 
	return unittest("CCSN yield grid reader", _ccsne.test_cc_yield_grid) 

