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


def test(run = True): 
	""" 
	Test the yield import functions 
	""" 
	test = moduletest("VICE CCSN yield import functions") 
	test.new(unittest("Limongi & Chieffi (2018)", test_LC18_import)) 
	test.new(unittest("Chieffi & Limongi (2013)", test_CL13_import)) 
	test.new(unittest("Chieffi & Limongi (2004)", test_CL04_import)) 
	test.new(unittest("Woosley & Weaver (1995)", test_WW95_import)) 
	test.new(unittest("Nomoto, Kobayashi & Tominaga (2013)", 
		test_NKT13_import)) 
	if run: 
		test.run() 
	else: 
		return test 


def test_LC18_import(): 
	""" 
	Test the Limongi & Chieffi (2018) import 
	""" 
	try: 
		from ....yields.ccsne import LC18 
	except: 
		return False 
	return True 


def test_CL13_import(): 
	""" 
	Test the Chieffi & Limongi (2013) import 
	""" 
	try: 
		from ....yields.ccsne import CL13 
	except: 
		return False 
	return True 


def test_CL04_import(): 
	""" 
	Test the Chieffi & Limongi (2004) import 
	""" 
	try: 
		from ....yields.ccsne import CL04 
	except: 
		return False 
	return True 


def test_WW95_import(): 
	""" 
	Test the Woosley & Weaver (1995) import 
	""" 
	try: 
		from ....yields.ccsne import WW95 
	except: 
		return False 
	return True 


def test_NKT13_import(): 
	""" 
	Test the Nomoto, Kobayashi & Tominaga (2013) import 
	""" 
	try: 
		from ....yields.ccsne import NKT13 
	except: 
		return False 
	return True 

