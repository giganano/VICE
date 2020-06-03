
from __future__ import absolute_import 
__all__ = ["test"] 
from ....testing import moduletest 
from ....testing import unittest 
from .._builtin_elemental_data import builtin_elemental_data 

_TEST_FRAME_ = {
	"c": 	0.01, 
	"n": 	list(range(5)) 
}


@moduletest 
def test(): 
	r""" 
	vice.core.dataframe.builtin_elemental_data module test 
	""" 
	return ["vice.core.dataframe.builtin_elemental_data", 
		[ 
			test_initialize() 
		] 
	] 


@unittest 
def test_initialize(): 
	r""" 
	vice.core.dataframe.builtin_elemental_data unit test 
	""" 
	def test(): 
		global _TEST_ 
		try: 
			_TEST_ = builtin_elemental_data(_TEST_FRAME_, "test") 
		except: 
			return False 
		return isinstance(_TEST_, builtin_elemental_data) 
	return ["vice.core.dataframe.builtin_elemental_data.__init__", test] 

