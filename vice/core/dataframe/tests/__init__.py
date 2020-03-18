
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from ....testing import moduletest 
	from . import base 
	from . import elemental_settings 
	from . import entrainment 
	from . import evolutionary_settings 
	from . import noncustomizable 
	from . import saved_yields 

	@moduletest 
	def test(): 
		""" 
		Run the tests on this module 
		""" 
		return ["vice.core.dataframe.tests", 
			[ 
				base.test(run = False), 
				elemental_settings.test(run = False), 
				entrainment.test(run = False), 
				evolutionary_settings.test(run = False), 
				noncustomizable.test(run = False), 
				saved_yields.test(run = False), 
			] 
		] 

else: 
	pass 

