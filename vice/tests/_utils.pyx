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
	"test_binspace_generator", 
	"test_bin_center_calculator", 
	"test_summation", 
	"test_string_copier", 
	"test_maximum" 
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
	test.new(test_bin_center_calculator()) 
	test.new(test_summation()) 
	test.new(test_string_copier()) 
	test.new(test_maximum()) 
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


def test_bin_center_calculator(): 
	""" 
	Tests the bin-center calculator at vice/src/utils.h 
	""" 
	return unittest("Bin centers", _utils.test_bin_centers)  


def test_summation(): 
	""" 
	Tests the sum function at vice/src/utils.h 
	""" 
	return unittest("Summation", _utils.test_sum) 


def test_string_copier(): 
	""" 
	Tests the char pointer from PyString function at vice/src/utils.h 
	""" 
	return unittest("Python to C string pipeline", 
		_utils.test_set_char_p_value) 


def test_maximum(): 
	""" 
	Tests the max function at vice/src/utils.h 
	""" 
	return unittest("Maximum", _utils.test_max) 

