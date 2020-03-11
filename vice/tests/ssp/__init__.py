
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = [
		"test", 
	] 
	from .._test_utils import moduletest 
	from . import _crf 
	from . import _msmf 
	from . import _mlr 
	from . import ssp 

	@moduletest 
	def test(): 
		""" 
		Run all test functions in this module 
		""" 
		return ["VICE single stellar population functions", 
			[ 
				_crf.test_cumulative_return_fraction(), 
				_msmf.test_main_sequence_mass_fraction(), 
				_mlr.test_mass_lifetime_relationship(), 
				ssp.test(run = False) 
			] 
		] 

else: 
	pass 

