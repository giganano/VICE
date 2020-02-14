
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = ["test_all"] 

	from ._integral import * 
	__all__.extend(_integral.__all__) 

	def test_all(): 
		""" 
		Run all test functions in this module 
		""" 
		test_euler() 
		test_trapezoid() 
		test_midpoint() 
		test_simpson() 

else: 
	pass 
