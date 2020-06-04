""" 
Test the CCSNe yield integrator at vice/yields/ccnse/_yield_integrator.pyx 
""" 

from __future__ import absolute_import 
__all__ = [
	"test" 
]
from ...._globals import _RECOGNIZED_ELEMENTS_ 
from .._yield_integrator import integrate as fractional 
from ....testing import moduletest 
from ....testing import unittest 
import warnings 
import math 


_STUDY_ = ["LC18", "CL13", "CL04", "WW95"]  
_NAMES_ = {
	"LC18": 		"Limongi & Chieffi (2018)", 
	"CL13": 		"Chieffi & Limongi (2013)", 
	"CL04": 		"Chieffi & Limongi (2004)", 
	"WW95": 		"Woosley & Weaver (1995)", 
}
_MOVERH_ = {
	"LC18":			[-3, -2, -1, 0], 
	"CL13": 		[0], 
	"CL04":			[-float("inf"), -4, -2, -1, -0.37, 0.15], 
	"WW95":			[-float("inf"), -4, -2, -1, 0] 
}
_ROTATION_ = {
	"LC18":			[0, 150, 300], 
	"CL13":			[0, 300], 
	"CL04":			[0], 
	"WW95":			[0] 
}
_UPPER_ = {
	"LC18":			120, 
	"CL13": 		120, 
	"CL04": 		35, 
	"WW95": 		40 
}
_IMF_ = ["kroupa", "salpeter", lambda m: m**-2] 


class generator: 

	def __init__(self, **kwargs): 
		self._kwargs = kwargs 


	def __call__(self): 
		success = True 
		for elem in _RECOGNIZED_ELEMENTS_: 
			try: 
				yield_, err = fractional(elem, **self._kwargs) 
				assert 0 <= yield_ < 1 
				if yield_ == 0: assert math.isnan(err) 
			except: 
				success = False 
		return success 


@moduletest 
def test(): 
	""" 
	Test the yield integration functions 
	""" 
	trials = [] 
	for i in _STUDY_: 
		for j in _MOVERH_[i]: 
			for k in _ROTATION_[i]: 
				for l in _IMF_: 
					params = dict(
						study = i, 
						MoverH = j, 
						rotation = k, 
						IMF = l, 
						m_upper = _UPPER_[i] 
					) 
					trials.append(trial(
						"%s :: [M/H] = %g :: vrot = %g km/s :: IMF = %s" % (
							_NAMES_[i], j, k, l), 
						generator(**params)
					)) 
	return ["vice.yields.ccsne.fractional", trials] 


@unittest 
def trial(label, generator_): 
	""" 
	Obtain a unittest object for a singlezone trial test 
	""" 
	def test_(): 
		return generator_() 
	return [label, test_] 

