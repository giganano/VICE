# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_callback_2arg_constructor",
	"test_callback_2arg_destructor"
]
from ....testing import unittest
from . cimport _callback_2arg


@unittest
def test_callback_2arg_constructor():
	"""
	Tests the callback_2arg constructor function at
	vice/src/objects/callback_2arg.h
	"""
	return ["vice.src.objects.callback_2arg constructor",
		_callback_2arg.test_callback_2arg_initialize]


@unittest
def test_callback_2arg_destructor():
	"""
	Tests the callback_2arg destructor function at
	vice/src/objects/callback_2arg.h
	"""
	return ["vice.src.objects.callback_2arg destructor",
		_callback_2arg.test_callback_2arg_free]

