# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_dataset_constructor", 
	"test_dataset_destructor" 
] 
from . cimport _dataset 

_RETURN_VALUE_MESSAGE_ = { 
	1: 		"Success", 
	0: 		"Failure" 
}


def test_dataset_constructor(): 
	""" 
	Test the dataset constructor function at vice/src/objects/dataset.h 
	""" 
	print("Dataset constructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_dataset.test_dataset_initialize()] 
	)) 


def test_dataset_destructor(): 
	""" 
	Test the dataset destructor function at vice/src/objects/dataset.h 
	""" 
	print("Dataset destructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_dataset.test_dataset_free()]
	)) 

