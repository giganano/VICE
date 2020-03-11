
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
	from ..._test_utils import unittest 
	from . import grid_reader 
	from . import integrator 
	from . import imports 

	@moduletest 
	def test(): 
		""" 
		Run all tests on CCSN nucleosynthetic yield features 
		""" 
		return ["VICE CCSN yield functions", 
			[ 
				grid_reader.test_table(), 
				integrator.test(run = False), 
				imports.test(run = False) 
			] 
		] 

else: 
	pass 

