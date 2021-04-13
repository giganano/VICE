""" 
Test the CCSNe yield integrator at vice/yields/ccnse/_yield_integrator.pyx 
""" 

from __future__ import absolute_import 
__all__ = ["test" ]
from ...._globals import _RECOGNIZED_ELEMENTS_ 
from .._yield_integrator import integrate as fractional 
from .._errors import _RECOGNIZED_STUDIES_ as _STUDY_ 
from .._errors import _NAMES_ 
from .._errors import _MOVERH_ 
from .._errors import _ROTATION_ 
from ....testing import moduletest 
from ....testing import unittest 
import warnings 
import random 
random.seed() 
import math 

# upper mass cutoff of each study 
_UPPER_ = {
	"LC18":			120, 
	"CL13": 		120, 
	"NKT13": 		40, 
	"CL04": 		35, 
	"WW95": 		40, 
	"S16/W18": 		120, 
	"S16/W18F": 	120, 
	"S16/N20": 		120 
}

# IMFs to test the integrations on 
_IMF_ = ["kroupa", "salpeter", lambda m: m**-2] 


class generator: 

	def __init__(self, **kwargs): 
		self._kwargs = kwargs 

	def __call__(self): 
		success = True 
		# Conduct the assertions for 10 randomly drawn elements 
		for i in range(10): 
			idx = int(random.random() * len(_RECOGNIZED_ELEMENTS_)) 
			elem = _RECOGNIZED_ELEMENTS_[idx] 
			try: 
				net_with_wind, err_net_with_wind = fractional(elem, 
					wind = True, net = True, **self._kwargs) 
				gross_with_wind, err_gross_with_wind = fractional(elem, 
					wind = True, net = False, **self._kwargs) 
				net_no_wind, err_net_no_wind = fractional(elem, 
					wind = False, net = True, **self._kwargs) 
				gross_no_wind, err_gross_no_wind = fractional(elem, 
					wind = False, net = False, **self._kwargs) 
			except: 
				return False 
			if net_with_wind == 0: success &= math.isnan(err_net_with_wind) 
			if gross_with_wind == 0: success &= math.isnan(err_gross_with_wind) 
			if net_no_wind == 0: success &= math.isnan(err_net_no_wind) 
			if gross_no_wind == 0: success &= math.isnan(err_gross_no_wind) 
			success &= 0 <= gross_no_wind <= gross_with_wind <= 1 
			success &= net_no_wind <= net_with_wind <= 1 
			success &= net_no_wind <= gross_no_wind 
			success &= net_with_wind <= gross_with_wind 
			if not success: break 
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

