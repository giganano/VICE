
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from ....testing import moduletest 
	from . import base 
	from . import builtin_elemental_data 
	from . import elemental_settings 
	from . import evolutionary_settings 
	from . import fromfile 
	from . import history 
	from . import noncustomizable 
	from . import saved_yields 
	from . import yield_settings 

	@moduletest 
	def test(): 
		""" 
		Run the tests on this module 
		""" 
		return ["vice.core.dataframe", 
			[ 
				base.test(run = False), 
				builtin_elemental_data.test(run = False), 
				elemental_settings.test(run = False), 
				evolutionary_settings.test(run = False), 
				fromfile.test(run = False), 
				history.test(run = False), 
				noncustomizable.test(run = False), 
				saved_yields.test(run = False), 
				yield_settings.test(run = False) 
			] 
		] 

else: 
	pass 

