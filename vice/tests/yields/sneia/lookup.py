
from __future__ import absolute_import 
from ...._globals import _RECOGNIZED_ELEMENTS_ 
from ....yields.sneia import fractional 
from ....yields.sneia import single 
from ..._test_utils import moduletest 
from ..._test_utils import unittest 
import numbers 


_STUDY_ = ["iwamoto99", "seitenzahl13"] 
_MODEL_ = {
	"seitenzahl13":	 		["N1", "N3", "N5", "N10", "N40", "N100H", 
							"N100", "N100L", "N150", "N200", "N300C", 
							"N1600", "N100_Z0.5", "N100_Z0.1", "N100_Z0.01"], 
	"iwamoto99": 			["W7", "W70", "WDD1", "WDD2", "WDD3", "CDD1", 
							"CDD2"] 
}


def test(run = True): 
	""" 
	Run all tests in this module 
	""" 
	test = moduletest("SN Ia yield lookup functions") 
	test.new(unittest("Single Ia mass yield", test_single)) 
	test.new(unittest("IMF-averaged calculator", test_fractional)) 
	if run: 
		test.run() 
	else: 
		return test 


def test_single(): 
	""" 
	Test the single SN Ia mass yield lookup function 
	""" 
	success = True 
	try: 
		for i in _RECOGNIZED_ELEMENTS_: 
			for j in _STUDY_: 
				for k in _MODEL_[j]: 
					x = single(i, study = j, model = k) 
					assert isinstance(x, numbers.Number) 
					assert x >= 0 
	except: 
		success = False 
	return success 


def test_fractional(): 
	""" 
	Test the fractional SN Ia mass yield function 
	""" 
	success = True 
	try: 
		for i in _RECOGNIZED_ELEMENTS_: 
			for j in _STUDY_: 
				for k in _MODEL_[j]: 
					x = fractional(i, study = j, model = k) 
					assert isinstance(x, numbers.Number) 
					assert 0 <= x < 1 
	except: 
		success = False 
	return success 

