
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from ....testing import moduletest 
	from . import mig_matrix_row 
	from . import mig_matrix 

	@moduletest 
	def test(): 
		return ["vice.core.multizone", 
			[
				mig_matrix_row.test(run = False), 
				mig_matrix.test(run = False) 
			]
		] 

else: 
	pass 
