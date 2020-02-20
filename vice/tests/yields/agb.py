""" 
Tests the AGB yield grid reader functions at vice/yields/agb/_grid_reader.pyx 
""" 

from __future__ import print_function 
__all__ = [
	"test" 
] 
from ...core.dataframe._builtin_dataframes import atomic_number 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ...yields.agb import grid 
from .._test_utils import moduletest 
from .._test_utils import unittest 
import numbers 


class generator: 

	""" 
	A class which can be cast as a unittest for the AGB yield grid functions. 
	""" 

	def __init__(self, study = "cristallo11"): 
		self._study = study 


	def __call__(self): 
		success = True 
		for i in _RECOGNIZED_ELEMENTS_: 
			if not (self._study == "karakas10" and atomic_number[i] > 28): 
				try: 
					yields, mass, z = grid(i, study = self._study) 
					assert isinstance(mass, tuple) 
					assert isinstance(z, tuple) 
					assert isinstance(yields, tuple) 
					assert all(map(lambda x: isinstance(x, tuple), yields)) 
					assert all(map(lambda x: isinstance(x, numbers.Number), 
						mass)) 
					assert all(map(lambda x: isinstance(x, numbers.Number), z)) 
					for j in range(len(yields)): 
						assert all(map(lambda x: isinstance(x, numbers.Number), 
							yields[j])) 
				except: 
					success = False 
			else: 
				pass 
		return success 


def test(run = True): 
	""" 
	Run the tests on the AGB yield grid functions 
	""" 
	test = moduletest("VICE AGB star yield grid lookup") 
	test.new(unittest("Cristallo et al. (2011)", 
		generator(study = "cristallo11"))) 
	test.new(unittest("Karakas (2010)", generator(study = "karakas10"))) 
	if run: 
		test.run() 
	else: 
		return test 

