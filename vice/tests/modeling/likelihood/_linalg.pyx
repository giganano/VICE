# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_matrix_addition", 
	"test_matrix_subtraction", 
	"test_matrix_transposition", 
	"test_matrix_determinant", 
	"test_matrix_inversion" 
] 
from ..._test_utils import unittest 
from . cimport _linalg 



def test_matrix_addition(): 
	""" 
	Test the matrix addition function at vice/src/modeling/likelihood/linalg.h 
	""" 
	return unittest("Matrix addition", _linalg.test_add_matrices) 


def test_matrix_subtraction(): 
	""" 
	Test the matrix subtraction function at 
	vice/src/modeling/likelihood/linalg.h 
	""" 
	return unittest("Matrix subtraction", _linalg.test_subtract_matrices) 


def test_matrix_transposition(): 
	""" 
	Test the matrix transposition function at 
	vice/src/modeling/likelihood/linalg.h 
	""" 
	return unittest("Matrix transposition", _linalg.test_transpose) 


def test_matrix_determinant(): 
	""" 
	Test the matrix determinant function at 
	vice/src/modeling/likelihood/linalg.h 
	""" 
	return unittest("Matrix determinant", _linalg.test_determinant) 


def test_matrix_inversion(): 
	""" 
	Test the matrix inversion function at 
	vice/src/modeling/likelihood/linalg.h 
	""" 
	return unittest("Matrix inversion", _linalg.test_inversion) 

