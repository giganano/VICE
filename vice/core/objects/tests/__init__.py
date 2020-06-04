
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = [ 
		"test", 
		"agb", 
		"callback_1arg", 
		"callback_2arg", 
		"ccsne", 
		"channel", 
		"element", 
		"fromfile", 
		"imf", 
		"integral", 
		"ism", 
		"mdf", 
		"singlezone", 
		"sneia", 
		"ssp" 
	] 

	from ....testing import moduletest 
	from . import _agb as agb 
	from . import _callback_1arg as callback_1arg 
	from . import _callback_2arg as callback_2arg 
	from . import _ccsne as ccsne 
	from . import _channel as channel 
	from . import _element as element 
	from . import _fromfile as fromfile 
	from . import _imf as imf 
	from . import _integral as integral 
	from . import _ism as ism 
	from . import _mdf as mdf 
	from . import _singlezone as singlezone 
	from . import _sneia as sneia 
	from . import _ssp as ssp 

	@moduletest 
	def test(): 
		""" 
		Runs all test functions in this module 
		""" 
		return ["vice.core.objects.tests", 
			[ 
				agb.test_agb_grid_constructor(), 
				agb.test_agb_grid_destructor(), 
				callback_1arg.test_callback_1arg_constructor(), 
				callback_1arg.test_callback_1arg_destructor(), 
				callback_2arg.test_callback_2arg_constructor(), 
				callback_2arg.test_callback_2arg_destructor(), 
				ccsne.test_ccsne_yield_specs_constructor(), 
				ccsne.test_ccsne_yield_specs_destructor(), 
				channel.test_channel_constructor(), 
				channel.test_channel_destructor(), 
				element.test_element_constructor(), 
				element.test_element_destructor(), 
				fromfile.test_fromfile_constructor(), 
				fromfile.test_fromfile_destructor(), 
				imf.test_imf_constructor(), 
				imf.test_imf_destructor(), 
				integral.test_integral_constructor(), 
				integral.test_integral_destructor(), 
				ism.test_ism_constructor(), 
				ism.test_ism_destructor(), 
				mdf.test_mdf_constructor(), 
				mdf.test_mdf_destructor(), 
				singlezone.test_singlezone_constructor(), 
				singlezone.test_singlezone_destructor(), 
				sneia.test_sneia_yield_specs_constructor(), 
				sneia.test_sneia_yield_specs_destructor(), 
				ssp.test_ssp_constructor(), 
				ssp.test_ssp_destructor() 
			] 
		] 

else: 
	pass 
