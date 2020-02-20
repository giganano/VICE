
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = [
		"test", 
		"agb", 
		"integral" 
	] 
	from .._test_utils import moduletest 
	from . import agb 
	from . import ccsne 
	from . import sneia 
	from . import _integral as integral 

	def test(run = True): 
		""" 
		Run all test functions in this module 
		""" 
		test = moduletest("VICE yield calculation functions") 
		test.new(agb.test(run = False)) 
		test.new(ccsne.test(run = False)) 
		test.new(sneia.test(run = False)) 
		test.new(integral.test(run = False)) 
		if run:	
			test.run() 
		else: 
			return test 

else: 
	pass 
