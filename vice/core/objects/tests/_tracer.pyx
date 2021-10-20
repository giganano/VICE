# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_tracer_constructor",
	"test_tracer_destructor"
]
from ....testing import unittest
from . cimport _tracer


@unittest
def test_tracer_constructor():
	"""
	Tests the tracer constructor function at vice/src/objects/tracer.h
	"""
	return ["vice.src.objects.tracer constructor",
		_tracer.test_tracer_initialize]


@unittest
def test_tracer_destructor():
	"""
	Tests the tracer destructor function at vice/src/objects/tracer.h
	"""
	return ["vice.src.objects.tracer destructor", _tracer.test_tracer_free]

