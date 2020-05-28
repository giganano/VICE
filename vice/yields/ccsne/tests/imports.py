r""" 
Tests the yield imports for CCSN yields 
""" 

from __future__ import absolute_import 
__all__ = [
	"test" 
] 
from ....testing import moduletest 
from ....testing import unittest 


@moduletest 
def test(): 
	r""" 
	Test the yield import functions 
	""" 
	return ["vice.yields.ccsne.import", 
		[ 
			test_LC18_import(), 
			test_CL13_import(), 
			test_CL04_import(), 
			test_WW95_import(), 
			test_NKT13_import(), 
			test_S16_import() 
		] 
	] 


@unittest 
def test_LC18_import(): 
	r""" 
	from vice.yields.ccsne import LC18 unit test 
	""" 
	def test(): 
		try: 
			from .. import LC18 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.LC18", test] 


@unittest 
def test_CL13_import(): 
	r""" 
	from vice.yields.ccsne import CL13 unit test 
	""" 
	def test(): 
		try: 
			from .. import CL13 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.CL13", test] 


@unittest 
def test_CL04_import(): 
	r""" 
	from vice.yields.ccsne import CL04 unit test 
	""" 
	def test(): 
		try: 
			from .. import CL04 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.CL04", test] 


@unittest 
def test_WW95_import(): 
	r""" 
	from vice.yields.ccsne import WW95 unit test 
	""" 
	def test(): 
		try: 
			from .. import WW95 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.WW95", test] 


@unittest 
def test_NKT13_import(): 
	r""" 
	from vice.yields.ccsne import NKT13 unit test 
	""" 
	def test(): 
		try: 
			from .. import NKT13 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.NKT13", test] 


@unittest 
def test_S16_import(): 
	r""" 
	from vice.yields.ccsne import S16 unit test 
	""" 
	def test(): 
		try: 
			from .. import S16 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.S16", test] 

