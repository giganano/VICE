
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
	
	@moduletest 
	def test(): 
		""" 
		Runs all test functions in this module 
		""" 
		return ["VICE linear algebra functions", 
			[ 
				linalg.test_matrix_addition(), 
				linalg.test_matrix_subtraction(), 
				linalg.test_matrix_transposition(), 
				linalg.test_matrix_determinant(), 
				linalg.test_matrix_inversion() 
			] 
		] 

else: 
	pass 

