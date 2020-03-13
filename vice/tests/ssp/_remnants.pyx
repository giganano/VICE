# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = ["test_kalirai08"] 
from .._test_utils import unittest 
from . cimport _remnants 


@unittest 
def test_kalirai08(): 
	""" 
	Test the Kalirai et al. (2008) initial-final remnant mass relation at 
	vice/src/ssp/remnants.h 
	""" 
	return ["Kalirai et al. (2008) initial-final mass relation", 
		_remnants.test_Kalirai08_remnant_mass] 

