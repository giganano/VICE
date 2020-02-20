
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 


if not __VICE_SETUP__: 

	from vice.tests import test 
	test(run = True) 

else: 
	pass 

