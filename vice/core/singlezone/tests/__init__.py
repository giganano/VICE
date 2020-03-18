
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test", "trials"] 
	from ....tests._test_utils import moduletest 
	from ._singlezone import singlezone_tester 
	from . import singlezone 

	@moduletest 
	def test(): 
		st = singlezone_tester() 
		return ["VICE singlezone object", 
			[ 
				st.test_name_setter(), 
				st.test_func_setter(), 
				st.test_mode_setter(), 
				st.test_verbose_setter(), 
				st.test_elements_setter(), 
				st.test_imf_setter(), 
				st.test_eta_setter(), 
				st.test_enhancement_setter(), 
				st.test_entrainment(), 
				st.test_zin_setter(), 
				st.test_recycling_setter(), 
				st.test_bins_setter(), 
				st.test_delay_setter(), 
				st.test_ria_setter(), 
				st.test_mg0_setter(), 
				st.test_smoothing_setter(), 
				st.test_tau_ia_setter(), 
				st.test_tau_star_setter(), 
				st.test_dt_setter(), 
				st.test_schmidt_setter(), 
				st.test_mgschmidt_setter(), 
				st.test_m_upper_setter(), 
				st.test_m_lower_setter(), 
				st.test_postMS_setter(), 
				st.test_z_solar_setter(), 
				st.test_prep(), 
				st.test_output_times_check(), 
				st.test_open_output_dir(), 
				st.test_setup_elements(), 
				st.test_set_ria(), 
				st.test_setup_Zin(), 
				st.test_pickle(), 
				singlezone.test(run = False) 
			] 
		] 
		
else: 
	pass 
