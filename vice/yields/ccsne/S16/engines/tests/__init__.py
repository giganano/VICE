
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	from ......testing import moduletest 
	from . import W18  

	@moduletest 
	def test(): 
		r""" 
		vice.yields.ccsne.S16.engines module test 
		""" 
		return ["vice.yields.ccsne.S16.engines", 
			[ 
				W18.test_W18() 
			] 
		] 

else: 
	pass 

