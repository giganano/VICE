
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = [
		"test", 
		"agb", 
		"integral" 
	] 
	from .._test_utils import moduletest 
	from . import agb 
	from . import ccsne 
	from . import sneia 
	from . import presets 
	from . import _integral as integral 

	@moduletest 
	def test(): 
		""" 
		Run all test functions in this module 
		""" 
		return ["VICE yield calculation functions", 
			[ 
				agb.test(run = False), 
				ccsne.test(run = False), 
				sneia.test(run = False), 
				integral.test(run = False), 
				presets.test(run = False) 
			] 
		] 

else: 
	pass 
