
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from ....testing import moduletest 
	from .repair_function import test_repair_function 
	from ._repfunc import test as test_repfunc 

	@moduletest 
	def test(): 
		r""" 
		vice.toolkit.repair_function module test 
		""" 
		return ["vice.toolkit.repair_function", 
			[
				test_repair_function(), 
				test_repfunc(run = False)  
			] 
		] 

else: 
	pass 
