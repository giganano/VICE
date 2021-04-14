""" 
Tests the AGB yield grid reader functions at vice/yields/agb/_grid_reader.pyx 
""" 

from __future__ import print_function 
__all__ = [
	"test" 
] 
from ....core.dataframe._builtin_dataframes import atomic_number 
from ...._globals import _RECOGNIZED_ELEMENTS_ 
from ....testing import moduletest 
from ....testing import unittest 
from .._grid_reader import yield_grid as grid 
from .._grid_reader import _VENTURA13_ELEMENTS_ 
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
			if self._study == "karakas10" and atomic_number[i] > 28: continue 
			if (self._study == "ventura13" and 
				i not in _VENTURA13_ELEMENTS_): continue 
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
		return success 


@moduletest 
def test(): 
	""" 
	Run the tests on the AGB yield grid functions 
	""" 
	return ["vice.yields.agb.grid", 
		[ 
			trial("Cristallo et al. (2011)", generator(study = "cristallo11")), 
			trial("Karakas (2010)", generator(study = "karakas10")), 
			trial("Ventura et al. (2013)", generator(study = "ventura13")) 
		] 
	] 


@unittest 
def trial(label, generator_): 
	""" 
	Obtain a unittest object for a singlezone trial test 
	""" 
	def test_(): 
		return generator_() 
	return [label, test_] 

