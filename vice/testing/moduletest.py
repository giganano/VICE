""" 
This file implements the moduletest object 
""" 

from __future__ import absolute_import 
__all__ = ["_moduletest"] 
from .unittest import _PASSED_MESSAGE_ 
from .unittest import _FAILED_MESSAGE_ 
from .unittest import _unittest 


class _moduletest: 

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
			raise TypeError("Object must be of type unittest. Got: %s" % (
				type(obj))) 

	def run(self, print_results = False): 
		r""" 
		Run the module tests 
		""" 
		passed = 0 
		failed = 0 
		if self.name is not None: 
			print("\033[96m%s\033[00m" % (self.name)) 
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

