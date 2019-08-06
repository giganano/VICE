
from test_agb_yields import main as test_agb_yields 
from test_cc_yields import main as test_cc_yields 
from test_dataframes import main as test_dataframes 
from test_ia_yields import main as test_ia_yields 
from test_presets import main as test_presets 
from test_ssp import main as test_ssp 
from test_sz_output_mirror import main as test_sz_output_mirror 

if __name__ == "__main__": 
	print("""\
Running comprehensive tests. This will take several minutes, the exact \
duration depending on the processing speed of the system. \
""")
	test_sz_output_mirror() 
	test_presets() 
	test_agb_yields() 
	test_cc_yields() 
	test_dataframes() 
	test_ia_yields() 
	test_ssp() 



