# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_migration_constructor",
	"test_migration_destructor"
]
from ....testing import unittest
from . cimport _migration


@unittest
def test_migration_constructor():
	"""
	Tests the migration constructor function at vice/src/objects/migration.h
	"""
	return ["vice.src.objects.migration constructor",
		_migration.test_migration_initialize]


@unittest
def test_migration_destructor():
	"""
	Tests the migration destructor functioon at vice/src/objects/migration.h
	"""
	return ["vice.src.objects.migration destructor",
		_migration.test_migration_free]

