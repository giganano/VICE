# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_callback_1arg_constructor",
	"test_callback_1arg_destructor"
]
from ....testing import unittest
from . cimport _callback_1arg


@unittest
def test_callback_1arg_constructor():
	"""
	Tests the callback_1arg constructor function at
	vice/src/objects/callback_1arg.h
	"""
	return ["vice.src.objects.callback_1arg constructor",
		_callback_1arg.test_callback_1arg_initialize]


@unittest
def test_callback_1arg_destructor():
	"""
	Tests the callback_1arg destructor function at
	vice/src/objects/callback_1arg.h
	"""
	return ["vice.src.objects.callback_1arg destructor",
		_callback_1arg.test_callback_1arg_free]

