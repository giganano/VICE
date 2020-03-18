""" 
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
	""" 
	Test the yield import functions 
	""" 
	return ["vice.yields.ccsne.import", 
		[ 
			test_LC18_import(), 
			test_CL13_import(), 
			test_CL04_import(), 
			test_WW95_import(), 
			test_NKT13_import() 
		] 
	] 


@unittest 
def test_LC18_import(): 
	""" 
	from vice.yields.ccsne import LC18 unit test 
	""" 
	def test(): 
		""" 
		Test the Limongi & Chieffi (2018) import 
		""" 
		try: 
			from .. import LC18 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.LC18", test] 


@unittest 
def test_CL13_import(): 
	""" 
	from vice.yields.ccsne import CL13 unit test 
	""" 
	def test(): 
		""" 
		Test the Chieffi & Limongi (2013) import 
		""" 
		try: 
			from .. import CL13 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.CL13", test] 


@unittest 
def test_CL04_import(): 
	""" 
	from vice.yields.ccsne import CL04 unit test 
	""" 
	def test(): 
		""" 
		Test the Chieffi & Limongi (2004) import 
		""" 
		try: 
			from .. import CL04 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.CL04", test] 


@unittest 
def test_WW95_import(): 
	""" 
	from vice.yields.ccsne import WW95 unit test 
	""" 
	def test(): 
		""" 
		Test the Woosley & Weaver (1995) import 
		""" 
		try: 
			from .. import WW95 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.WW95", test] 


@unittest 
def test_NKT13_import(): 
	""" 
	from vice.yields.ccsne import NKT13 unit test 
	""" 
	def test(): 
		""" 
		Test the Nomoto, Kobayashi & Tominaga (2013) import 
		""" 
		try: 
			from .. import NKT13 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.NKT13", test] 

