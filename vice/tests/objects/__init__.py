
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = ["test_all"] 

	from ._agb import * 
	from ._ccsne import * 
	from ._channel import * 
	from ._dataset import * 
	from ._element import * 
	from ._fromfile import * 
	from ._imf import * 
	from ._integral import * 
	from ._ism import * 
	from ._mdf import * 
	from ._migration import * 
	from ._multizone import * 
	from ._singlezone import * 
	from ._sneia import * 
	from ._ssp import * 
	from ._tracer import * 

	__all__.extend(_agb.__all__) 
	__all__.extend(_ccsne.__all__) 
	__all__.extend(_channel.__all__) 
	__all__.extend(_dataset.__all__) 
	__all__.extend(_element.__all__) 
	__all__.extend(_fromfile.__all__) 
	__all__.extend(_imf.__all__) 
	__all__.extend(_integral.__all__) 
	__all__.extend(_ism.__all__) 
	__all__.extend(_mdf.__all__) 
	__all__.extend(_migration.__all__) 
	__all__.extend(_multizone.__all__) 
	__all__.extend(_singlezone.__all__) 
	__all__.extend(_sneia.__all__) 
	__all__.extend(_ssp.__all__) 
	__all__.extend(_tracer.__all__) 

	def test_all(): 
		""" 
		Runs all test functions in this module 
		""" 
		test_agb_grid_constructor() 
		test_agb_grid_destructor() 
		test_ccsne_yield_specs_constructor() 
		test_ccsne_yield_specs_destructor() 
		test_channel_constructor() 
		test_channel_destructor() 
		test_dataset_constructor() 
		test_dataset_destructor() 
		test_element_constructor() 
		test_element_destructor() 
		test_fromfile_constructor() 
		test_fromfile_destructor() 
		test_imf_constructor() 
		test_imf_destructor() 
		test_integral_constructor() 
		test_integral_destructor() 
		test_ism_constructor() 
		test_ism_destructor() 
		test_mdf_constructor() 
		test_mdf_destructor() 
		test_migration_constructor() 
		test_migration_destructor() 
		test_multizone_constructor() 
		test_multizone_destructor() 
		test_singlezone_constructor() 
		test_singlezone_destructor() 
		test_sneia_yield_specs_constructor() 
		test_sneia_yield_specs_destructor() 
		test_ssp_constructor() 
		test_ssp_destructor() 
		test_tracer_constructor() 
		test_tracer_destructor() 

else: 
	pass 
