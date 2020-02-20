
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from ..._test_utils import moduletest 
	from . import lookup 

	def test(run = True): 
		test = moduletest("SN Ia yield functions") 
		test.new(lookup.test(run = False)) 
		if run: 
			test.run() 
		else: 
			return test 

else: 
	pass 

