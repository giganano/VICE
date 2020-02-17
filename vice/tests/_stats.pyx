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


def test(run = True): 
	""" 
	Run all tests in this module 
	""" 
	test = moduletest("VICE statistical functions") 
	test.new(test_gaussian_sampler()) 
	test.new(test_conversion_to_pdf()) 
	if run: 
		test.run() 
	else: 
		return test 


def test_gaussian_sampler(): 
	""" 
	Test the gaussian sampler at vice/src/stats.h 
	""" 
	return unittest("Gaussian sampler", _stats.test_normal) 


def test_conversion_to_pdf(): 
	""" 
	Test the conversion to PDF function at vice/src/stats.h 
	""" 
	return unittest("Conversion to PDF", _stats.test_convert_to_PDF) 

