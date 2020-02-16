
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = [
		"test", 
		"integral" 
	] 
	from .._test_utils import moduletest 
	from . import _integral as integral 

	def test(run = True): 
		""" 
		Run all test functions in this module 
		""" 
		test = moduletest("VICE yield calculation functions") 
		test.new(integral.test()) 
		if run:	
			test.run() 
		else: 
			return test 

else: 
	pass 
