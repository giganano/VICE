# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_channel_constructor", 
	"test_channel_destructor" 
] 
from .._test_utils import unittest 
from . cimport _channel 


def test_channel_constructor(): 
	""" 
	Tests the channel constructor function at vice/src/objects/channel.h 
	""" 
	return unittest("Arbitrary enrichment channel constructor", 
		_channel.test_channel_initialize) 


def test_channel_destructor(): 
	""" 
	Tests the channel destructor function at vice/src/objects/channel.h 
	""" 
	return unittest("Arbitrary enrichment channel destructor", 
		_channel.test_channel_free) 

