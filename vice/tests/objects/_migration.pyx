# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_migration_constructor", 
	"test_migration_destructor" 
] 
from . cimport _migration 

_RETURN_VALUE_MESSAGE_ = { 
	1: 		"Success", 
	0: 		"Failure" 
}


def test_migration_constructor(): 
	""" 
	Tests the migration constructor function at vice/src/objects/migration.h 
	""" 
	print("Migration constructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_migration.test_migration_initialize()] 
	)) 


def test_migration_destructor(): 
	""" 
	Tests the migration destructor functioon at vice/src/objects/migration.h 
	""" 
	print("Migration destructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_migration.test_migration_free()] 
	)) 

