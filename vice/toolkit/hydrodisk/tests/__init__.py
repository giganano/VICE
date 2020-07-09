
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from ....testing import moduletest 
	from .hydrodiskstars import * 

	@moduletest 
	def test(): 
		r""" 
		vice.toolkit.hydrodisk module test 
		""" 
		return ["vice.toolkit.hydrodisk", 
			[ 
				test_linear(run = False), 
				test_sudden(run = False), 
				test_diffusion(run = False) 
			] 
		] 

else: 
	pass 
