# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_cumulative_return_fraction" 
] 
from .._test_utils import unittest 
from . cimport _crf 

def test_cumulative_return_fraction(): 
	""" 
	Test the cumulative return fraction function 
	""" 
	return unittest("Cumulative return fraction", _crf.test_CRF) 

