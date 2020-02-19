
from __future__ import absolute_import 
__all__ = [
	"test", 
	"test_mirror", 
	"test_history", 
	"test_mdf", 
	"test_output" 
] 
from ..core.singlezone.singlezone import singlezone 
from ..core.dataframe import base as dataframe 
from ..core.outputs import output 
from ..core.outputs import history 
from ..core.outputs import mdf 
from ..core.mirror import mirror 
from ._test_utils import moduletest 
from ._test_utils import unittest 
try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 
try: 
	import numpy as np 
	_OUTTIMES_ = np.linspace(0, 1, 21) 
except (ModuleNotFoundError, ImportError): 
	_OUTTIMES_ = [0.05 * i for i in range(21)] 
_TEST_NAME_ = "test"

def test(run = True): 
	""" 
	Tests all functions in this module 
	""" 
	test = moduletest("VICE output utilities") 
	singlezone(name = _TEST_NAME_).run(_OUTTIMES_, overwrite = True) 
	test.new(unittest("Mirror", test_mirror)) 
	test.new(unittest("History", test_history)) 
	test.new(unittest("MDF", test_mdf)) 
	test.new(unittest("Output object", test_output)) 
	if run: 
		test.run() 
	else: 
		return test 


def test_mirror(): 
	""" 
	Tests the mirror function 
	""" 
	try: 
		test = mirror(_TEST_NAME_) 
		return isinstance(test, singlezone) 
	except: 
		return False 


def test_history(): 
	""" 
	Tests the history function 
	""" 
	try: 
		test = history(_TEST_NAME_) 
		return isinstance(test, dataframe) 
	except: 
		return False 


def test_mdf(): 
	""" 
	Tests the mdf function 
	""" 
	try: 
		test = mdf(_TEST_NAME_) 
		return isinstance(test, dataframe) 
	except: 
		return False 


def test_output(): 
	""" 
	Tests the output class 
	""" 
	try: 
		test = output(_TEST_NAME_) 
		return (
			isinstance(test, output) and 
			isinstance(test.elements, tuple) and 
			isinstance(test.agb_yields, dataframe) and 
			isinstance(test.ccsne_yields, dataframe) and 
			isinstance(test.sneia_yields, dataframe) and 
			isinstance(test.mdf, dataframe) and 
			isinstance(test.history, dataframe) 
		) 
	except: 
		return False 

