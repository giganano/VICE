
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = [
		"test", 
		"linalg" 
	] 
	from ..._test_utils import moduletest 
	from . import _linalg as linalg 
	
	def test(run = True): 
		""" 
		Runs all test functions in this module 
		""" 
		test = moduletest("VICE linear algebra functions") 
		test.new(linalg.test_matrix_addition()) 
		test.new(linalg.test_matrix_subtraction()) 
		test.new(linalg.test_matrix_transposition()) 
		test.new(linalg.test_matrix_determinant()) 
		test.new(linalg.test_matrix_inversion()) 
		if run: 
			test.run(print_results = True) 
		else: 
			return test 

else: 
	pass 

