# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_all", 
	"test_choose_operation", 
	"test_absolute_value", 
	"test_sign_function", 
	"test_hash_codes", 
	"test_pseudorandom_generator", 
	"test_1D_interpolation", 
	"test_2D_interpolation", 
	"test_bin_number_finder", 
	"test_binspace_generator" 
] 
from ._test_utils import moduletest 
from ._test_utils import unittest 
from . cimport _utils 


def test(run = True): 
	""" 
	Tests all of VICE's utility functions at vice/src/utils.h 
	""" 
	test = moduletest("VICE utility functions") 
	test.new(test_choose_operation()) 
	test.new(test_absolute_value()) 
	test.new(test_sign_function()) 
	test.new(test_hash_codes()) 
	test.new(test_pseudorandom_generator()) 
	test.new(test_1D_interpolation()) 
	test.new(test_2D_interpolation()) 
	test.new(test_bin_number_finder()) 
	test.new(test_binspace_generator()) 
	if run: 
		test.run() 
	else: 
		return test 


def test_choose_operation(): 
	""" 
	Tests the choose operation at vice/src/utils.h 
	""" 
	return unittest("Choose operation", _utils.test_choose) 


def test_absolute_value(): 
	""" 
	Tests the absolute value function at vice/src/utils.h 
	""" 
	return unittest("Absolute value", _utils.test_absval) 


def test_sign_function(): 
	""" 
	Tests the sign function at vice/src/utils.h 
	""" 
	return unittest("Sign function", _utils.test_sign) 


def test_hash_codes(): 
	""" 
	Tests the hash-code function at vice/src/utils.h 
	""" 
	return unittest("Simple hash", _utils.test_simple_hash) 


def test_pseudorandom_generator(): 
	""" 
	Tests the pseudorandom number generator at vice/src/utils.h 
	""" 
	return unittest("Pseudorandom number generator", _utils.test_rand_range) 


def test_1D_interpolation(): 
	""" 
	Tests the 1D interpolation function at vice/src/utils.h 
	""" 
	return unittest("1-dimensional interpolation", _utils.test_interpolate) 


def test_2D_interpolation(): 
	""" 
	Tests the 2D interpolation function at vice/src/utils.h 
	""" 
	return unittest("2-dimensional interpolation", _utils.test_interpolate2D) 


def test_bin_number_finder(): 
	""" 
	Tests the bin number finder at vice/src/utils.h 
	""" 
	return unittest("Bin number finder", _utils.test_get_bin_number) 


def test_binspace_generator(): 
	""" 
	Tests the binspace generator at vice/src/utils.h 
	""" 
	return unittest("Binspace generator", _utils.test_binspace) 

