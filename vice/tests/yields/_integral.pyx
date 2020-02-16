# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [ 
	"test", 
	"test_euler", 
	"test_trapezoid", 
	"test_midpoint", 
	"test_simpson" 
] 
from .._test_utils import moduletest 
from .._test_utils import unittest 
from . cimport _integral 


def test(run = True): 
	""" 
	Tests this module 
	""" 
	test = moduletest("VICE Numerical Integration Functions") 
	test.new(test_euler()) 
	test.new(test_trapezoid()) 
	test.new(test_midpoint()) 
	test.new(test_simpson()) 
	if run: 
		test.run() 
	else: 
		return test 


def test_euler(): 
	""" 
	Tests the euler's method integration routine at vice/src/yields/integral.c 
	""" 
	return unittest("Euler's method", _integral.test_quad_euler) 


def test_trapezoid(): 
	""" 
	Tests the trapezoid rule integration routine at vice/src/yields/integral.c 
	""" 
	return unittest("Trapezoid rule", _integral.test_quad_trapzd) 


def test_midpoint(): 
	""" 
	Tests the midpoint rule integration routine at vice/src/yields/integral.c 
	""" 
	return unittest("Midpoint rule", _integral.test_quad_midpt) 


def test_simpson(): 
	""" 
	Tests the Simpson's rule integration routine at vice/src/yields/integral.c 
	""" 
	return unittest("Simpson's rule", _integral.test_quad_simp) 

