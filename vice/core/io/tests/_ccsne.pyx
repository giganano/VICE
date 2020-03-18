# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_ccsn_yield_grid_reader" 
] 
from ....tests._test_utils import moduletest 
from ....tests._test_utils import unittest 
from . cimport _ccsne 


@moduletest 
def test(): 
	""" 
	Run the tests on this module 
	""" 
	return ["vice.src.io.ccsne", 
		[ 
			test_ccsn_yield_grid_reader()
		] 
	] 


@unittest 
def test_ccsn_yield_grid_reader(): 
	""" 
	Tests the CCSN yield grid reader at vice/src/io/ccsne.h 
	""" 
	return ["vice.src.io.ccsne.cc_yield_grid", _ccsne.test_cc_yield_grid] 

