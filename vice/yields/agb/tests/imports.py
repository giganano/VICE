""" 
Tests yield imports for AGB star yields 
""" 

from __future__ import absolute_import 
__all__ = ["test"] 
from ...._globals import _RECOGNIZED_ELEMENTS_ 
from ....core.dataframe._builtin_dataframes import atomic_number 
from ....testing import moduletest 
from ....testing import unittest 


@moduletest 
def test(): 
	r""" 
	Test the yield import functions 
	""" 
	return ["vice.yields.agb.import", 
		[ 
			test_cristallo11_import(), 
			test_karakas10_import() 
		] 
	] 


@unittest 
def test_cristallo11_import(): 
	r""" 
	from vice.yields.agb import cristallo11 unittest 
	""" 
	def test(): 
		try: 
			from .. import cristallo11 
		except: 
			return False 
		from .. import settings 
		return all([settings[i] == "cristallo11" for i in _RECOGNIZED_ELEMENTS_]) 
	return ["vice.yields.agb.cristallo11", test] 


@unittest 
def test_karakas10_import(): 
	r""" 
	from vice.yields.agb import karakas10 unittest 
	""" 
	def test(): 
		try: 
			from .. import karakas10 
		except: 
			return False 
		from .. import settings 
		status = True 
		for i in _RECOGNIZED_ELEMENTS_: 
			if atomic_number[i] <= 28 and settings[i] != "karakas10": 
				status = False 
				break 
		return status 
	return ["vice.yields.agb.karakas10", test] 

