
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
	from . import builtins_ 

	def test(run = True): 
		test = moduletest("VICE dataframe") 
		test.new(base.test(run = False)) 
		test.new(elemental_settings.test(run = False)) 
		test.new(builtins_.test(run = False)) 
		if run: 
			test.run() 
		else: 
			return test 

else: 
	pass 

