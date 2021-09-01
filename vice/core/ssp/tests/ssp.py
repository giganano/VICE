""" 
Test the single population enrichment function 

User access of this code is strongly discouraged 
""" 

from __future__ import absolute_import 
__all__ = [
	"test"  
] 
from ...._globals import _RECOGNIZED_ELEMENTS_ 
from ...._globals import _VERSION_ERROR_ 
from ...dataframe._builtin_dataframes import atomic_number 
from .._ssp import single_stellar_population 
from ....yields import agb 
from ....testing import moduletest 
from ....testing import unittest 
from ...mlr import mlr 
import math 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 


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

	def __init__(self, msg, **kwargs): 
		self.msg = msg 
		self._kwargs = kwargs 

	@unittest 
	def __call__(self): 
		def test(): 
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
		return [self.msg, test] 

	@property 
	def msg(self): 
		r""" 
		Type : str 

		The message to print with the unit test. 
		""" 
		return self._msg 

	@msg.setter 
	def msg(self, value): 
		if isinstance(value, strcomp): 
			self._msg = value 
		else: 
			raise TypeError("Attribute 'msg' must be of type str. Got: %s" % (
				type(value))) 


class mlr_generator: 

	""" 
	A callable object designed to run trial SSP calculations under different 
	assumptions about the mass-lifetime relations. A timestep size of 1.e-4 is 
	used to ensure that the assumed MLR responds properly to stellar 
	populations young enough that no stars have died yet. 
	""" 

	def __init__(self, mlr = "larson1974"): 
		self.mlr = mlr 

	@unittest 
	def __call__(self): 
		def test(): 
			success = True 
			try: 
				current = mlr.setting 
				mlr.setting = self.mlr 
				for elem in _RECOGNIZED_ELEMENTS_: 
					mass, times = single_stellar_population(elem, time = 1, 
						dt = 1.e-4) 
					success &= all([not math.isnan(_) for _ in mass]) 
					if not success: break 
				mlr.setting = current 
			except: 
				return False 
			return success 
		return ["vice.core.single_stellar_population [MLR :: %s]" % (self.mlr), 
			test] 

	@property 
	def mlr(self): 
		r""" 
		Type : str 

		Default : "larson1974" 

		The MLR setting to test the SSP calculations with. 
		""" 
		return self._mlr 

	@mlr.setter 
	def mlr(self, value): 
		if isinstance(value, strcomp): 
			if value.lower() in mlr.recognized: 
				self._mlr = value.lower() 
			else: 
				raise ValueError("Unrecognized MLR: %s" % (value)) 
		else: 
			raise TypeError("MLR must be of type str. Got: %s" % (type(value))) 


@moduletest 
def test(): 
	""" 
	Run the trial tests of the single_stellar_population function 
	""" 
	trials = [] 
	for i in _IMF_: 
		trials.append(generator(
			"vice.core.single_stellar_population [IMF :: %s]" % (str(i)), 
			IMF = i)()) 
	for i in _RIA_: 
		trials.append(generator(
			"vice.core.single_stellar_population [RIa :: %s]" % (str(i)), 
			RIa = i)()) 
	for i in mlr.recognized: trials.append(mlr_generator(mlr = i)()) 
	return ["vice.core.single_stellar_population trial tests", trials] 

