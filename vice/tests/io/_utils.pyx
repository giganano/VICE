# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test", 
	"test_square_ascii_reader", 
	"test_header_length_finder", 
	"test_file_dimension_finder", 
	"test_line_counter"  
] 
from .._test_utils import moduletest 
from .._test_utils import unittest 
from . cimport _utils 


@moduletest 
def test(): 
	""" 
	Test all files in this module 
	""" 
	return ["VICE File I/O Utility Functions", 
		[ 
			test_square_ascii_reader(), 
			test_header_length_finder(), 
			test_file_dimension_finder(), 
			test_line_counter() 
		] 
	] 


@unittest 
def test_square_ascii_reader(): 
	""" 
	Tests the square ascii file reader at vice/src/io/utils.h 
	""" 
	return ["Square ascii file reader", _utils.test_read_square_ascii_file] 


@unittest 
def test_header_length_finder(): 
	""" 
	Tests the header length finder vice/src/io/utils.h 
	""" 
	return ["Header length finder", _utils.test_header_length] 


@unittest 
def test_file_dimension_finder(): 
	""" 
	Tests the file dimension finder at vice/src/io/utils.h 
	""" 
	return ["File dimension finder", _utils.test_file_dimension] 


@unittest 
def test_line_counter(): 
	""" 
	Tests the line counter at vice/src/io/utils.h 
	""" 
	return ["Line counter", _utils.test_line_count] 

