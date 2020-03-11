""" 
Test the VICE dataframe base class 
""" 

from __future__ import absolute_import 
__all__ = ["test"] 
from ...core.dataframe import base 
from .._test_utils import moduletest 
from .._test_utils import unittest 


@moduletest 
def test(): 
	""" 
	Run all tests of the VICE dataframe base class 
	""" 
	return ["Base class", 
		[
			test_initialization(), 
			test_keys(), 
			test_todict(), 
			test_getitem(), 
			test_setitem(), 
			test_remove(), 
			test_call(), 
			test_filter() 
		] 
	] 


@unittest 
def test_initialization(): 
	""" 
	Dataframe base class initialization unit test 
	""" 
	def test(): 
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
	return ["Initialization", test] 
	

@unittest 
def test_keys(): 
	""" 
	Base class keys function unit test 
	""" 
	def test(): 
		""" 
		Tests the keys function of the VICE dataframe base class 
		""" 
		try: 
			return _TEST_FRAME_.keys() == [str(i) for i in range(10)] 
		except: 
			return False 
	return ["Keys", test] 


@unittest 
def test_todict(): 
	""" 
	Base class todict unit test 
	""" 
	def test(): 
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
	return ["Todict", test] 


@unittest 
def test_getitem(): 
	""" 
	Base class __getitem__ unit test 
	""" 
	def test(): 
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
	return ["Getitem", test] 


@unittest 
def test_call(): 
	""" 
	Base class __call__ unit test 
	""" 
	def test(): 
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
	return ["Call", test] 


@unittest 
def test_setitem(): 
	""" 
	Base class __setitem__ unit test 
	""" 
	def test(): 
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
	return ["Setitem", test] 


@unittest 
def test_remove(): 
	""" 
	Base class remove function 
	""" 
	def test(): 
		""" 
		Test the remove function 
		""" 
		try: 
			_TEST_FRAME_.remove("foo") 
		except: 
			return False 
		return "foo" not in _TEST_FRAME_.keys() 
	return ["Remove", test] 


@unittest 
def test_filter(): 
	""" 
	Base class filter function 
	""" 
	def test(): 
		""" 
		Test the filter function 
		""" 
		try: 
			for i in _TEST_FRAME_.keys(): 
				for j in range(10): 
					test = _TEST_FRAME_.filter(i, "<", j) 
					assert all(map(lambda x: x < j, test[i])) 
					test = _TEST_FRAME_.filter(i, "<=", j) 
					assert all(map(lambda x: x <= j, test[i])) 
					test = _TEST_FRAME_.filter(i, "=", j) 
					assert all(map(lambda x: x == j, test[i])) 
					test = _TEST_FRAME_.filter(i, "==", j) 
					assert all(map(lambda x: x == j, test[i])) 
					test = _TEST_FRAME_.filter(i, ">=", j) 
					assert all(map(lambda x: x >= j, test[i])) 
					test = _TEST_FRAME_.filter(i, ">", j) 
					assert all(map(lambda x: x > j, test[i])) 
		except: 
			return False 
		return True 
	return ["Filter", test] 

