r""" 
Built-in stellar radial migration schema for disk galaxy models 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["linear", "sudden", "diffusion", "test"]  
	from .hydrodiskstars import linear 
	from .hydrodiskstars import sudden 
	from .hydrodiskstars import diffusion 
	from .tests import test 

else: 
	pass 

