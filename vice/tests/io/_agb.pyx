# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_agb_grid_import" 
] 
from .._test_utils import unittest 
from . cimport _agb 


def test_agb_grid_import(): 
	""" 
	Tests the AGB star yield grid import function at vice/src/io/agb.h 
	""" 
	return unittest("AGB Star yield grid import", _agb.test_import_agb_grid) 

