
from __future__ import absolute_import 
__all__ = [ 
	"test", 
	"test_mirror", 
	"test_history", 
	"test_mdf", 
	"test_output" 
] 
from ....testing import moduletest 
from ....testing import unittest 
from ...singlezone import singlezone 
from ...dataframe import base as dataframe 
from ...outputs import output 
from ...mirror import mirror 
from .. import history 
from .. import mdf 
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
	Run the tests on this module 
	""" 
	singlezone.singlezone(name = _TEST_NAME_).run(_OUTTIMES_, overwrite = True) 
	return ["vice.core.outputs.tests", 
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
		try: 
			test_ = mirror(_TEST_NAME_) 
		except: 
			return False 
		return isinstance(test_, singlezone.singlezone) 
	return ["vice.core.mirror", test] 


@unittest 
def test_history(): 
	""" 
	History function unit test 
	""" 
	def test(): 
		""" 
		Tests the history function 
		""" 
		try: 
			test_ = history(_TEST_NAME_) 
		except: 
			return False 
		return isinstance(test_, dataframe) 
	return ["vice.core.outputs.history", test] 


@unittest 
def test_mdf(): 
	""" 
	MDF function unit test 
	""" 
	def test(): 
		""" 
		Tests the mdf function 
		""" 
		try: 
			test_ = mdf(_TEST_NAME_) 
		except: 
			return False 
		return isinstance(test_, dataframe) 
	return ["vice.core.outputs.mdf", test] 


@unittest 
def test_output(): 
	""" 
	output class unit test 
	""" 
	def test(): 
		""" 
		Tests the output class 
		""" 
		try: 
			test_ = output(_TEST_NAME_) 
		except: 
			return False 
		return (
			isinstance(test_, output) and 
			isinstance(test_.elements, tuple) and 
			isinstance(test_.agb_yields, dataframe) and 
			isinstance(test_.ccsne_yields, dataframe) and 
			isinstance(test_.sneia_yields, dataframe) and 
			isinstance(test_.mdf, dataframe) and 
			isinstance(test_.history, dataframe) 
		) 
	return ["vice.core.outputs.output", test] 

