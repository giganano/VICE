
``VICE`` Tests 
==============
``VICE`` provides a set of comprehensive tests, which users can run from the 
root directory of this repository via ``make tests``. If users have installed 
``VICE`` for multiple versions of ``python``, this command is chained to 
both ``python 2`` and ``python 3`` via ``make tests2`` and ``make tests3``. 

Alternatively, users may open ``ipython``, a ``jupyter notebook``, or some 
other variant thereof to run the tests. For example: 

..code:: python 

	from vice.tests import * 

	# run all tests 
	run_comprehensive_tests() 

	# run tests on AGB yield grid reader 
	test_agb_yields() 

	# run tests on core collapse supernovae yield calculations 
	test_cc_yields() 

	# run tests on type Ia supernovae yield calculations 
	test_ia_yields() 

	# run tests on single stellar population features 
	test_ssp() 

	# run tests on singlezone and output objects as well as mirror function 
	test_sz_output_mirror() 

	# run tests on VICE dataframes 
	test_dataframes() 


