r""" 
VICE Interpolation Schema : Internal utilities for interpolation. 

.. versionadded:: 1.X.0 

Contents 
--------
interp_scheme_1d : object 
	A 1-d linear interpolation scheme given a list of (x, y) points. 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["interp_scheme_1d", "test"] 
	from .interp_scheme_1d import interp_scheme_1d 
	from .tests import test 

else: pass 
