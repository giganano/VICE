# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [ 
	"test_all", 
	"test_custom_mass_distribution", 
	"test_mass_bin_counter", 
	"test_imf_evaluation", 
	"test_builtin_salpeter", 
	"test_builtin_kroupa"  
] 
from ._test_utils import moduletest 
from ._test_utils import unittest 
from . cimport _imf 


def test(run = True): 
	""" 
	Runs all tests in this module 
	""" 
	test = moduletest("VICE Stellar Initial Mass Function Features") 
	test.new(test_custom_mass_distribution()) 
	test.new(test_mass_bin_counter()) 
	test.new(test_imf_evaluation()) 
	test.new(test_builtin_salpeter()) 
	test.new(test_builtin_kroupa()) 
	if run: 
		test.run() 
	else: 
		return test 


def test_custom_mass_distribution(): 
	""" 
	Tests the function which sets a custom mass distribution at 
	vice/src/imf.h 
	""" 
	return unittest("Custom mass distribution", 
		_imf.test_imf_set_mass_distribution) 


def test_mass_bin_counter(): 
	""" 
	Tests the n_mass_bins function at vice/src/imf.h 
	""" 
	return unittest("Mass bin counter", _imf.test_n_mass_bins) 


def test_imf_evaluation(): 
	""" 
	Tests the function which evaluates and imf at vice/src/imf.h 
	""" 
	return unittest("IMF evaluation", _imf.test_imf_evaluate) 


def test_builtin_salpeter(): 
	""" 
	Tests the built-in Salpeter (1955) IMF at vice/src/imf.h 
	""" 
	return unittest("Built-in Salpeter (1955) IMF", _imf.test_salpeter55) 


def test_builtin_kroupa(): 
	""" 
	Tests the built-in Kroupa (2001) IMF at vice/src/imf.h 
	""" 
	return unittest("Built-in Kroupa (2001) IMF", _imf.test_kroupa01) 

