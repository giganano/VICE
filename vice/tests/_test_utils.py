""" 
This file implements utility functions for VICE's tests. 
""" 

from __future__ import absolute_import 
__all__ = [
	"moduletest", 
	"unittest" 
] 
from .._globals import _VERSION_ERROR_ 
import functools 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 


# "Passed" and "Failed" as green and red strings, respectively 
_PASSED_MESSAGE_ = "\033[92mPassed\033[00m" 
_FAILED_MESSAGE_ = "\033[91mFailed\033[00m" 


def moduletest(function): 
	""" 
	A decorator which will construct a moduletest automatically from a 
	description and a list of unittest objects 
	""" 
	@functools.wraps(function) 
	def wrapper(run = True): 
		description, unittests = function() 
		test = _moduletest(description) 
		for i in unittests: 
			test.new(i) 
		if run: 
			test.run(print_results = True)  
		else: 
			return test 
	return wrapper 


def unittest(function): 
	""" 
	A decorator which will construct a unittest automatically from a 
	description and a function which runs the test 
	""" 
	@functools.wraps(function) 
	def wrapper(*args): 
		""" 
		Some unittests are for objects, and will require a call to self as the 
		first argument 
		""" 
		description, testfunc = function(*args) 
		return _unittest(description, testfunc) 
	return wrapper 


class _moduletest(object): 

	""" 
	A class designed to hold the information associated with a module test 
	(i.e. a set of unit tests) and subsequently run it. 

	User access of this class is strongly discouraged. 
	""" 

	def __init__(self, name): 
		self.name = name 
		self._unittests = [] 

	@property 
	def name(self): 
		""" 
		Type :: str 

		The name of the module being tested 
		""" 
		return self._name 

	@name.setter 
	def name(self, value): 
		if isinstance(value, str): 
			self._name = value 
		elif value is None: 
			self._name = None 
		else: 
			raise TypeError("Attribute 'name' must be of type str. Got: %s" % (
				type(value))) 

	@property 
	def unittests(self): 
		""" 
		Type :: list 

		The unit tests in the module 
		""" 
		return self._unittests 

	def new(self, obj): 
		""" 
		Add a unit test to the module test. 
		""" 
		if isinstance(obj, _unittest) or isinstance(obj, _moduletest): 
			self._unittests.append(obj) 
		else: 
			print(obj) 
			raise TypeError("Object must be of type unittest. Got: %s" % (
				type(obj))) 

	def run(self, print_results = False): 
		""" 
		Run the module tests 
		""" 
		passed = 0 
		failed = 0 
		if self.name is not None: 
			header = "Module Test: %s\n" % (self.name) 
			for i in range(len(header) - 1): 
				header += "=" 
			print("\n\033[96m%s\033[00m" % (header)) 
		else: 
			pass 
		for i in self._unittests: 
			if isinstance(i, _unittest): 
				if i.run(): 
					print("\t%s :: %s" % (i.name, _PASSED_MESSAGE_)) 
					passed += 1 
				else: 
					print("\t%s :: %s" % (i.name, _FAILED_MESSAGE_)) 
					failed += 1 
			else: 
				passed_, failed_ = i.run() 
				passed += passed_ 
				failed += failed_ 
		if print_results: 
			if not failed: 
				print("\n\033[92mAll tests passed.\033[00m\n") 
			else: 
				print("\n\033[92m%d tests passed.\033[00m" % (passed)) 
				print("\033[91m%d tests failed.\033[00m\n" % (failed)) 
		else: 
			pass 
		return [passed, failed] 


class _unittest(object): 

	""" 
	A class designed to hold the information associated with a unit test and 
	subsequently run it. 

	User access of this class is strongly discouraged. 
	""" 

	def __init__(self, name, function): 
		self.name = name 
		self.function = function 

	def __repr__(self): 
		return "%s :: %s" % (self.name, 
			_PASSED_MESSAGE_ if self.run() else _FAILED_MESSAGE_) 

	def __str__(self): 
		return self.__repr__() 

	def __enter__(self): 
		return self 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		return exc_value is None 

	@property 
	def name(self): 
		""" 
		Type :: str 

		The name of the test 
		""" 
		return self._name 

	@name.setter 
	def name(self, value): 
		if isinstance(value, strcomp): 
			self._name = value 
		else: 
			raise TypeError("""Unit test attribute 'name' must be of type \
str. Got: %s""" % (type(value))) 

	@property 
	def function(self): 
		""" 
		Type :: <function> 

		The function to call to conduct the unit test. This must return type 
		bool and take no arguments. 
		""" 
		return self._function 

	@function.setter 
	def function(self, value): 
		if callable(value): 
			self._function = value 
		else: 
			raise TypeError("Unit test function must be a callable object.") 

	def run(self): 
		""" 
		Run this unit test 
		""" 
		return self.function() 


