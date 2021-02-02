r""" 
Built-in stellar radial migration schema for disk galaxies inspired by 
hydrodynamical simulations. 

.. versionadded:: 1.2.0 

Contents 
--------
hydrodiskstars : object 
	A stellar migration scheme inspired by a cosmological zoom-in simulation 
	of a Milky Way-like galaxy ran at the University of Washington. Stellar 
	populations can migrate according to a handful of assumptions about the 
	time dependence of their orbital radius between birth and the end of the 
	simulation. 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["hydrodiskstars", "test"]  
	from .hydrodiskstars import hydrodiskstars 
	from .tests import test 

else: 
	pass 

