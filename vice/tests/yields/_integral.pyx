# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_euler", 
	"test_trapezoid", 
	"test_midpoint", 
	"test_simpson" 
] 
from .._test_utils import _RETURN_VALUE_MESSAGE_ 
from . cimport _integral 


def test_euler(): 
	""" 
	Tests the euler's method integration routine at vice/src/yields/integral.c 
	""" 
	print("Euler's method integration: %s" % (
		_RETURN_VALUE_MESSAGE_[_integral.test_quad_euler()] 
	)) 


def test_trapezoid(): 
	""" 
	Tests the trapezoid rule integration routine at vice/src/yields/integral.c 
	""" 
	print("Trapezoid rule integration: %s" % (
		_RETURN_VALUE_MESSAGE_[_integral.test_quad_trapzd()] 
	)) 


def test_midpoint(): 
	""" 
	Tests the midpoint rule integration routine at vice/src/yields/integral.c 
	""" 
	print("Midpoint rule integration: %s" % (
		_RETURN_VALUE_MESSAGE_[_integral.test_quad_midpt()] 
	)) 


def test_simpson(): 
	""" 
	Tests the Simpson's rule integration routine at vice/src/yields/integral.c 
	""" 
	print("Simpson's rule integration: %s" % (
		_RETURN_VALUE_MESSAGE_[_integral.test_quad_simp()] 
	)) 

