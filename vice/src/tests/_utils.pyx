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
	"test_sqrtx_interpolation",
	"test_bin_number_finder",
	"test_binspace_generator",
	"test_bin_center_calculator",
	"test_summation",
	"test_string_copier",
	"test_maximum"
]
from ...testing import moduletest
from ...testing import unittest
from . cimport _utils


@moduletest
def test():
	"""
	Run the tests on this module
	"""
	return ["vice.src.utils",
		[
			test_choose_operation(),
			test_absolute_value(),
			test_sign_function(),
			test_hash_codes(),
			test_pseudorandom_generator(),
			test_1D_interpolation(),
			test_2D_interpolation(),
			test_sqrtx_interpolation(),
			test_bin_number_finder(),
			test_binspace_generator(),
			test_bin_center_calculator(),
			test_summation(),
			test_string_copier(),
			test_maximum()
		]
	]


@unittest
def test_choose_operation():
	"""
	Tests the choose operation at vice/src/utils.h
	"""
	return ["vice.src.utils.choose", _utils.test_choose]


@unittest
def test_absolute_value():
	"""
	Tests the absolute value function at vice/src/utils.h
	"""
	return ["vice.src.utils.absval", _utils.test_absval]


@unittest
def test_sign_function():
	"""
	Tests the sign function at vice/src/utils.h
	"""
	return ["vice.src.utils.sign", _utils.test_sign]


@unittest
def test_hash_codes():
	"""
	Tests the hash-code function at vice/src/utils.h
	"""
	return ["vice.src.utils.simple_hash", _utils.test_simple_hash]


@unittest
def test_pseudorandom_generator():
	"""
	Tests the pseudorandom number generator at vice/src/utils.h
	"""
	return ["vice.src.utils.rand_range", _utils.test_rand_range]


@unittest
def test_1D_interpolation():
	"""
	Tests the 1D interpolation function at vice/src/utils.h
	"""
	return ["vice.src.utils.interpolate", _utils.test_interpolate]


@unittest
def test_2D_interpolation():
	"""
	Tests the 2D interpolation function at vice/src/utils.h
	"""
	return ["vice.src.utils.interpolate2D", _utils.test_interpolate2D]


@unittest
def test_sqrtx_interpolation():
	"""
	Tests the sqrt(x) interpolation function at vice/src/utils.h
	"""
	return ["vice.src.utils.interpolate_sqrt", _utils.test_interpolate_sqrt]


@unittest
def test_bin_number_finder():
	"""
	Tests the bin number finder at vice/src/utils.h
	"""
	return ["vice.src.utils.get_bin_number", _utils.test_get_bin_number]


@unittest
def test_binspace_generator():
	"""
	Tests the binspace generator at vice/src/utils.h
	"""
	return ["vice.src.utils.binspace", _utils.test_binspace]


@unittest
def test_bin_center_calculator():
	"""
	Tests the bin-center calculator at vice/src/utils.h
	"""
	return ["vice.src.utils.bin_centers", _utils.test_bin_centers]


@unittest
def test_summation():
	"""
	Tests the sum function at vice/src/utils.h
	"""
	return ["vice.src.utils.sum", _utils.test_sum]


@unittest
def test_string_copier():
	"""
	Tests the char pointer from PyString function at vice/src/utils.h
	"""
	return ["vice.src.utils.set_char_p_value", _utils.test_set_char_p_value]


@unittest
def test_maximum():
	"""
	Tests the max function at vice/src/utils.h
	"""
	return ["vice.src.utils.max", _utils.test_max]

