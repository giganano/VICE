
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test", "trials"] 
	from .._test_utils import moduletest 
	from ._singlezone import singlezone_tester 
	from . import singlezone 

	def test(run = True): 
		test = moduletest("VICE singlezone object") 
		st = singlezone_tester() 
		test.new(st.test_name_setter()) 
		test.new(st.test_func_setter()) 
		test.new(st.test_mode_setter()) 
		test.new(st.test_verbose_setter()) 
		test.new(st.test_elements_setter()) 
		test.new(st.test_imf_setter()) 
		test.new(st.test_eta_setter()) 
		test.new(st.test_enhancement_setter()) 
		test.new(st.test_entrainment()) 
		test.new(st.test_zin_setter()) 
		test.new(st.test_recycling_setter()) 
		test.new(st.test_bins_setter()) 
		test.new(st.test_delay_setter()) 
		test.new(st.test_ria_setter()) 
		test.new(st.test_mg0_setter()) 
		test.new(st.test_smoothing_setter()) 
		test.new(st.test_tau_ia_setter()) 
		test.new(st.test_tau_star_setter()) 
		test.new(st.test_dt_setter()) 
		test.new(st.test_schmidt_setter()) 
		test.new(st.test_mgschmidt_setter()) 
		test.new(st.test_m_upper_setter()) 
		test.new(st.test_m_lower_setter()) 
		test.new(st.test_postMS_setter()) 
		test.new(st.test_z_solar_setter()) 
		test.new(st.test_prep()) 
		test.new(st.test_output_times_check()) 
		test.new(st.test_open_output_dir()) 
		test.new(st.test_setup_elements()) 
		test.new(st.test_set_ria()) 
		test.new(st.test_setup_Zin()) 
		test.new(st.test_save_yields()) 
		test.new(st.test_save_attributes()) 
		test.new(singlezone.test(run = False)) 
		if run: 
			test.run(print_results = True) 
		else: 
			return test 
		
else: 
	pass 
