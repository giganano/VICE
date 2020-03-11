# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test", 
	"test_gaussian_sampler", 
	"test_conversion_to_pdf" 
] 
from ._test_utils import moduletest 
from ._test_utils import unittest 
from . cimport _stats 


@moduletest 
def test(): 
	""" 
	Run all tests in this module 
	""" 
	return ["VICE statistical function", 
		[
			test_gaussian_sampler(), 
			test_conversion_to_pdf(), 
		] 
	] 


@unittest 
def test_gaussian_sampler(): 
	""" 
	Test the gaussian sampler at vice/src/stats.h 
	""" 
	return ["Gaussian sampler", _stats.test_normal] 


@unittest 
def test_conversion_to_pdf(): 
	""" 
	Test the conversion to PDF function at vice/src/stats.h 
	""" 
	return ["Conversion to PDF", _stats.test_convert_to_PDF] 

