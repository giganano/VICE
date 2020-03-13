
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = [ 
		"crf", 
		"msmf", 
		"mlr", 
		"test" 
	] 
	from .._test_utils import moduletest 
	from . import _crf as crf 
	from . import _msmf as msmf 
	from . import _mlr as mlr 
	from . import _remnants as remnants 
	from . import ssp 

	@moduletest 
	def test(): 
		""" 
		Run all test functions in this module 
		""" 
		return ["VICE single stellar population functions", 
			[ 
				crf.test_cumulative_return_fraction(), 
				crf.test_setup_cumulative_return_fraction(), 
				msmf.test_main_sequence_mass_fraction(), 
				msmf.test_setup_main_sequence_mass_fraction(), 
				mlr.test_mass_lifetime_relationship(), 
				remnants.test_kalirai08(), 
				ssp.test(run = False) 
			] 
		] 

else: 
	pass 

