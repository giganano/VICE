""" 
Test the VICE dataframe base class 
""" 

from __future__ import absolute_import 
__all__ = ["test"] 
from ...core.dataframe import base 
from .._test_utils import moduletest 
from .._test_utils import unittest 


def test(run = True): 
	""" 
	Run all tests of the VICE dataframe base class 
	""" 
	# reset_test_frame() 
	test = moduletest("Base class") 
	test.new(unittest("Initialization", test_initialization)) 
	test.new(unittest("Keys", test_keys)) 
	test.new(unittest("Todict", test_todict)) 
	test.new(unittest("Getitem", test_getitem)) 
	test.new(unittest("Setitem", test_setitem)) 
	test.new(unittest("Remove", test_remove)) 
	test.new(unittest("Call", test_call)) 
	if run: 
		test.run() 
	else: 
		return test 


def test_initialization(): 
	""" 
	Test the initialization of the VICE dataframe base class 
	""" 
	global _TEST_FRAME_ 
	_TEST_FRAME_ = dict(zip(
		[str(i) for i in range(10)], 
		10 * [list(range(10))] 
	)) 
	try: 
		_TEST_FRAME_ = base(_TEST_FRAME_) 
	except: 
		return False 
	return isinstance(_TEST_FRAME_, base) 


def test_keys(): 
	""" 
	Tests the keys function of the VICE dataframe base class 
	""" 
	try: 
		return _TEST_FRAME_.keys() == [str(i) for i in range(10)] 
	except: 
		return False 


def test_todict(): 
	""" 
	Tests the todict function of the VICE dataframe base class 
	""" 
	try: 
		return _TEST_FRAME_.todict() == dict(zip(
			[str(i) for i in range(10)], 
			10 * [list(range(10))] 
		)) 
	except: 
		return False 


def test_getitem(): 
	""" 
	Tests the getitem function of the VICE dataframe base class 
	""" 
	try: 
		for i in range(10): 
			assert _TEST_FRAME_[str(i)] == list(range(10)) 
		for i in range(10): 
			assert _TEST_FRAME_[i] == base(dict(zip( 
				[str(i) for i in range(10)], 
				10 * [i] 
			))) 
	except: 
		return False 
	return True 


def test_call(): 
	""" 
	Tests the call function of the VICE dataframe base class 
	""" 
	try: 
		for i in _TEST_FRAME_.keys(): 
			assert _TEST_FRAME_(int(i)) == _TEST_FRAME_[int(i)] 
			assert _TEST_FRAME_(i) == _TEST_FRAME_[i] 
	except: 
		return False 
	return True 


def test_setitem(): 
	""" 
	Test the setitem function 
	""" 
	try: 
		_TEST_FRAME_["foo"] = "bar" 
		assert _TEST_FRAME_["foo"] == "bar" 
		assert "foo" in _TEST_FRAME_.keys() 
	except: 
		return False 
	return True 


def test_remove(): 
	""" 
	Test the remove function 
	""" 
	try: 
		_TEST_FRAME_.remove("foo") 
	except: 
		return False 
	return "foo" not in _TEST_FRAME_.keys() 

