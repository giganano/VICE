# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = ["test"]
from ...testing import moduletest
from ...testing import unittest
from . cimport _callback


@moduletest
def test():
	"""
	Tests the callback object function evaluations
	"""
	return ["vice.src.callback",
		[
			test_callback1_evaluate(),
			test_callback2_evaluate()
		]
	]


@unittest
def test_callback1_evaluate():
	"""
	Tests the callback evaluation with one parameter at vice/src/callback.h
	"""
	return ["vice.src.callback.callback_1arg_evaluate",
		_callback.test_callback_1arg_evaluate]


@unittest
def test_callback2_evaluate():
	"""
	Tests the callback evaluation with two parameters at vice/src/callback.h
	"""
	return ["vice.src.callback.callback_2arg_evaluate",
		_callback.test_callback_2arg_evaluate]

