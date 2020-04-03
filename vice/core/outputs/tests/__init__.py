
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from ....testing import moduletest 
	from . import outputs 
	from . import output 

	@moduletest 
	def test(): 
		r""" 
		vice.outputs moduletest 
		""" 
		return ["vice.core.outputs", 
			[ 
				outputs.test(run = False), 
				output.test(run = False) 
			] 
		] 

else: 
	pass 

