# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import 
__all__ = ["kroupa", "salpeter"] 
import numbers 
from . cimport _imf 


def kroupa(mass): 
	""" 
	The Kroupa (2001) stellar initial mass function (IMF). 

	Parameters 
	========== 
	mass :: real number 
		The stellar mass in Msun 

	Returns 
	======= 
	dndm :: real number 
		The unnormalized value of the Kroupa IMF at that stellar mass, 
		defined as dN/dm 

	Raises 
	====== 
	TypeError :: 
		::	mass is not a real number 
	ValueError :: 	
		::	mass is non-positive 

	References 
	========== 
	Kroupa (2001), MNRAS, 322, 231 
	""" 
	return _common(mass, _imf.kroupa01) 


def salpeter(mass): 
	""" 
	The Salpeter (1955) stellar initial mass function (IMF). 

	Parameters 
	========== 
	mass :: real number 
		The stellar mass in Msun 

	Returns 
	======= 
	dndm :: real number 
		The unnormalized value of the Salpeter IMF at that stellar mass, 
		define as dN/dm 

	Raises 
	====== 
	TypeError :: 
		::	mass is not a real number 
	ValueError :: 	
		::	mass is non-positive 

	References 
	========== 
	Salpeter (1955), ApJ, 121, 161 
	""" 
	return _common(mass, _imf.salpeter55) 


def _common(mass, builtin_imf): 
	""" 
	Evaluate the built-in IMF 

	Parameters 
	========== 
	mass :: real number 
		The stellar mass in Msun 
	builtin_IMF :: <function> 
		The function to send the mass to which will evaluate the IMF 

	Returns 
	======= 
	dndm :: real number 
		The unnormalized value of the IMF at that stellar mass, defined as 
		dN/dm 

	Raises 
	====== 
	TypeError :: 
		::	mass is not a real number 
	ValueError :: 	
		::	mass is non-positive 
	""" 
	if isinstance(mass, numbers.Number): 
		if mass > 0: 
			return builtin_imf(<double> mass) 
		else: 
			raise ValueError("Mass must be positive. Got: %g" % (mass)) 
	else: 
		raise TypeError("Mass must be a real number. Got: %s" % (type(mass))) 

