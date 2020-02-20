
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = [
		"test" 
	] 
	from ..._test_utils import moduletest 
	from . import integrator 
	from . import imports 

	def test(run = True): 
		test = moduletest("VICE CCSN yield functions") 
		test.new(integrator.test(run = False)) 
		test.new(imports.test(run = False)) 
		if run: 
			test.run() 
		else: 
			return test 

else: 
	pass 

