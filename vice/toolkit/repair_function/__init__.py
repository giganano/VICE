r""" 
VICE toolkit: Repaired Functions 

.. versionadded:: 1.X.0 

Contents 
--------
repair_function : <function> 
	Repair a function that was not able to be pickled with a singlezone output 
repfunc : <type> 
	A repaired function object. Implements a linear interpolation scheme 
	under the hood to approximate the value of the lost function at 
	intermediate times. 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["repair_function", "repfunc", "test"] 
	from .repair_function import repair_function 
	from .repfunc import repfunc 
	from .tests import test 

else: 
	pass 
