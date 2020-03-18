""" 
This file runs trial tests of the singlezone object to ensure that each 
attribute which can vary by type does not produce an error at runtime. 
""" 

from __future__ import absolute_import 
__all__ = [
	"test" 
]
from ....tests._test_utils import moduletest 
from ....tests._test_utils import unittest 
from ..singlezone import singlezone 
import math 
try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 
try: 
	import numpy as np 
	_OUTTIMES_ = np.linspace(0, 1, 21) 
except (ModuleNotFoundError, ImportError): 
	_OUTTIMES_ = [0.05 * i for i in range(21)] 


""" 
Below are each of the parameters that either have a limited range of values 
or may vary by type. The singlezone object is tested by running one of each 
and ensuring that the simulation runs under each parameter. 
""" 
_MODES_ = ["ifr", "sfr", "gas"] 
_IMF_ = ["kroupa", "salpeter", lambda m: m**-2] 
_ETA_ = [2.5, lambda t: 2.5 * math.exp( -t / 4.0 )] 
_ZIN_ = [0, 1.0e-8, lambda t: 1.0e-8 * (t / 10.0), {
	"o":		lambda t: 0.0057 * (t / 10.0),  
	"fe": 		0.0013
}] 
_RECYCLING_ = ["continuous", 0.4] 
_RIA_ = ["plaw", "exp", lambda t: t**-1.5] 
_TAU_STAR_ = [2.0, lambda t: 2.0 + t / 10.0] 
_SCHMIDT_ = [False, True] 


class generator: 

	""" 
	A callable object which can be cast as a unittest object for the 
	singlezone object 
	""" 

	def __init__(self, **kwargs): 
		self._sz = singlezone(name = "test", dt = 0.05, **kwargs) 

	def __call__(self): 
		# try: 
		self._sz.run(_OUTTIMES_, overwrite = True) 
		# except: 
		# 	return False 
		return True 


@moduletest 
def test(): 
	""" 
	Run the trial tests of the singlezone object 
	""" 
	trials = [] 
	for i in _MODES_: 
		trials.append(trial("mode: %s" % (str(i)), generator(mode = i))) 
	for i in _IMF_: 
		trials.append(trial("IMF: %s" % (str(i)), generator(IMF = i))) 
	for i in _ETA_: 
		trials.append(trial("eta: %s" % (str(i)), generator(eta = i))) 
	for i in _ZIN_: 
		trials.append(trial("Zin: %s" % (str(i)), generator(Zin = i))) 
	for i in _RECYCLING_: 
		trials.append(trial("recycling: %s" % (str(i)), 
			generator(recycling = i))) 
	for i in _RIA_: 
		trials.append(trial("RIa: %s" % (str(i)), generator(RIa = i))) 
	for i in _TAU_STAR_: 
		trials.append(trial("SFE timescale: %s" % (str(i)), 
			generator(tau_star = i))) 
	for i in _SCHMIDT_: 
		trials.append(trial("Schmidt: %s" % (str(i)), generator(schmidt = i))) 
	return ["VICE singlezone trial tests", trials] 


@unittest 
def trial(label, generator_): 
	""" 
	Obtain a unittest object for a singlezone trial test 
	""" 
	def test_(): 
		return generator_() 
	return [label, test_] 

