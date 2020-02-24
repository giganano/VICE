"""
VICE Tests 
========== 
This module includes all of VICE's internal testing routines. The tests are 
implemented in a tree strucutre - all tests can be ran via the test() 
function, or alternatively, individual modules are imported here, and 
their tests can also be ran, by calling their associated test() function 
"""

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = [ 
		"test", 
		"dataframe", 
		"imf", 
		"io", 
		"modeling", 
		"objects", 
		"outputs", 
		"singlezone", 
		"ssp", 
		"stats", 
		"utils", 
		"yields" 
	] 

	from ._test_utils import moduletest 
	from . import dataframe 
	from . import _imf as imf 
	from . import io 
	from . import modeling 
	from . import objects 
	from . import outputs 
	from . import singlezone 
	from . import ssp 
	from . import _stats as stats 
	from . import _utils as utils 
	from . import yields 

	def test(run = True): 
		""" 
		Runs VICE's comprehensive tests 
		""" 
		test = moduletest(None) 
		test.new(singlezone.test(run = False)) 
		test.new(outputs.test(run = False)) 
		test.new(utils.test(run = False)) 
		test.new(imf.test(run = False)) 
		test.new(dataframe.test(run = False)) 
		test.new(io.test(run = False)) 
		test.new(modeling.test(run = False)) 
		test.new(objects.test(run = False)) 
		test.new(ssp.test(run = False)) 
		test.new(stats.test(run = False)) 
		test.new(yields.test(run = False)) 
		if run: 
			header = "VICE Comprehensive Tests\n" 
			for i in range(len(header) - 1): 
				header += "="  
			print("\033[091m%s\033[00m" % (header)) 
			print("This may take a few minutes.") 
			yields.presets.spawn_dummy_yield_file() 
			test.run(print_results = True) 
			yields.presets.remove_dummy_yield_file() 
		else: 
			return test 

else: 
	pass 
