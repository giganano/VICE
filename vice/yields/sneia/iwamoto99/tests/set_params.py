
from __future__ import absolute_import 
from ....._globals import _RECOGNIZED_ELEMENTS_ 
from .....testing import unittest 
from ... import fractional 
from ... import settings 


@unittest 
def test(): 
	r""" 
	Run the unit test on the set_params function in this module 
	""" 
	def test_set_params(): 
		kwargs = {
			"model": "CDD1", 
			"n": 1.3e-03 
		} 
		try: 
			from .. import set_params 
			set_params(**kwargs) 
		except: 
			return False 
		status = True 
		for i in _RECOGNIZED_ELEMENTS_: 
			if settings[i] != fractional(i, study = "iwamoto99", **kwargs): 
				status = False 
				break 
		return status 
	return ["vice.yields.sneia.iwamoto99.set_params", test_set_params] 

