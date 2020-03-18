
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from ....tests._test_utils import moduletest 
	from ....tests._test_utils import unittest 
	from . import grid_reader 
	from . import integrator 
	from . import imports 

	@moduletest 
	def test(): 
		""" 
		Run all tests on CCSN nucleosynthetic yield features 
		""" 
		return ["vice.yields.ccsne", 
			[ 
				grid_reader.test_table(), 
				imports.test(run = False), 
				integrator.test(run = False) 
			] 
		] 

else: 
	pass 

