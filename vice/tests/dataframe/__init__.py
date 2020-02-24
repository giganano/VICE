
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from .._test_utils import moduletest 
	from . import base 
	from . import elemental_settings 
	from . import entrainment 
	from . import evolutionary_settings 
	from . import noncustomizable 
	from . import saved_yields 
	from . import builtins_ 

	def test(run = True): 
		test = moduletest("VICE dataframe") 
		test.new(base.test(run = False)) 
		test.new(elemental_settings.test(run = False)) 
		test.new(entrainment.test(run = False)) 
		test.new(evolutionary_settings.test(run = False)) 
		test.new(noncustomizable.test(run = False)) 
		test.new(saved_yields.test(run = False)) 
		test.new(builtins_.test(run = False)) 
		if run: 
			test.run(print_results = True)  
		else: 
			return test 

else: 
	pass 

