
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["W18"] 
	from ......testing import moduletest 
	from . import W18 

	@moduletest 
	def test(): 
		r""" 
		vice.yields.ccsne.engines.S16 module test 
		""" 
		return ["vice.yields.ccsne.engines.S16", 
			[ 
				W18.test() 
			] 
		] 

else: pass 

