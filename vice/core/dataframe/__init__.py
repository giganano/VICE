r""" 
The VICE dataframe 
================== 
Provides a means of storing and accessing data with both case-insensitive 
strings and integers, allowing both indexing and calling. 

Derived Classes: 
	- builtin_elemental_data 
	- elemental_settings 
	- evolutionary_settings 
	- fromfile 
	- history 
	- noncustomizable 
	- saved_yields 
	- yield_settings 

Built-in Instances: 
	- atomic_number 
	- primordial 
	- solar_z 
	- sources 
	- stable_isotopes 

.. note:: All built-in instances are of the derived class 
	``builtin_elemental_data``. 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = [ 
		"base", 
		"builtin_elemental_data", 
		"elemental_settings", 
		"evolutionary_settings", 
		"fromfile", 
		"history", 
		"noncustomizable", 
		"saved_yields", 
		"yield_settings", 
		"test" 
	] 

	from ...testing import moduletest 
	from ._base import base 
	from ._builtin_elemental_data import builtin_elemental_data 
	from ._elemental_settings import elemental_settings 
	from ._evolutionary_settings import evolutionary_settings 
	from ._fromfile import fromfile 
	from ._history import history 
	from ._noncustomizable import noncustomizable 
	from ._saved_yields import saved_yields 
	from ._yield_settings import yield_settings 
	from ._builtin_dataframes import * 
	from . import tests 
	__all__.extend(_builtin_dataframes.__all__) 

	@moduletest 
	def test(): 
		r""" 
		Run the tests on this module 
		""" 
		return ["vice.core.dataframe", 
			[
				tests.test(run = False), 
				_builtin_dataframes.test(run = False) 
			] 
		] 

else: 
	pass 

