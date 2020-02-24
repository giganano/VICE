
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = [
		"test", 
		"likelihood" 
	] 
	from .._test_utils import moduletest 
	from . import likelihood 

	def test(run = True): 
		""" 
		Run the tests over this module 
		""" 
		test = moduletest("VICE modeling features") 
		test.new(likelihood.test(run = False)) 
		if run: 
			test.run(print_results = True) 
		else: 
			return test   

else: 
	pass 
