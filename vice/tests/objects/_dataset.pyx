# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_dataset_constructor", 
	"test_dataset_destructor" 
] 
from .._test_utils import unittest 
from . cimport _dataset 


def test_dataset_constructor(): 
	""" 
	Test the dataset constructor function at vice/src/objects/dataset.h 
	""" 
	return unittest("Dataset destructor", 
		_dataset.test_dataset_initialize) 


def test_dataset_destructor(): 
	""" 
	Test the dataset destructor function at vice/src/objects/dataset.h 
	""" 
	return unittest("Dataset destructor", 
		_dataset.test_dataset_free) 

