
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from .....testing import moduletest 
	from ._generic import generic_test 
	from ._no_migration import no_migration_test 
	from ._separation import separation_test 

	@moduletest 
	def test(): 
		r""" 
		vice.core.multizone edge cases module test 
		""" 
		return ["vice.core.multizone edge cases", 
			[ 
				generic_test(run = False), 
				no_migration_test(run = False), 
				separation_test(run = False) 
			] 
		] 

else: 
	pass 
