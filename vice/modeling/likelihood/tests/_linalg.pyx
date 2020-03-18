# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_matrix_addition", 
	"test_matrix_subtraction", 
	"test_matrix_transposition", 
	"test_matrix_determinant", 
	"test_matrix_inversion" 
] 
from ....testing import moduletest 
from ....testing import unittest 
from . cimport _linalg 


@moduletest 
def test(): 
	""" 
	Run the tests on this module 
	""" 
	return ["vice.modeling.likelihood.tests.linalg", 
		[ 
			test_matrix_addition(), 
			test_matrix_subtraction(), 
			test_matrix_transposition(), 
			test_matrix_determinant(), 
			test_matrix_inversion() 
		] 
	] 


@unittest 
def test_matrix_addition(): 
	""" 
	Test the matrix addition function at vice/src/modeling/likelihood/linalg.h 
	""" 
	return ["vice.src.modeling.likelihood.linalg.add_matrices", 
		_linalg.test_add_matrices] 


@unittest 
def test_matrix_subtraction(): 
	""" 
	Test the matrix subtraction function at 
	vice/src/modeling/likelihood/linalg.h 
	""" 
	return ["vice.src.modeling.likelihood.linalg.subtract_matrices", 
		_linalg.test_subtract_matrices] 


@unittest 
def test_matrix_transposition(): 
	""" 
	Test the matrix transposition function at 
	vice/src/modeling/likelihood/linalg.h 
	""" 
	return ["vice.src.modeling.likelihood.linalg.transpose", 
		_linalg.test_transpose] 


@unittest 
def test_matrix_determinant(): 
	""" 
	Test the matrix determinant function at 
	vice/src/modeling/likelihood/linalg.h 
	""" 
	return ["vice.src.modeling.likelihood.linalg.determinant", 
		_linalg.test_determinant] 


@unittest 
def test_matrix_inversion(): 
	""" 
	Test the matrix inversion function at 
	vice/src/modeling/likelihood/linalg.h 
	""" 
	return ["vice.src.modeling.likelihood.linalg.invert", 
		_linalg.test_inversion] 

