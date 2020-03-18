
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = [
		"singlechain", 
		"parameter", 
		"test" 
	] 
	from ..tests._test_utils import moduletest 
	from .singlechain import singlechain 
	from .singlechain import parameter 
	from . import likelihood 

	@moduletest 
	def test(): 
		""" 
		Run all tests on this module 
		""" 
		return ["vice.modeling", 
			[
				likelihood.test(run = False) 
			] 
		] 

else: 
	pass 
