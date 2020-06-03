
from __future__ import absolute_import 
__all__ = ["test_tracers_row"] 
from ....testing import unittest 
from ....core.dataframe import base 
from ....core.outputs import stars 
import numbers 


@unittest 
def test_tracers_row(): 
	r""" 
	vice.core.dataframe.tracers.__getitem__.row unit test 
	""" 
	def test(): 
		r""" 
		This funciton will only be called after the test.vice multizone output 
		has been produced by the module test which calls this. 
		""" 
		try: 
			_TEST_ = stars("test") 
			for i in range(_TEST_.size[0]): 
				assert isinstance(_TEST_[i], base) 
				assert _TEST_[i].keys() == _TEST_.keys() 
				assert all(map(lambda x: isinstance(x, numbers.Number), 
					[_TEST_[i][j] for j in _TEST_.keys()])) 
		except: 
			return False 
		return True 
	return ["vice.core.dataframe.tracers.__getitem__.row", test] 

