# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_cumulative_return_fraction", 
	"test_setup_cumulative_return_fraction" 
] 
from .._test_utils import unittest 
from . cimport _crf 


@unittest 
def test_cumulative_return_fraction(): 
	""" 
	Test the cumulative return fraction function 
	""" 
	return ["Cumulative return fraction", _crf.test_CRF] 


@unittest 
def test_setup_cumulative_return_fraction(): 
	""" 
	Test the cumulative return fraction setup for singlezone simulation at 
	vice/src/ssp/crf.h 
	""" 
	return ["Setup singlezone cumulative return fraction", _crf.test_setup_CRF] 

