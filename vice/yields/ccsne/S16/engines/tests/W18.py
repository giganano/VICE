r""" 
This file implements testing of the explodability engines in the parent 
directory. 
""" 

from __future__ import absolute_import 
from ......testing import unittest 
from ..W18 import W18 
import numbers 
import random 


@unittest 
def test_W18(): 
	r""" 
	vice.yields.ccsne.S16.engines.W18 unit test 
	""" 
	def test(): 
		try: 
			W18_ = W18() 
		except: 
			return None 
		try: 
			for i in range(1000): 
				mass = 120 * random.random() 
				assert 0 <= W18_(mass) <= 1 
				if mass < 8: assert W18_(mass) == 0 
			assert isinstance(W18_.masses, list) 
			assert all([isinstance(i, numbers.Number) for i in W18_.masses]) 
			assert isinstance(W18_.frequencies, list) 
			assert all([isinstance(i, numbers.Number) for i in W18_.frequencies]) 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.S16.engines.W18", test] 

