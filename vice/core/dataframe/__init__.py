""" 
The VICE dataframe 
================== 
This package implements the VICE dataframe and all of its subclasses. Users 
should not create their own instances of VICE dataframe subclasses, but should 
feel free to use the base class however they choose. 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = [ 
		"agb_yield_settings", 
		"base", 
		"elemental_settings", 
		"evolutionary_settings", 
		"fromfile", 
		"history", 
		"noncustomizable", 
		"saved_yield", 
		"tracers", 
		"yield_settings", 
		"zone_entrainment" 
	] 

	from ._agb_yield_settings import agb_yield_settings 
	from ._base import base 
	from ._elemental_settings import elemental_settings 
	from ._evolutionary_settings import evolutionary_settings 
	from ._fromfile import fromfile 
	from ._history import history 
	from ._noncustomizable import noncustomizable 
	from ._saved_yields import saved_yields 
	from ._tracers import tracers 
	from ._yield_settings import yield_settings 
	from ._entrainment import zone_entrainment 
	from ._builtin_dataframes import * 
	__all__.extend(_builtin_dataframes.__all__) 

else: 
	pass 

