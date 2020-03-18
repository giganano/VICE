
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
	from ....testing import moduletest 
	from . import _linalg as linalg 
	
	@moduletest 
	def test(): 
		""" 
		Runs all test functions in this module 
		""" 
		return ["vice.modeling.likelihood.tests", 
			[ 
				linalg.test(run = False) 
			] 
		] 

else: 
	pass 

