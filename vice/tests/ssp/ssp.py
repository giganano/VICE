""" 
Test the single population enrichment function 

User access of this code is strongly discouraged 
""" 

from __future__ import absolute_import 
__all__ = [
	"test"  
] 
from ...core.dataframe._builtin_dataframes import atomic_number 
from ...core.ssp._ssp import single_stellar_population 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ...yields import agb 
from .._test_utils import moduletest 
from .._test_utils import unittest 


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
			current_agb_setting = agb.settings[elem] 
			agb.settings[elem] = "cristallo11" 
			try: 
				mass, times = single_stellar_population(elem, **self._kwargs) 
				if mass[-1] > _MSTAR_: success = False 
			except: 
				success = False 
			if atomic_number[elem] <= 28: 
				agb.settings[elem] = "karakas10" 
				try: 
					mass, times = single_stellar_population(elem, 
						**self._kwargs) 
					if mass[-1] > _MSTAR_: success = False 
				except: 
					success = False 
			else: 
				continue 
			agb.settings[elem] = current_agb_setting 
		return success 


def test(run = True): 
	""" 
	Run the trial tests of the single_stellar_population function 
	""" 
	test = moduletest("VICE single stellar population enrichment trial tests") 
	for i in _IMF_: 
		test.new(unittest("IMF = %s" % (str(i)), generator(IMF = i))) 
	for i in _RIA_: 
		test.new(unittest("RIa = %s" % (str(i)), generator(RIa = i))) 
	if run: 
		test.run() 
	else: 
		return test 

