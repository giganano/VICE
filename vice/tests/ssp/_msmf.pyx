# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_main_sequence_mass_fraction", 
	"test_setup_main_sequence_mass_fraction" 
] 
from .._test_utils import unittest 
from . cimport _msmf 


@unittest 
def test_main_sequence_mass_fraction(): 
	""" 
	Test the main sequence mass fraction function at vice/src/ssp/msmf.h 
	""" 
	return ["Main sequence mass fraction", _msmf.test_MSMF] 


@unittest 
def test_setup_main_sequence_mass_fraction(): 
	""" 
	Test the main sequence mass fraction setup for singlezone simulation at 
	vice/src/ssp/msmf.h 
	""" 
	return ["Setup singlezone main sequence mass fraction", 
		_msmf.test_setup_MSMF] 

