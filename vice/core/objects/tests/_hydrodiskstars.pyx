# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_hydrodiskstars_constructor",
	"test_hydrodiskstars_destructor"
]
from ....testing import unittest
from . cimport _hydrodiskstars


@unittest
def test_hydrodiskstars_constructor():
	r"""
	Test the hydrodiskstars constructor at vice/src/objects/hydrodiskstars.h
	"""
	return ["vice.src.objects.hydrodiskstars constructor",
		_hydrodiskstars.test_hydrodiskstars_initialize]


@unittest
def test_hydrodiskstars_destructor():
	r"""
	Test the hydrodiskstars destructor at vice/src/objects/hydrodiskstars.h
	"""
	return ["vice.src.objects.hydrodiskstars destructor",
		_hydrodiskstars.test_hydrodiskstars_free]

