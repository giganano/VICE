""" 
This file implements the unittest object 
""" 

from __future__ import absolute_import 
__all__ = ["_unittest"] 
from .._globals import _VERSION_ERROR_ 
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
_SKIPPED_MESSAGE_ = "\033[94mSkipped\033[00m" 


class _unittest: 

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
			{
				True: 		_PASSED_MESSAGE_, 
				False: 		_FAILED_MESSAGE_, 
				None: 		_SKIPPED_MESSAGE_ 
			}[self.run()]) 
			# _PASSED_MESSAGE_ if self.run() else _FAILED_MESSAGE_) 

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

