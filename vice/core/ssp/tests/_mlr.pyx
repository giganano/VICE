# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_mass_lifetime_relationship" 
] 
from ....testing import unittest 
from . cimport _mlr 


@unittest 
def test_mass_lifetime_relationship(): 
	""" 
	Tests the mass lifetime relationship function implemented at 
	vice/src/ssp/mlr.h 
	""" 
	return ["vice.src.ssp.mlr.main_sequence_turnoff_mass", 
		_mlr.test_main_sequence_turnoff_mass] 

