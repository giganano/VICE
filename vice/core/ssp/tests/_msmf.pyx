# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_main_sequence_mass_fraction", 
	"test_setup_main_sequence_mass_fraction" 
] 
from ....testing import unittest 
from . cimport _msmf 


@unittest 
def test_main_sequence_mass_fraction(): 
	""" 
	Test the main sequence mass fraction function at vice/src/ssp/msmf.h 
	""" 
	return ["vice.src.ssp.msmf.MSMF", _msmf.test_MSMF] 


@unittest 
def test_setup_main_sequence_mass_fraction(): 
	""" 
	Test the main sequence mass fraction setup for singlezone simulation at 
	vice/src/ssp/msmf.h 
	""" 
	return ["vice.src.ssp.msmf.setup_MSMF", _msmf.test_setup_MSMF] 

