""" 
This file implements utility functions for VICE's tests. 
""" 

from __future__ import absolute_import 
__all__ = [
	"moduletest", 
	"unittest" 
] 
from .._globals import _VERSION_ERROR_ 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 


class moduletest(object): 

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
		if isinstance(obj, unittest) or isinstance(obj, moduletest): 
			self._unittests.append(obj) 
		else: 
			raise TypeError("Object must be of type unittest. Got: %s" % (
				type(obj))) 

	def run(self): 
		""" 
		Run the module tests 
		""" 
		if self.name is not None: 
			header = "Testing: %s\n" % (self.name) 
			for i in range(len(header) - 1): 
				header += "=" 
			print("\n\033[96m%s\033[00m" % (header)) 
		else: 
			pass 
		for i in self._unittests: 
			i.run() 


class unittest(object): 

	""" 
	A class designed to hold the information associated with a unit test and 
	subsequently run it. 

	User access of this class is strongly discouraged. 
	""" 

	def __init__(self, name, function): 
		self.name = name 
		self.function = function 

	def __repr__(self): 
		return "%s :: %s" % (self.name, self.message) 

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

	@property 
	def message(self): 
		""" 
		Type :: str 

		The 'success' or 'failure' message as a string. Runs the test 
		automatically. 
		""" 
		if self.function(): 
			return "\033[92mSuccess\033[00m" 
		else: 
			return "\033[91mFailed\033[00m" 

	def run(self): 
		""" 
		Run this unit test 
		""" 
		print("\t%s" % (self.__str__()))  

