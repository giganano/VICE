# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_ia_yield_lookup" 
] 
from .._test_utils import unittest 
from . cimport _sneia 


def test_ia_yield_lookup(): 
	""" 
	Test the SN Ia mass yield lookup function at vice/src/io/sneia.h 
	""" 
	return unittest("SN Ia yield lookup", 
		_sneia.test_single_ia_mass_yield_lookup) 

