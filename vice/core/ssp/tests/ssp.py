""" 
Test the single population enrichment function 

User access of this code is strongly discouraged 
""" 

from __future__ import absolute_import 
__all__ = [
	"test"  
] 
from ...._globals import _RECOGNIZED_ELEMENTS_ 
from ...dataframe._builtin_dataframes import atomic_number 
from .._ssp import single_stellar_population 
from ....testing import moduletest 
from ....testing import unittest 


""" 
The IMF and RIa are the only parameters to the single_stellar_population 
function which have a limited range of values or may vary by type. The 
function is tested by ensuring that it runs under all possible combinations 
""" 
_MSTAR_ = 1.e6 
_IMF_ = ["kroupa", "salpeter", lambda m: m**-2] 
_RIA_ = ["plaw", "exp", lambda t: t**-1.5] 


class generator: 

	""" 
	A callable object which can be cast as a unittest for the 
	single_stellar_population function 
	""" 

	def __init__(self, **kwargs): 
		self._kwargs = kwargs 

	def __call__(self): 
		success = True 
		for elem in _RECOGNIZED_ELEMENTS_: 
			try: 
				mass, times = single_stellar_population(elem, 
					agb_model = "cristallo11", **self._kwargs)  
				if mass[-1] > _MSTAR_: success = False 
			except: 
				success = False 
			if atomic_number[elem] <= 28: 
				try: 
					mass, times = single_stellar_population(elem, 
						agb_model = "karakas10", **self._kwargs) 
					if mass[-1] > _MSTAR_: success = False 
				except: 
					success = False 
			else: 
				continue 
		return success 


@moduletest 
def test(): 
	""" 
	Run the trial tests of the single_stellar_population function 
	""" 
	trials = [] 
	for i in _IMF_: 
		trials.append(trial(
			"vice.core.single_stellar_population [IMF :: %s]" % (str(i)), 
			generator(IMF = i))) 
	for i in _RIA_: 
		trials.append(trial(
			"vice.core.single_stellar_population [RIa :: %s]" % (str(i)), 
			generator(RIa = i))) 
	return ["vice.core.single_stellar_population trial tests", trials] 


@unittest 
def trial(label, generator_): 
	""" 
	Obtain a unittest object for a single_stellar_population trial test 
	""" 
	def test_(): 
		return generator_() 
	return [label, test_] 

