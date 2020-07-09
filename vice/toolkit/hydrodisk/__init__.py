r""" 
Built-in stellar radial migration schema for Milky Way-like disk galaxy 
models. Stellar populations can migrate according to a handful of assumptions 
about the time dependence of their orbital radius between birth and the end of 
the simulation. 

Contents 
--------
linear : object 
	The orbital radii at times between birth and 12.8 Gyr are assigned via 
	linear interpolation. Stellar populations therefore spiral uniformly 
	inward or outward. 
sudden : object 
	The time of migration is randomly drawn from a uniform distrbution between 
	when a stellar population is born and 12.8 Gyr. At times prior to this, it 
	is at its radius of birth, and after this, it is at its final radius. 
	Stellar populations therefore spend no time at intermediate radii. 
diffusion : object 
	The orbital radius at times between birth and 12.8 Gyr are assigned via a 
	sqrt(time) dependence, approximating a random-walk motion. Stellar 
	populations therefore spiral inward or outward, but slightly faster than 
	the linear approximation when they are young. 

.. note:: Simulations which adopt these models that run for longer than 12.8 
	Gyr are not supported. Stellar populations in the built-in hydrodynamical 
	simulation data span 12.8 Gyr of ages. 
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

