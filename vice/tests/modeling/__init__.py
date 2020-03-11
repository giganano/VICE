
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

	@moduletest 
	def test(run = True): 
		""" 
		Run the tests over this module 
		""" 
		return ["VICE modeling features", 
			[ 
				likelihood.test(run = False) 
			] 
		] 

else: 
	pass 
