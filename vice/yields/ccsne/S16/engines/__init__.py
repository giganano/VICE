r""" 
Sukhbold et al. (2016), ApJ, 821, 38 core collapse supernova explosion engines. 

**Signature**: from vice.yields.ccsne.S16 import engines 

Contents 
--------
W18 : engine 
	The W18 explosion engine. 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["W18", "test"] 
	from .tests import test  
	from .W18 import W18 
	W18 = W18() 

else: 
	pass 

