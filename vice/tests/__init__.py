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

	@moduletest 
	def test(): 
		""" 
		Runs VICE's comprehensive tests 
		""" 
		header = "VICE Comprehensive Tests\n" 
		for i in range(len(header) - 1): 
			header += "=" 
		print("\033[091m%s\033[00m" % (header)) 
		print("This may take a few minutes.") 
		return [None, 
			[ 
				singlezone.test(run = False), 
				outputs.test(run = False), 
				utils.test(run = False), 
				imf.test(run = False), 
				dataframe.test(run = False), 
				io.test(run = False), 
				modeling.test(run = False), 
				ssp.test(run = False), 
				stats.test(run = False), 
				yields.test(run = False) 
			] 
		] 

else: 
	pass 
