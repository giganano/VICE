# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_matrix_addition", 
	"test_matrix_subtraction", 
	"test_matrix_transposition", 
	"test_matrix_determinant", 
	"test_matrix_inversion" 
]
from . cimport _linalg 

_RETURN_VALUE_MESSAGE_ = {
	1: 		"Success", 
	0: 		"Failure" 
}

def test_matrix_addition(): 
	""" 
	Test the matrix addition function at vice/src/modeling/likelihood/linalg.h 
	""" 
	print("Matrix addition: %s" % (
		_RETURN_VALUE_MESSAGE_[_linalg.test_add_matrices()]
	)) 


def test_matrix_subtraction(): 
	""" 
	Test the matrix subtraction function at 
	vice/src/modeling/likelihood/linalg.h 
	""" 
	print("Matrix subtraction: %s" % (
		_RETURN_VALUE_MESSAGE_[_linalg.test_subtract_matrices()]
	)) 


def test_matrix_transposition(): 
	""" 
	Test the matrix transposition function at 
	vice/src/modeling/likelihood/linalg.h 
	""" 
	print("Matrix transposition: %s" % (
		_RETURN_VALUE_MESSAGE_[_linalg.test_transpose()]
	)) 


def test_matrix_determinant(): 
	""" 
	Test the matrix determinant function at 
	vice/src/modeling/likelihood/linalg.h 
	""" 
	print("Matrix determinant: %s" % (
		_RETURN_VALUE_MESSAGE_[_linalg.test_determinant()]
	)) 


def test_matrix_inversion(): 
	""" 
	Test the matrix inversion function at 
	vice/src/modeling/likelihood/linalg.h 
	""" 
	print("Matrix inversion: %s" % (
		_RETURN_VALUE_MESSAGE_[_linalg.test_inversion()]
	)) 

