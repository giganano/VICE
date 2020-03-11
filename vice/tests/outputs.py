
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


@moduletest 
def test(): 
	""" 
	Tests all functions in this module 
	""" 
	singlezone(name = _TEST_NAME_).run(_OUTTIMES_, overwrite = True) 
	return ["VICE output utilities", 
		[ 
			test_mirror(), 
			test_history(), 
			test_mdf(), 
			test_output() 
		] 
	] 


@unittest 
def test_mirror(): 
	""" 
	Mirror function unit test 
	""" 
	def test(): 
		""" 
		Tests the mirror function 
		""" 
		# try: 
		test_ = mirror(_TEST_NAME_) 
		# except: 
		# 	return False 
		return isinstance(test_, singlezone) 
	return ["Mirror", test] 


@unittest 
def test_history(): 
	""" 
	History function unit test 
	""" 
	def test(): 
		""" 
		Tests the history function 
		""" 
		# try: 
		test_ = history(_TEST_NAME_) 
		# except: 
		# 	return False 
		return isinstance(test_, dataframe) 
	return ["History", test] 


@unittest 
def test_mdf(): 
	""" 
	MDF function unit test 
	""" 
	def test(): 
		""" 
		Tests the mdf function 
		""" 
		# try: 
		test_ = mdf(_TEST_NAME_) 
		# except: 
		# 	return False 
		return isinstance(test_, dataframe) 
	return ["MDF", test] 


@unittest 
def test_output(): 
	""" 
	output class unit test 
	""" 
	def test(): 
		""" 
		Tests the output class 
		""" 
		# try: 
		test_ = output(_TEST_NAME_) 
		# except: 
		# 	return False 
		return (
			isinstance(test_, output) and 
			isinstance(test_.elements, tuple) and 
			isinstance(test_.agb_yields, dataframe) and 
			isinstance(test_.ccsne_yields, dataframe) and 
			isinstance(test_.sneia_yields, dataframe) and 
			isinstance(test_.mdf, dataframe) and 
			isinstance(test_.history, dataframe) 
		) 
	return ["Output", test] 

