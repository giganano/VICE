""" 
Tests the yield imports for CCSN yields 
""" 

from __future__ import absolute_import 
__all__ = [
	"test" 
] 
from ..._test_utils import moduletest 
from ..._test_utils import unittest 
from ....yields import ccsne 


@moduletest 
def test(): 
	""" 
	Test the yield import functions 
	""" 
	return ["VICE CCSN yield import functions", 
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
			from ....yields.ccsne import LC18 
		except: 
			return False 
		return True 
	return ["Limongi & Chieffi (2018)", test] 


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
			from ....yields.ccsne import CL13 
		except: 
			return False 
		return True 
	return ["Chieffi & Limongi (2013)", test] 


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
			from ....yields.ccsne import CL04 
		except: 
			return False 
		return True 
	return ["Chieffi & Limongi (2004)", test] 


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
			from ....yields.ccsne import WW95 
		except: 
			return False 
		return True 
	return ["Woosley & Weaver (1995)", test] 


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
			from ....yields.ccsne import NKT13 
		except: 
			return False 
		return True 
	return ["Nomoto, Kobayashi & Tominaga (2013)", test] 

