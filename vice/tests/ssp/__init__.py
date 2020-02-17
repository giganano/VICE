
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

	def test(run = True): 
		""" 
		Run all test functions in this module 
		""" 
		test = moduletest("VICE single stellar population functions") 
		test.new(_crf.test_cumulative_return_fraction()) 
		test.new(_msmf.test_main_sequence_mass_fraction()) 
		test.new(_mlr.test_mass_lifetime_relationship()) 
		if run: 
			test.run() 
		else: 
			return test 

else: 
	pass 

