""" 
This package implements the python wrapper of the singlezone object. Source 
code can be found at vice/src/singlezone.h and accompanying files. 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = ["singlezone"] 
	from .singlezone import singlezone 
else: 
	pass 
