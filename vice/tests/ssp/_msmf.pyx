# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_main_sequence_mass_fraction" 
] 
from .._test_utils import unittest 
from . cimport _msmf 


def test_main_sequence_mass_fraction(): 
	""" 
	Tests the main sequence mass fraction function at vice/src/ssp/msmf.h 
	""" 
	return unittest("Main sequence mass fraction", _msmf.test_MSMF) 

