"""
VICE Tests 
========== 
This module includes all of VICE's internal testing routines. 

Functions 
========= 
run_comprehensive_tests 
test_agb_yields
test_cc_yields
test_dataframes
test_ia_yields 
test_ssp
test_sz_output_mirror
"""

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = [ 
		"test", 
		"imf", 
		"modeling", 
		"objects", 
		"ssp", 
		"utils", 
	] 

	from ._test_utils import moduletest 
	from . import _utils as utils 
	from . import _imf as imf 
	from . import modeling 
	from . import objects 
	from . import ssp 
	from . import yields 

	def test(run = True): 
		""" 
		Runs VICE's comprehensive tests 
		""" 
		test = moduletest(None) 
		test.new(utils.test(run = False)) 
		test.new(imf.test(run = False)) 
		test.new(modeling.test(run = False)) 
		test.new(objects.test(run = False)) 
		test.new(ssp.test(run = False)) 
		test.new(yields.test(run = False)) 
		if run: 
			header = "VICE Comprehensive Tests\n" 
			for i in range(len(header) - 1): 
				header += "="  
			print("\033[091m%s\033[00m" % (header)) 
			test.run() 
		else: 
			return test 

else: 
	pass 
