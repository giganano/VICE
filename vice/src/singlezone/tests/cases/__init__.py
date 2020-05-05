
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__:

	__all__ = ["test"] 
	from .....testing import moduletest 
	from ._quiescence import quiescence_test 

	@moduletest 
	def test(): 
		r""" 
		vice.core.singlezone edge cases 
		""" 
		return ["vice.core.singlezone edge cases", 
			[
				quiescence_test(run = False) 
			] 
		] 

else: 
	pass 
