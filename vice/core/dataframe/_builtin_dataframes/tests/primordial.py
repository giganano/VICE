
from __future__ import absolute_import 
__all__ = ["test_primordial"] 
from ....._globals import _RECOGNIZED_ELEMENTS_ 
from .....tests._test_utils import unittest 
from ..primordial import primordial 
import numbers 


@unittest 
def test_primordial(): 
	""" 
	Primordial_z built-in dataframe unit test 
	""" 
	def test(): 
		""" 
		Test the primordial abundances dataframe 
		""" 
		try: 
			for i in _RECOGNIZED_ELEMENTS_: 
				assert isinstance(primordial[i], numbers.Number) 
				if i == "he": 
					assert primordial[i] > 0 
				else: 
					assert primordial[i] == 0 
		except: 
			return False 
		return True 
	return ["Primordial Z", test] 

