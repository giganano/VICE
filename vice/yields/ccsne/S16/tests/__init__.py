
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from .....testing import moduletest 
	from . import set_params 
	from ..engines.tests import test as test_engines 

	@moduletest 
	def test(): 
		r""" 
		Run the unit tests on this moudle 
		""" 
		return ["vice.yields.ccsne.S16", 
			[ 
				set_params.test(), 
				test_engines(run = False) 
			] 
		] 

else: 
	pass 
