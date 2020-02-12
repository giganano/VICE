# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_channel_constructor", 
	"test_channel_destructor" 
] 
from . cimport _channel 

_RETURN_VALUE_MESSAGE_ = {
	1: 		"Success", 
	0: 		"Failure" 
}


def test_channel_constructor(): 
	""" 
	Tests the channel constructor function at vice/src/objects/channel.h 
	""" 
	print("Channel constructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_channel.test_channel_initialize()] 
	)) 


def test_channel_destructor(): 
	""" 
	Tests the channel destructor function at vice/src/objects/channel.h 
	""" 
	print("Channel destructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_channel.test_channel_free()] 
	)) 

