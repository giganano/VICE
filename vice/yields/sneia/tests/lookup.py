
from __future__ import absolute_import 
from ...._globals import _RECOGNIZED_ELEMENTS_ 
from ....testing import unittest 
from .._yield_lookup import integrated_yield as fractional 
from .._yield_lookup import single_detonation as single 
import numbers 


_STUDY_ = ["iwamoto99", "seitenzahl13"] 
_MODEL_ = {
	"seitenzahl13":	 		["N1", "N3", "N5", "N10", "N40", "N100H", 
							"N100", "N100L", "N150", "N200", "N300C", 
							"N1600", "N100_Z0.5", "N100_Z0.1", "N100_Z0.01"], 
	"iwamoto99": 			["W7", "W70", "WDD1", "WDD2", "WDD3", "CDD1", 
							"CDD2"] 
}


@unittest 
def test_single(): 
	""" 
	vice.yields.sneia.single unit test 
	""" 
	def test(): 
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
	return ["vice.yields.sneia.single", test] 


@unittest 
def test_fractional(): 
	""" 
	vice.yields.sneia.fractional unit test 
	""" 
	def test(): 
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
	return ["vice.yields.sneia.fractional", test] 

