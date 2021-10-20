# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_channel_constructor",
	"test_channel_destructor"
]
from ....testing import unittest
from . cimport _channel


@unittest
def test_channel_constructor():
	"""
	Tests the channel constructor function at vice/src/objects/channel.h
	"""
	return ["vice.src.objects.channel constructor",
		_channel.test_channel_initialize]


@unittest
def test_channel_destructor():
	"""
	Tests the channel destructor function at vice/src/objects/channel.h
	"""
	return ["vice.src.objects.channel destructor", _channel.test_channel_free]

