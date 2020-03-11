
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = [
		"test", 
		"agb", 
		"ccsne", 
		"sneia", 
		"utils" 
	] 
	from .._test_utils import moduletest 
	from . import _agb as agb 
	from . import _ccsne as ccsne 
	from . import _sneia as sneia 
	from . import _utils as utils 

	@moduletest 
	def test(): 
		return ["VICE File I/O Functions", 
			[ 
				agb.test_agb_grid_import(), 
				ccsne.test_ccsn_yield_grid_reader(), 
				sneia.test_ia_yield_lookup(), 
				utils.test(run = False) 
			] 
		] 

else: 
	pass 
