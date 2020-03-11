
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from .._test_utils import moduletest 
	from . import base 
	from . import elemental_settings 
	from . import entrainment 
	from . import evolutionary_settings 
	from . import noncustomizable 
	from . import saved_yields 
	from . import builtins_ 

	@moduletest 
	def test(): 
		return ["VICE dataframe", 
			[ 
				base.test(run = False), 
				elemental_settings.test(run = False), 
				entrainment.test(run = False), 
				evolutionary_settings.test(run = False), 
				noncustomizable.test(run = False), 
				saved_yields.test(run = False), 
				builtins_.test(run = False) 
			] 
		] 

else: 
	pass 

