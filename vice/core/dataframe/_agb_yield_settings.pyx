# cython: language_level = 3, boundscheck = False
""" 
This file implements the agb_yield_settings object, a subclass of the 
yield_settings object. This object allows strings denoting tables for 
built-in yield studies and functions of two real numbers, interpreted as 
stellar mass in Msun and metallicity by mass. 
""" 

from ..._globals import _VERSION_ERROR_ 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
import numbers 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from . cimport _agb_yield_settings 


#------------------------ AGB YIELD SETTINGS SUBCLASS ------------------------# 
cdef class agb_yield_settings(yield_settings): 

	""" 
	A subclass of the yield_settings subclass which allows either functions 
	that accept TWO (rather than one) numerical values or a string denoting a 
	particular study. 

	There is only one instance of this class within VICE - the user's 
	AGB star yield settings at vice.yields.agb.settings. These dataframes 
	should NOT be directly assigned by the user; that is, only their existing 
	fields should be modified. 

	vice.yields.agb.settings 
	======================== 
	Fractional yields from AGB stars as a function of stellar mass and total 
	metallicity Z. 

	See docstring of VICE dataframe base class for more information. 
	""" 

	def __init__(self, frame, name, allow_funcs, config_field): 
		"""
		Parameters 
		========== 
		frame :: dict 
			A python dictionary to construct the dataframe from 
		""" 
		#=====================================================================#
		"""
		(The above docstring is entered purely to keep the visible __init__ 
		docstring consistent across subclasses and instances of the VICE 
		dataframe. Below is the actual docstring for this function.)

		Parameters
		==========
		frame :: dict 
			A python dictionary to construct the dataframe from 
		name :: str 
			A string denoting the name of the objects stored as fields in 
			this dataframe (i.e. core-collapse yield settings.) 
		allow_funcs :: bool 
			A boolean describing whether or not functional attribute are allowed 
		config_field :: str 
			The name of the '.config' file that is stored whenever the user 
			saves new default yield settings. 
		""" 
		msg = "Custom instances of this dataframe are not allowed." 
		assert config_field == "agb", msg  
		assert allow_funcs, msg 
		assert name == "AGB yield", msg 
		super().__init__(frame, name, allow_funcs, config_field) 

	def __setitem__(self, key, value): 
		# These import statements cause import errors when in the preamble 
		from ...yields.agb._grid_reader import _RECOGNIZED_STUDIES_ 
		from ._builtin_dataframes import atomic_number 

		if isinstance(key, strcomp): 
			if key.lower() in _RECOGNIZED_ELEMENTS_: 
				if isinstance(value, strcomp): 
					if value.lower() in _RECOGNIZED_STUDIES_: 
						if (value.lower() == "karakas10" and 
							atomic_number[key] > 28): 
							""" 
							Karakas et al. (2010) table only goes up to Ni. 
							""" 
							raise LookupError("""\
The Karakas (2010), MNRAS, 403, 1413 study did not report yields for elements \
heavier than nickel. Please modify the attribute 'elements' to exclude these \
elements from the simulation (or adopt an alternate yield model) before \
proceeding.""") 		
						else: 
							self._frame[key.lower()] = value.lower() 
					else: 
						raise ValueError("""Unrecognized AGB star yield \
study: %s""" % (value)) 

				elif callable(value): 
					# Callable function -> store a copy of it if it passes 
					try: 
						# Try calling it at a typical mass and metallicity
						x = value(3, 0.01) 
					except: 
						raise TypeError("""AGB star yield settings, when \
callable, must accept two numerical parameters rather than one. The first \
argument is interpreted as the stellar mass in Msun and the second as the \
metallicity by mass Z.""") 
					if isinstance(x, numbers.Number): 
						self._frame[key.lower()] = value 
					else: 
						raise TypeError("""AGB star yield settings, when \
callable, must return a numerical value.""") 
				else: 
					raise TypeError("""Functional AGB star yield settings \
must be either a callable function accepting two numerical parameters or a 
string denoting an AGB star yield study.""") 
			else: 
				raise ValueError("Unrecognized element: %s" % (key)) 
		else: 
			raise TypeError("Dataframe key must be of type str. Got: %s" % (
				type(key))) 

