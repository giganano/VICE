# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [ 
	"test_all", 
	"test_custom_mass_distribution", 
	"test_mass_bin_counter", 
	"test_imf_evaluation", 
	"test_builtin_imfs" 
] 
from ._test_utils import _RETURN_VALUE_MESSAGE_ 
from . cimport _imf 


def test_all(): 
	""" 
	Runs all tests in this module 
	""" 
	test_custom_mass_distribution() 
	test_mass_bin_counter() 
	test_imf_evaluation() 
	test_builtin_imfs() 


def test_custom_mass_distribution(): 
	""" 
	Tests the function which sets a custom mass distribution at 
	vice/src/imf.h 
	""" 
	print("Custom mass distribution: %s" % (
		_RETURN_VALUE_MESSAGE_[_imf.test_imf_set_mass_distribution()] 
	)) 


def test_mass_bin_counter(): 
	""" 
	Tests the n_mass_bins function at vice/src/imf.h 
	""" 
	print("Mass bin counter: %s" % (
		_RETURN_VALUE_MESSAGE_[_imf.test_n_mass_bins()] 
	)) 


def test_imf_evaluation(): 
	""" 
	Tests the function which evaluates and imf at vice/src/imf.h 
	""" 
	print("IMF evaluation: %s" % (
		_RETURN_VALUE_MESSAGE_[_imf.test_imf_evaluate()] 
	)) 


def test_builtin_imfs(): 
	""" 
	Tests the built-in IMFs at vice/src/imf.h 
	""" 
	print("Salpeter (1955) IMF: %s" % (
		_RETURN_VALUE_MESSAGE_[_imf.test_salpeter55()] 
	)) 
	print("Kroupa (2001) IMF: %s" % (
		_RETURN_VALUE_MESSAGE_[_imf.test_kroupa01()] 
	)) 

