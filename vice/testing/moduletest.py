""" 
This file implements the moduletest object 
""" 

from __future__ import absolute_import 
__all__ = ["_moduletest"] 
from .unittest import _SKIPPED_MESSAGE_ 
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
		elif obj is not None:  
			raise TypeError("Object must be of type unittest. Got: %s" % (
				type(obj))) 
		else: 
			# the root moduletest being ran will return None when finished. 
			pass 

	def run(self, print_results = False): 
		r""" 
		Run the module tests 
		""" 
		passed = 0 
		failed = 0 
		skipped = 0 
		if self.name is not None: 
			print("\033[96m%s\033[00m" % (self.name)) 
		else: 
			pass 
		for i in self._unittests: 
			if isinstance(i, _unittest): 
				x = i.run() 
				msg = "\t%s :: " % (i.name) 
				if x is None: 
					msg += _SKIPPED_MESSAGE_
					skipped += 1  
				elif x: 
					msg += _PASSED_MESSAGE_ 
					passed += 1 
				else: 
					msg += _FAILED_MESSAGE_ 
					failed += 1 
				print(msg) 
			else: 
				passed_, failed_, skipped_ = i.run() 
				passed += passed_ 
				failed += failed_ 
				skipped += skipped_ 
		if print_results: 
			if not failed and not skipped: 
				print("\n\033[92mAll tests passed.\033[00m\n") 
			else: 
				print("\n\033[92m%d tests passed.\033[00m" % (passed)) 
				print("\033[91m%d tests failed.\033[00m" % (failed)) 
				print("\033[94m%d tests skipped.\033[00m\n" % (skipped)) 
		else: 
			pass 
		return [passed, failed, skipped] 

