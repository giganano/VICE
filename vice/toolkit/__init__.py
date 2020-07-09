r""" 
VICE Toolkit : General utilities to maximize VICE's computational power and 
user-friendliness. 

.. versionadded:: 1.X.0 

Contents 
--------
repair_function : <function> 
	Obtain an approximation of a function which could not be pickled with a 
	VICE output from the output itself. 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["hydrodisk", "repair_function", "test"] 
	from ..testing import moduletest 
	from .repair_function import repair_function 
	from .repair_function import test as test_repfunc 
	from . import hydrodisk 

	@moduletest 
	def test(): 
		r""" 
		vice.toolkit module test 
		""" 
		return ["vice.toolkit", 
			[
				hydrodisk.test(run = False), 
				test_repfunc(run = False) 
			] 
		] 

else: 
	pass 
