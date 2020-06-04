""" 
This file implements the unittest and moduletest decorators for testing 
""" 

from __future__ import absolute_import 
__all__ = ["moduletest", "unittest"] 
from .moduletest import _moduletest 
from .unittest import _unittest 
import functools 
import inspect 


def moduletest(function): 
	""" 
	A decorator which will construct a moduletest automatically from a 
	description and a list of unittest objects 
	""" 
	@functools.wraps(function) 
	def wrapper(run = True): 
		try: 
			description, unittests = function() 
		except TypeError: 
			print(inspect.getfile(function)) 
			print(function) 
			raise 
		test = _moduletest(description) 
		if unittests is None: 
			test.new(skip_dummy(description)) 
		else:  
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



@unittest 
def skip_dummy(description): 
	r""" 
	Produces a skip message for a module test 
	""" 
	def test(): 
		return None 
	return [description, test] 

