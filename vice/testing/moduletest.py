r""" 
**VICE Developer's Documentation** 

This file implements an object used for "module testing", or stitching 
together a series of unit tests. The decorators.py file implements the 
decorator @moduletest, which can be attached to a function that returns a name 
of the module test and a list containing unit test and other module test 
objects. 
""" 

from __future__ import absolute_import 
__all__ = ["_moduletest"] 
from .unittest import _SKIPPED_MESSAGE_ 
from .unittest import _PASSED_MESSAGE_ 
from .unittest import _FAILED_MESSAGE_ 
from .unittest import _unittest 


class _moduletest: 

	r""" 
	**VICE Developer's Documentation** 
	
	The base class for a module test in VICE, or stitching together a series 
	of unit tests. 

	**Signature**: moduletest(name) 

	Parameters 
	----------
	name : ``str`` 
		The attribute ``name``. See below. 

	Attributes 
	----------
	name : ``str`` 
		The name of the module test. 
	unittests : ``list`` 
		A list of the unit tests contained in this module test, as well as 
		other module tests contained within this one. 

	Functions 
	---------
	new : instance method 
		Add a new unit test or module test object to this one. 
	run : instance method 
		Run all unit tests and module tests contained within this one. 
	""" 

	def __init__(self, name): 
		self.name = name 
		self._unittests = [] 

	@property 
	def name(self): 
		r""" 
		**VICE Developer's Documentation 

		Type : ``str`` 

		The name of the module test. 
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
		r""" 
		**VICE Developer's Documentation** 

		Type : ``list`` 

		The unit tests in this module test. 
		""" 
		return self._unittests 

	def new(self, obj): 
		r""" 
		**VICE Developer's Documentation** 

		Add a unit test to this module test. 

		**Signature**: x.new(obj) 

		Parameters 
		----------
		x : ``moduletest`` 
			An instance of this class. 
		obj : ``unittest`` or ``moduletest`` 
			The unittest or another moduletest object to add to this one. 
		""" 
		if isinstance(obj, _unittest) or isinstance(obj, _moduletest): 
			self._unittests.append(obj) 
		elif obj is not None:  
			raise TypeError("""\
Object must be of type unittest or moduletest. Got: %s""" % (type(obj))) 
		else: 
			# the root moduletest being ran will return None when finished. 
			pass 

	def run(self, print_results = True): 
		r""" 
		**VICE Deverloper's Documentation** 

		Run the module tests. 

		**Signature**: x.run(print_results = True) 

		Parameters 
		----------
		x : ``moduletest`` 
			An instance of this class. 
		print_results : ``bool`` [default : True] 
			Whether or not to print the total number of tests that pass, fail, 
			and skip. 
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
				passed_, failed_, skipped_ = i.run(print_results = False) 
				passed += passed_ 
				failed += failed_ 
				skipped += skipped_ 
		if print_results: 
			if not failed and not skipped: 
				print("\n\033[92mAll tests passed. (%d)\033[00m\n" % (passed)) 
			else: 
				print("\n\033[92m%d tests passed.\033[00m" % (passed)) 
				print("\033[91m%d tests failed.\033[00m" % (failed)) 
				print("\033[94m%d tests skipped.\033[00m\n" % (skipped)) 
		else: 
			pass 
		return [passed, failed, skipped] 

