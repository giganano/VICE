# This file, included with the VICE package, is protected under the terms of the 
# associated MIT License, and any use or redistribution of this file in original 
# or altered form is subject to the copyright terms therein. 

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

from test_agb_yields import main as test_agb_yields 
from test_cc_yields import main as test_cc_yields 
from test_dataframes import main as test_dataframes 
from test_ia_yields import main as test_ia_yields 
from test_ssp import main as test_ssp 
from test_sz_output_mirror import main as test_sz_output_mirror 

def run_comprehensive_tests(): 
	"""
	Runs the full comprehensive set of tests. 
	"""
	print("""\
Running comprehensive tests. This will take several minutes, the exact \
duration depending on the processing speed of the system. \
""")
	test_sz_output_mirror() 
	test_agb_yields() 
	test_cc_yields() 
	test_dataframes() 
	test_ia_yields() 
	test_ssp() 


