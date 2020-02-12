
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test_all"] 
	from ._linalg import * 
	__all__.extend(_linalg.__all__) 
	
	def test_all(): 
		""" 
		Runs all test functions in this module 
		""" 
		test_matrix_addition() 
		test_matrix_subtraction() 
		test_matrix_transposition() 
		test_matrix_determinant() 
		test_matrix_inversion() 

else: 
	pass 

