
# Python Functions
from __future__ import print_function, division, unicode_literals
from ..data import agb_yield_grid
from ..data import integrated_cc_yield
from _data_management import output
import _globals
import warnings
import numbers
import inspect
import math as m
import sys
import os
try:
	# NumPy compatible but not NumPy dependent
	import numpy as _np
except:
	pass
try:
	# Pandas compatible but not Pandas dependent
	import pandas as _pd
except:
	pass
if sys.version_info[0] == 3:
	from builtins import str, range, bytes
else:
	pass

# C Functions
cimport cython
from libc.stdlib cimport malloc, free
from ctypes import *
clib = pydll.LoadLibrary("%score/enrichment.so" % (_globals.DIRECTORY))

__all__ = ["integrator"]

# This should always be caught at import anyway
def __version_error():
	message = "Only Python versions 2.6, 2.7, and >= 3.3 are "
	message += "supported by VICE."
	raise SystemError(message)


class integrator(object):

	"""
	CLASS: integrator
	=================
	This class runs numerical integrations of one-zone chemical evolution 
	models according to user specified parameters. Default parameters are 
	set according to a constant infall rate into a system of initially clean 
	gas with fiducial parameters that yield near-solar abundances for each 
	element by the end of the integration. 

	See docstrings for individual parameters on how to initialize them 
	according to your preferences as well as more details on the role they 
	play in the integration.


	User-specified Attributes:
	==========================
	name:				The name of the model being run. 
	func:				A built-in default function that always return 9.1
	mode:				The physical value being specified by func
	elements:			The symbols of the elements to track in the integration 
	imf:				The initial mass function
	schmidt:			A boolean describing whether or not to use an 
					implementation of gas-mass dependent 
					star formation efficiency 
	eta:				The mass loading factor
	enhancement: 			The ratio of outflow metallicity to ISM metallicity
	Zin: 				The inflow metallicity
	recycling:			The instantaneous recycling parameter
	bins:				The bins in [X/Y] to sort the final stellar metallicity 
					distribution function into
	delay:				The minimum delay time of SNe Ia in Gyr.
	dtd:				The delay time distribution (DTD) of SNe Ia
	Mg0:				The initial gas mass of the system
	smoothing:			The mass loading factor smoothing timescale in Gyr
	tau_ia:				The e-folding timescale of SNe Ia
					(only relevant for exponential SNe Ia DTD models)
	tau_star:			The depletion timescale in Gyr
	dt:				The size of timesteps in Gyr
	schmidt_index:			The power-law index on gas-mass dependent SFE
	MgSchmidt:			The normalization factor on gas-mass dependent SFE
	m_upper:			Upper mass limit on star formation in Msun
	m_lower:			Lower mass limit on star formation in Msun
	Z_solar:			The value to adopt for solar metallicity by mass Z
	rotating_ccsne:			Whether or not to adopt the Chieffie & Limongi (2013) 
					rotating CCSNe yields or nonrotating. Default yields 
					are those used in Johnson & Weinberg (2018, in prep). 
	auto_recalc:			Whether or not to auto-recalculate and set the 
					CCSNe yields from the current parameter settings. 



	Built-in Attributes:
	====================
	recognized_elements:		The elements that this software is built to 
					model the enrichment for
	recognized_imfs:		The stellar initial mass functions that this 
					software has built in



	Functions:
	==========
	settings:				Prints the current model parameters
	run:					Runs the integration functions on the parameters
	recalculate_cc_yields: 			Recalculates the CCSNe yields from current 
						settings of an instance of an integrator object. 



	While the attribute func must be a function of time in Gyr, the user has 
	the option to do the same with attributes eta, enhancement, Zin 
	(which can also contain different functions for each element), dtd, 
	and tau_star. If the user passes a numerical value for these parameters, 
	then it will be that numerical value at all times in the integration. 
	However, in the event that the user initializes one of these attributes 
	as a callable python function, then this software will let that parameter 
	take on the value the function returns at all times during the 
	integration. This allows the user to specify models of mass loading 
	factors, outflow enhancement factors, inflow metallicity, and 
	star formation efficiency that are time-dependent with arbitrary degrees 
	of complexity. The user may also specify an entirely customized SNe Ia 
	delay-time distribution (DTD). The full flexibility of each of these 
	parameters can be also be used simultaneously. 



	USERS' WARNING REGARDING PASSING FUNCTIONS AS ATTRIBUTES:
	=========================================================
	As noted above, two attributes of this class can be set to callable 
	functions of time (eta and tau_star). The attribute func, by default, 
	is required to be one. 

	The functions that these parameters take must be pure python functions. 
	That is, a Type Error will be raised in the event that it receives a 
	built-in funciton. That also includes any and all functions whose original 
	source code is implemented in a language other than Python, such as many 
	NumPy mathematical functions as well as Python code that has been ran 
	through a Cython compiler. 

	However, to implement an attribute involving any of these functions, 
	the user simply needs to wrap them in a python function. For example, the 
	following will produce a Type Error:

	>>> import vice
	>>> import numpy as np
	>>> i = vice.integrator(func = np.exp)

	If the user desires NumPy's exp function to be passed as the func 
	attribute, then this can be implemented in the following manner:

	>>> import vice
	>>> import numpy as np
	>>> def f(t):
	>>>     return np.exp(t)
	>>> i = vice.integrator(func = f)

	This sort of wrapping can also be done in a single line at the time of 
	initialization using a <lambda>:

	>>> import vice
	>>> import numpy as np
	>>> i = vice.integrator(func = lambda t: np.exp(t))

	See docstrings for individual attributes for more direction on how to 
	specify these parameters according to your model. 


	USERS' WARNING ON EMULATING DELTA FUNCTIONS IN ATTRIBUTES:
	==========================================================
	Here we detail a simple warning on emulating delta function in attributes. 
	VICE is a timestep-style integrator, and therefore, these can be 
	achieved by letting a quantity take on some very high value for one 
	timestep. If the user wishes to build a delta function into their model, 
	they need to make sure that: 

	1) They let their delta function have an intrinsic finite width of at 
	   least one timestep. Otherwise, it is not guaranteed that the numerical 
	   integrator will find the delta function. 

	2) They have set their output times such that the integrator will write 
	   to the output file at the time of the delta function. If this is not 
	   ensured, the output will still show the behavior induced by the delta 
	   function, but not in the parameter which was meant to exhibit one. 

	Delta functions of any kind tend to make any physical system behave 
	eradically for a brief period. Thus we recommend that when you employ a 
	delta function, you set your integration to write output at every timestep 
	following the delta function for a brief time interval. This merely 
	ensures that the output and subsequent plots will show the full behavior 
	of the integration. Otherwise the output may show breaks and 
	discontinuities where there are none when finer output time intervals are 
	used. 

	For the purpose of minimizing disk-space usage while still maintaining 
	high time-step resolution, VICE does not require that output be written 
	to disk at every timestep. See docstring of integrator.run for 
	instructions on how to specify your output times.
	"""

	def __init__(self, name = "onezonemodel", 
		func = _globals._DEFAULT_FUNC, 
		mode = "ifr", 
		elements = ["fe", "o", "sr"], 
		imf = "kroupa", 
		schmidt = False, 
		eta = 2.5, 
		enhancement = 1, 
		Zin = 0, 
		recycling = "continuous", 
		bins = _globals._DEFAULT_BINS(),
		delay = 0.15, 
		dtd = "plaw", 
		Mg0 = 6.0e9, 
		smoothing = 0., 
		tau_ia = 1.5, 
		tau_star = 2., 
		dt = 0.001, 
		schmidt_index = 0.5, 
		MgSchmidt = 6.0e9, 
		m_upper = 100, 
		m_lower = 0.08, 
		Z_solar = 0.014, 
		rotating_ccsne = True, 
		auto_recalc = False):

		"""
		Kwargs, Defaults, and Units:
		============================
		name 		= "onezonemodel"
		func 		= def f(t): return 9.1 [mode-dependent]
		elements 	= ["fe", "o", "sr"]
		mode 		= "ifr"  
		eta  		= 2.5 
		enhancement 	= 2.5 
		Zin		= 0
		recycling 	= "continuous"
		bins 		= [-3, -2.99, -2.98, ... , 0.98, 0.99, 1]
		delay		= 0.15 [Gyr]
		dtd 		= "plaw"
		Mg0		= 6.0e9 [Msun]
		smoothing 	= 0.0 [Gyr]
		tau_Ia		= 1.5 [Gyr]
		tau_star 	= 2.0 [Gyr]
		dt 		= .001 [Gyr]
		m_upper 	= 100 [M_sun]
		m_lower 	= 0.08 [M_sun]
		Z_solar 	= 0.014 
		"""

		# The integration and model structs from the C-wrapping
		# User access of these parameters is strongly discouraged
		self.__model = __model_struct()
		self.__run = __integration_struct()

		# Call the setter methods for each attribute for type-checking
		self._auto_recalc = False
		self.name = name
		self.func = func
		self.mode = mode
		self.elements = elements
		self.imf = imf
		self.eta = eta
		self.enhancement = enhancement
		self.Zin = Zin
		self.recycling = recycling
		self.bins = bins
		self.delay = delay
		self.dtd = dtd
		self.Mg0 = Mg0
		self.smoothing = smoothing
		self.tau_Ia = tau_ia
		self.tau_star = tau_star
		self.schmidt = schmidt
		self.schmidt_index = schmidt_index 
		self.MgSchmidt = MgSchmidt
		self.dt = dt
		self.m_upper = m_upper
		self.m_lower = m_lower
		self.Z_solar = Z_solar
		self.rotating_ccsne = rotating_ccsne
		self.auto_recalc = auto_recalc
		if self._auto_recalc:
			if any(list(map(lambda x: x in kwargs, 
				["imf", "m_upper", "m_lower", "rotating_ccsne"]))):
				self.recalculate_yields()
			else:
				pass
		else:
			pass

	@property
	def recognized_elements(self):
		"""
		The symbols of the elements whose enrichment properties are built into 
		this software. The user can specify which elements are tracked in 
		each integration via the 'elements' attribute.
		"""
		return _globals.RECOGNIZED_ELEMENTS

	@property
	def recognized_imfs(self):
		"""
		The initial mass functions (IMFs) that are built into this software. 
		The user can specify which one to use via the attribute 'imf'.
		"""
		return _globals.RECOGNIZED_IMFS

	@property
	def name(self):
		"""
		The name of the model being run. The output of the 
		integration will be placed in a file in the user's 
		current working directory under the same name. To place the 
		output file under a different directory, then this 
		parameter should be initialized as the full path to the 
		desired output file. For example:

		>>> example = vice.integrator()
		>>> example.name = "onezonemodel"
				
		The above will create an output file under the name 
		onezonemodel in your current working directory at the time of 
		integration. 

		>>> example = vice.integrator()
		>>> example.name = "/path/to/output/directory/onezonemodel"

		The above, however, will create a folder named onezonemodel in 
		the directory /path/to/output/directory/ at the time of 
		integration and the output will be stored there. 

		It does not matter whether or not the user places a '/' at the end of 
		the name; this possibility is taken into account.
		"""
		return self._name

	@name.setter
	def name(self, value):
		throw = False
		# Python 2.x string treatment
		if sys.version_info[0] == 2:
			if isinstance(value, basestring):
				self._name = value
				while self._name[-1] == '/':
					self._name = self._name[:-1]
			else:
				throw = True
		# Python 3.x string treatment
		elif sys.version_info[0] == 3:
			if isinstance(value, str):
				self._name = value
				while self._name[-1] == '/':
					self._name = self._name[:-1]
			else:
				throw = True
		else:
			# This should be caught at import anyway
			__version_error()

		#Type Error
		if throw:
			message = "Attribute name must be of type string. Got: %s" % (
				type(value))
			raise TypeError(message)
		else:
			pass

	@property
	def func(self):
		"""
		The specified function of time. This can represent either the 
		infall rate in Msun/yr, the star formation rate in Msun/yr, or the gas 
		mass in Msun. The specification between these is set by the 
		attribute 'mode'. Note that the parameter this function takes will 
		always be interpreted as time in Gyr. 

		See class docstring for users' note on setting functions as attribute 
		values.

		Example: An exponentially declining infall rate with an e-folding 
		timescale of 6 Gyr:

		>>> import vice
		>>> import numpy as np
		>>> def f(t):
		>>>     return 9.1 * np.exp( -t / 6 )
		>>> i = vice.integrator(mode = "ifr", func = f)

		Example: An exponentially declining infall rate with an e-folding 
		timescale of 6 Gyr, but very little gas at the start of integration, 
		emulating a linear-exponential gas history:

		>>> import vice
		>>> import numpy as np
		>>> def f(t):
		>>>     return 9.1 * np.exp( -t / 6 )
		# Specify only 1 solar mass of gas at the first timestep
		>>> i = vice.integrator(mode = "ifr", func = f, Mg0 = 1)

		Example: The previous history, but with attributes initialized in 
		different steps rather than in one line:

		>>> import vice
		>>> import numpy as np
		>>> def f(t):
		>>>     return 9.1 * np.exp( -t / 6 )
		>>> i = vice.integrator()
		>>> i.mode = "ifr"
		>>> i.func = f
		>>> i.Mg0 = 1

		See docstring of attribute 'mode' for more details.
		"""
		return self._func

	@func.setter
	def func(self, value):
		if callable(value):
			if self.__args(value):
				message = "Attribute 'func' must be a callable function that "
				message += "takes only one parameter with no variable, "
				message += "keyword, or default arguments."
				raise ValueError(message)
			else:
				self._func = value
		else:
			message = "Attribute 'func' must be a callable function that "
			message += "takes only one parameter with no variable, "
			message += "keyword, or default arguments."
			raise TypeError(message)

	@property
	def mode(self):
		"""
		The specification of the attribute 'func' (as a string). This parameter 
		is case-insensitive and will always be converted to a lower-case string. 
		There are three possible values:

		mode = "ifr":
		=============
		Attribute func is a callable function of time, where the argument is 
		given in Gyr. It then returns the rate of gas infall into the galaxy 
		in Msun/yr at that time.

		mode = "sfr":
		=============
		Attribute func is a callabe function of time, where the arguement is 
		given in Gyr. It then returns a star formation rate in Msun/yr at that 
		time. 

		mode = "gas":
		=============
		Attribute func is a callable function of time, where the argument is 
		given in Gyr. It then returns a gas mass in Msun at that time. 

		Note the differences in units - the time is specified in Gyr, while the 
		infall and star formation rates are always specified in Msun/yr 
		according to convention. 

		Note also that the integration will always start at time = 0.
		"""
		return self._mode

	@mode.setter
	def mode(self, value):
		throw = False
		# Python 2.x string treatment
		if sys.version_info[0] == 2:
			if isinstance(value, basestring):
				if value.lower() in ["ifr", "sfr", "gas"]:
					self._mode = value.lower()
					self.__run.mode = value.lower().encode("latin-1")
				else:
					message = "Unrecognized mode: %s" % (value)
					raise ValueError(message)
			else:
				throw = True
		# Python 3.x string treatment
		elif sys.version_info[0] == 3:
			if isinstance(value, str):
				if value.lower() in ["ifr", "sfr", "gas"]:
					self._mode = value.lower()
					self.__run.mode = value.lower().encode("latin-1")
				else:
					message = "Unrecognized mode: %s" % (value)
					raise ValueError(message)
			else:
				throw = True
		else:
			# This should be caught at import anyway
			__version_error()

		# TypeError
		if throw:
			message = "Attribute name must be of type string. Got: %s" % (
				type(value))
			raise TypeError(message)
		else:
			pass

	@property
	def elements(self):
		"""
		The elements that are to be modeled while the integration is running. 
		They're encoded as their one- or two-letter symbols (case-insensitive). 
		This attribute accepts array-like objects and stores them in a python 
		tuple. 
		"""
		return self._elements

	@elements.setter
	def elements(self, value):
		if "numpy" in sys.modules and isinstance(value, _np.ndarray):
			copy = value.tolist()
		elif "pandas" in sys.modules and isinstance(value, _pd.DataFrame):
			copy = [i[0] for i in value.values.tolist()]
		elif type(value) in [list, tuple]:
			copy = value[:]
		else:
			message = "Attribute 'elements' must be either a NumPy array, "
			message += "Pandas DataFrame, python list, or python tuple. "
			raise TypeError(message)

		for i in copy:
			if i.lower() not in _globals.RECOGNIZED_ELEMENTS: 
				message = "Unrecognized element: %s" % (i)
				raise ValueError(message)
			else:
				continue
		self._elements = tuple(copy[:])

	@property
	def Mg0(self):
		"""
		The gas mass in Msun at time = 0, when the integration will start. 

		Note that this parameter is only relevant in infall mode. When in 
		gas mode, the initial gas supply will simply be taken as self.func(0), 
		and in sfr mode, the initial gas supply is taken from the star 
		formation rate at time 0 times the depletion time at time 0.
		"""
		return self._Mg0

	@Mg0.setter
	def Mg0(self, value):
		if isinstance(value, numbers.Number):
			if value > 0: 
				self._Mg0 = float(value)
				self.__run.MG = float(value)
			elif value == 0:
				self._Mg0 = 1.e-12
				self.__run.MG = 1.e-12
			else:
				message = "Initial gas supply must be a positive float."
				raise ValueError(message)
		else:
			message = "Attribute 'Mg0' must be a numerical value. Got: %s" % (
				type(value))
			raise TypeError(message)

	@property
	def imf(self):
		"""
		The initial mass function (IMF) to use in the model as a string. This 
		parameter is case-insensitive and will always be converted to a 
		lower-case string.

		Note that this software currently only recognizes Salpeter and 
		Kroupa IMFs. 
		"""
		return self._imf

	@imf.setter
	def imf(self, value):
		throw = False
		# Python 2.x string treatment
		if sys.version_info[0] == 2:
			if isinstance(value, basestring):
				if value.lower() in _globals.RECOGNIZED_IMFS:
					if self._auto_recalc: self.recalculate_cc_yields()
					self._imf = value.lower()
					self.__model.imf = value.lower().encode("latin-1")
				else:
					raise ValueError("Unrecognized IMF: %s" % (value))
			else:
				throw = True
		# Python 3.x string treatment
		elif sys.version_info[0] == 3:
			if isinstance(value, str):
				if value.lower() in _globals.RECOGNIZED_IMFS:
					if self._auto_recalc: self.recalculate_cc_yields()
					self._imf = value.lower()
					self.__model.imf = value.lower().encode("latin-1")
				else:
					raise ValueError("Unrecognized IMF: %s" % (value))
			else:
				throw = True
		else:
			# This should be caught at import anyway
			__version_error()

		# TypeError
		if throw:
			message = "Attribute imf must be of type string. Got: %s" % (
				type(value))
			raise TypeError(message)
		else:
			pass

	@property
	def eta(self):
		"""
		The unitless mass loading factor (eta = outflow rate / star formation 
		rate). This can either be a single numerical value or a callable 
		function of time in Gyr.

		Users' Note Regarding Smoothing Timescales:
		===========================================
		In the case of a callable function of time with a nonzero smoothing 
		time, note that at all timesteps the instantaneous value of eta is used 
		to determine the outflow rate. That is, it is ONLY the star formation 
		rate that is smoothed over the specified timescale, not the mass 
		loading factor.

		See docstring to attribute smoothing for more details on smoothing 
		timescales.

		See class docstring for Users' warning on specifying functions as 
		attribute values. 
		"""
		return self._eta

	@eta.setter
	def eta(self, value):
		if callable(value):
			if self.__args(value):
				message = "Attribute 'eta', when callable, must take only one "
				message += "parameter and no keyword/variable/default "
				message += "parameters."
				raise ValueError(message)
			else:
				self._eta = value
		elif isinstance(value, numbers.Number):
			self._eta = float(value)
		else:
			message = "Attribute 'eta' must be either a callable python "
			message += "function or a numerical value. Got: %s" % (
				type(value))
			raise TypeError(message)

	@property
	def enhancement(self):
		"""
		The outflow enhancement factor xi_{enh} = Z_{out} / Z_{gas}, 
		the ratio of the outflow metallicity to the gas metallicity

		This value may be either a single numerical value or a callable 
		function of time. It's value will be the same for all elements in 
		the integration. 
		"""
		return self._enhancement

	@enhancement.setter
	def enhancement(self, value):
		if callable(value):
			if self.__args(value):
				message = "Attribute 'enhancement', when callable, must take "
				message += "only one parameter and no keyword/variable/default "
				message += "parameters."
				raise ValueError(message)
			else:
				self._enhancement = value
		elif isinstance(value, numbers.Number):
			if self._enhancement >= 0:
				self._enhancement = float(value)
			else:
				message = "Attribute enhancement must be non-negative." 
				raise ValueError(message)
		else:
			message = "Attribute 'enhancement' must be either a callable "
			message += "python function or a numerical value."
			raise TypeError(message)

	@property
	def Zin(self):
		"""
		The inflow metallicity Z_x = M_x / M_infall

		This parameter can be either a numerical value, a list of numerical 
		values, a callable function of time, or a list of callable functions 
		of time. In the case of lists or other array like objects like 
		NumPy arrays, it will immediately be converted into a dictionary 
		keyed on by the element abbreviation in lower case (e.g. 'fe' for 
		iron), and will be treated component-wise with the attribute 
		'elements' to assign the individual infall metallicities to each 
		element. 

		When this attribute is a dictionary, it's elements may also be 
		modified as such. For example, the following will implement solar 
		iron infall at all times and a linearly increasing oxygen infall 
		metallicity that reaches solar at 10 Gyr: 

		>>> import vice
		>>> example = vice.integrator()
		>>> example.Zin = len(example.elements) * [0.]
		>>> example.Zin
		{"fe": 0.0, "o": 0.0, "sr": 0.0}
		>>> example.Zin["fe"] = vice.solar_z["fe"]
		>>> example.Zin["o"] = lambda t: vice.solar_z["o"] * (t / 10.0)
		>>> example.Zin
		{"fe": 0.0012, "o": <function <lambda> at XXXXXXX>, "sr": 0.0}

		Note that keying this attribute as a dictionary is case-sensitive and 
		must be done with lower-case strings, as illustrated in the sample. 
		"""
		return self._Zin

	@Zin.setter
	def Zin(self, value):
		is_array = False
		if isinstance(value, numbers.Number):
			self._Zin = float(value)
		elif callable(value):
			if self.__args(value):
				message = "Attribute 'Zin', when callable, must take only one "
				message += "parameter and no keyword/variable/default "
				message += "parameters."
				raise ValueError(message)
			else:
				self._Zin = value
		# Array treatment of Zin from here on out
		elif "numpy" in sys.modules and isinstance(value, _np.ndarray):
			copy = value.tolist()
			is_array = True
		elif "pandas" in sys.modules and isinstance(value, _pd.DataFrame):
			copy = [i[0] for i in value.values.tolist()]
			is_array = True
		elif isinstance(value, list):
			copy = value[:]
			is_array = True
		else:
			message = "Attribute Zin must be either a callable function of "
			message += "time, a numerical value, or a list of any combination "
			message += "of the two. "
			raise TypeError(message)

		if is_array:
			if len(value) != len(self._elements):
				message = "Attribute 'Zin', when initialized as an array, "
				message += "must have one entry for each element. Please "
				message += "modify the attribute 'elements' first if you "
				message += "wish to add or remove elements from the " 
				message += "integration. "
				raise ValueError(message)
			else:
				pass
			dummy = len(value) * [None]
			for i in range(len(dummy)):
				if isinstance(value[i], numbers.Number):
					dummy[i] = float(value[i])
				elif callable(value[i]):
					if self.__args(value[i]):
						message = "Attribute 'Zin', when passed as an array "
						message += "containing callable functions of time, "
						message += "must contain functions which each take "
						message += "exactly one parameter with no keyword/"
						message += "variable/default arguments." 
						raise ValueError(message)
					else:
						dummy[i] = value[i]
				else:
					message = "Attribute 'Zin', when passed as an array, "
					message += "must contain only numerical values and " 
					message += "functions of time as array elements. Error "
					message += "found at index %d. Got %s" % (i, 
						type(value[i]))
					raise TypeError(message)
			self._Zin = dict(zip(self._elements, dummy))
		else:
			pass

	@property
	def recycling(self):
		"""
		The recycling specification. This represents the cumulative return 
		fraction following a single episode of star formation (i.e. the 
		mass fraction that is returned to the ISM from stars). 

		If a numerical value is specified, this will be treated as the an 
		instantaneous return fraction. For example, if recycling = 0.4, then 
		at all timesteps, the integrator will return 40% of all mass that 
		goes into star formation back to the ISM at that timestep. 

		Otherwise, the user may specify the string "continuous" (case-
		insensitive) and the integrator will use a more sophisticated time-
		dependent formulation of the cumulative return fraction given the 
		initial mass function and the mass in stellar remnants following a 
		single episode of star formation. 

		See appendix A2 and figure A1 of Johnson & Weinberg (2018, in prep) 
		for details.
		"""
		return self._recycling

	@recycling.setter
	def recycling(self, value):
		if isinstance(value, numbers.Number):
			if 0 <= value <= 1:
				self._recycling = float(value)
				self.__model.R0 = value
				self.__model.continuous = 0
			else:
				message = "The cumulative return fraction must be between "
				message += "0 and 1 to be physical."
				raise ValueError(message)
		elif isinstance(value, str):
			if value.lower() == "continuous":
				self._recycling = value.lower()
				self.__model.R0 = 0
				self.__model.continuous = 1
			else:
				message = "If attribute 'recycling' is to be a string, it must "
				message += "be 'continuous' (case-insensitive). "
				message += "Got: %s" % (value)
				raise ValueError(message)
		# Python 3.x will always evaluate to False before reaching basestring
		elif sys.version_info[0] == 2 and isinstance(value, basestring):
			if value.lower() == "continuous":
				self._recycling = value.lower()
				self.__model.R0 = 0
				self.__model.continuous = 1
			else:
				message = "If attribute 'recycling' is to be a string, it must "
				message += "be 'continuous' (case-insensitive). "
				message += "Got: %s" % (value)
				raise ValueError(message)
		else:
			message = "Attribute recycling must be either a numerical value "
			message += "between 0 and 1 or the string 'continuous' (case-"
			message += "insensitive)."
			raise TypeError(message)

	@property
	def delay(self):
		"""
		The minimum time-delay in Gyr of SNe Ia following the formation of a 
		single stellar population. That is, following any given episode of 
		star formation, SNe Ia enrichment of any element will not set in until 
		this much time has passed in the simulation.
		"""
		return self._delay

	@delay.setter
	def delay(self, value):
		if isinstance(value, numbers.Number):
			if value >= 0: 
				self._delay = value 
				self.__model.t_d = value
			else:
				message = "Attribute 'delay' must be a positive value."
				raise ValueError(message)
		else:
			message = "Attribute 'delay' must be a positive numerical value. "
			message += "Got: %s" % (type(value))
			raise TypeError(message)

	@property
	def tau_Ia(self):
		"""
		The e-folding timescale of SNe Ia in Gyr. This attribute is only 
		relevant if the delay-time distribution (attribute dtd) is set to 
		"exp", in which case, the SNe Ia rate goes as exp( -t / tau_Ia ).

		If a power law DTD is used (i.e. if self.dtd == "plaw"), or if the 
		user specifies their own custom DTD, then this parameter plays no role 
		in the integration.
		"""
		return self._tau_Ia

	@tau_Ia.setter
	def tau_Ia(self, value):
		if isinstance(value, numbers.Number):
			if value > 0: 
				self._tau_Ia = value
				self.__model.tau_ia = value
			else:
				message = "Attribute 'tau_Ia' must be a positive value. "
				raise ValueError(message)
		else:
			message = "Attribute 'tau_Ia' must be a positive numerical value." 
			message += "Got: %s" % (type(value))
			raise TypeError(message)

	@property
	def tau_star(self):
		"""
		The depletion timescale tau_star in Gyr (also the inverse of the 
		star formation efficiency). In all modes, this is the value relating 
		the gas mass to the star-formation rate: 

		tau_star = M_gas / SFR

		This parameter may be a simple numerical value or a callable function 
		of time. See class docstring for Users' warning on specifying functions 
		as attribute values.

		When the attribute 'schmidt' = True, this parameter is used as the 
		normalization on Schmidt-Law star formation efficiency, whereby the 
		SFE is proportional to the gas supply. That is: 

		SFE = tau_star(t)^-1 * (Mgas / MgSchmidt)^(schmidt_index)
		"""
		return self._tau_star

	@tau_star.setter
	def tau_star(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				self._tau_star = float(value)
			else:
				message = "Attribute 'tau_star' must be positive value. "
				raise ValueError(message)
		elif callable(value):
			if self.__args(value):
				message = "When callable, attribute 'tau_star' must take only "
				message += "one parameter and no keyword/variable/default "
				message += "arguments."
				raise ValueError(message)
			else:
				self._tau_star = value
		else:
			message = "Attribute 'tau_star' must be either a numerical value "
			message += "or a callable function taking one parameter."
			raise TypeError(message)

	@property
	def schmidt(self):
		"""
		A boolean describing whether or not to use and implementation of 
		Schmidt-law efficiency, whereby the star-formation efficiency is 
		proportional to the gas supply. The specifics of this behavior are 
		specified by the attributes 'tau_star', 'schmidt_index', and 
		'MgSchmidt'.
		"""
		return self._schmidt

	@schmidt.setter
	def schmidt(self, value):
		if isinstance(value, numbers.Number):
			if value:
				self._schmidt = True
				self.__model.schmidt = 1
			else:
				self._schmidt = False
				self.__model.schmidt = 0
		if isinstance(value, bool):
			self._schmidt = value
			if value:
				self.__model.schmidt = 1
			else:
				self.__model.schmidt = 0
		else:
			message = "Attribute 'schmidt' must be interpretable as a "
			message += "boolean. Got: %s" % (type(value))
			raise TypeError(message)

	@property
	def schmidt_index(self):
		"""
		The power-law index for the depletion time derived from a schmidt-law 
		star formation efficiency:

		SFE = tau_star(t)^-1 * (Mgas / MgSchmidt)**(schmidt_index)
		"""
		return self._schmidt_index

	@schmidt_index.setter
	def schmidt_index(self, value):
		if isinstance(value, numbers.Number):
			self._schmidt_index = value
			self.__model.schmidt_index = value
		else:
			message = "Attribute 'schmidt_index' must be a numerical value."
			raise TypeError(message)
		if self._schmidt_index < 0:
			message = "Attribute 'schmidt_index' is now a negative value. "
			message += "This may introduce numerical artifacts. "
			warnings.warn(message, UserWarning)

	@property
	def MgSchmidt(self):
		"""
		The normalization on the Schmidt-Law: 

		SFE \\propto (Mgas / MgSchmidt)**(schmidt_index)

		In practice, this should be some fiducial gas mass. In that case, the 
		star-formation efficiency is close to what the user specifies as the 
		normalization constant tau_star(t).
		"""
		return self._MgSchmidt

	@MgSchmidt.setter
	def MgSchmidt(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				self._MgSchmidt = value
				self.__model.mgschmidt = value
			else:
				message = "Attribute 'MgSchmidt' must be a positive definite "
				message += "value."
				raise ValueError(message)
		else:
			message = "Attribute 'MgSchmidt' must be a numerical value."
			raise TypeError(message)

	@property
	def dtd(self):
		"""
		The SNe Ia delay-time distribution (DTD). There are two built-in 
		DTDs that VICE will automatically treat, and to use one of these 
		this attribute must be set to a particular string. 

		"exp": An exponential DTD with e-folding timescale set by the 
		attribute 'tau_Ia'

		"plaw": A power-law dtd proportional to t^-1.1

		In addition to these built-in DTDs, the user also has the option to 
		pass their own function of time. Like all other attributes that 
		accept functions as parameters in VICE, it must take only one 
		parameter and no keyword/default/variable arguments. It will be 
		interpreted as the rate R as a function of time in Gyr. 

		The user need not worry about the normalization of their DTD. Prior 
		to the integration, VICE will integrate the DTD up to 12.5 Gyr and 
		normalize it automatically. Therefore, the user also need not worry 
		about how long their integrations run - the DTD will always be 
		treated the same. 
		"""
		return self._dtd

	@dtd.setter
	def dtd(self, value):
		if callable(value):
			if self.__args(value):
				message = "When callable, attribute 'dtd' must take only "
				message += "one parameter and no keyword/variable/default "
				message += "parameters."
				raise ValueError(message)
			else:
				self._dtd = value
				self.__model.dtd = "custom".encode("latin-1")
		# Python 3.x string treatment
		elif sys.version_info[0] == 3 and isinstance(value, str):
			if value.lower() in ["exp", "plaw"]:
				self._dtd = value.lower()
				self.__model.dtd = value.lower().encode("latin-1")
			else:
				raise ValueError("Unrecognized SNe Ia DTD: %s" % (value))
		# Python 2.x string treatment
		elif sys.version_info[0] == 2 and isinstance(value, basestring):
			if value.lower() in ["exp", "plaw"]:
				self._dtd = value.lower()
				self.__model.dtd = value.lower().encode("latin-1")
			else:
				raise ValueError("Unrecgonized SNe Ia DTD: %s" % (value))
		else:
			message = "Attribute dtd must be either a callable function, "
			message += "the string \"exp\", or the string \"plaw\"."
			raise TypeError(message)

	@property
	def smoothing(self):
		"""
		The smoothing timescale in Gyr. This is the timescale on which the 
		star-formation rate is averaged to determine the outflow rate. That is, 
		at all timesteps: 

		outflow rate = eta * <star formation rate>_(smoothing)

		where the average is over the previous timesteps leading up to the 
		current timestep. In the cases where the current time is less than the 
		smoothing time, which is inevitable at early times during integration, 
		the average is truncated at t = 0 to avoid numerical errors.

		If the user wishes to not have any smoothing time, it can be set to some 
		dummy value - a negative value, zero, or some value smaller than the 
		timestep will all achieve this effect.

		See appendix A2 of Johnson & Weinberg (2018, in prep) for more details 
		on smoothing timescales.
		"""
		return self._smoothing

	@smoothing.setter
	def smoothing(self, value):
		if isinstance(value, numbers.Number):
			if value >= 0:
				self._smoothing = value
				self.__model.smoothing_time = value
			else:
				message = "Attribute 'smoothing' must be non-negative."
				raise ValueError(message)
		else:
			message = "Attribute 'smoothing' must be a numerical value."
			raise TypeError(message)

	@property
	def bins(self):
		"""
		The bins within which the stellar metallicity distribution function will 
		be determined. This value must be an array-like object of numerical 
		values. NumPy and Pandas arrays are supported, but this software is not 
		dependent on them. 

		Note: Calling this attribute returns a python list object. The actual 
		attribute, however, is stored in an array of C doubles.
		"""
		# clib.set_mdf_bins(byref(self.__model))
		return [self.__model.bins[i] for i in list(range(
			self.__model.num_bins + 1l))]

	@bins.setter
	def bins(self, value):
		# Python 3.x will evaluate to True before reacing basestring and 
		# throwing an error so no extra lines necessary here 
		if isinstance(value, str) or isinstance(value, basestring):
			message = "Attribute 'bins' must be an array-like object of "
			message += "numerical values."
			raise TypeError(message)
		else:
			try:
				copy = value[:]
			except TypeError:
				message = "Attribute 'bins' must be an array-like object of "
				message = "numerical values."
				raise TypeError(message)

		if "numpy" in sys.modules and isinstance(value, _np.ndarray):
			copy = value.tolist()
		elif "pandas" in sys.modules and isinstance(value, _pd.DataFrame):
			copy = [i[0] for i in value.values.tolist()]
		else:
			pass

		if all(list(map(lambda x: isinstance(x, numbers.Number), copy))):
			copy = [float(i) for i in copy]
			copy = sorted(copy) # sort from least to greatest
		else:
			message = "Attribute 'bins' must be an array-like object of "
			message += "numerical values. If yo've passed a NumPy or Pandas "
			message += "array, ensure that it is 1-dimensional.\n"
			message += "Got: ", value
			raise TypeError(message)

		ptr = c_double * len(copy)
		self.__model.bins = ptr(*list(copy[:]))
		self.__model.num_bins = len(value) - 1l

	@property
	def dt(self):
		"""
		The time difference in Gyr to use in the integration.
		"""
		return self._dt

	@dt.setter
	def dt(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				self._dt = value
				self.__run.dt = value
			else:
				message = "Attribute 'dt' must be positive definite."
				raise ValueError(message)
		else:
			message = "Attribute 'dt' must be a numerical value."
			raise TypeError(message)

	@property
	def m_upper(self):
		"""
		The upper mass limit on star formation in solar masses. 

		Modifying this attribute will automatically recalculate the yields 
		from core-collapse supernovae off of the built-in grid from 
		Chieffi & Limongi (2013) ApJ, 764, 21 provided that the class 
		attribute 'auto_recalc' is set to True. 

		Users' Warning: 
		===============
		Mass yields for core collapse supernovae are only sampled up to 
		120 Msun. We therefore recommend the user not implement upper mass 
		limits above 120 as it may introduce numerical artifacts. 
		"""
		return self._m_upper

	@m_upper.setter
	def m_upper(self, value):
		if isinstance(value, numbers.Number):
			if value > 0: 
				if self._auto_recalc: self.recalculate_cc_yields()
				self._m_upper = float(value)
			else: 
				message = "Attribute m_upper must be positive."
				raise ValueError(message)
			if self._m_upper < 80:
				message = "This a low upper mass limit on star formation. "
				message += "This may introduce numerical artifacts. " 
				message += "Disregard this message if this is intentional."
				warnings.warn(message, UserWarning)
			else:
				pass
		else:
			message = "Attribute m_upper must be a numerical value. Got: %s" % (
				type(value))
			raise TypeError(message)

	@property
	def m_lower(self):
		"""
		The lower mass limit on star formation in solar masses. 

		Modifying this attribute will automatically recalculate the yields 
		from core-collapse supernovae off of the built-in grid from 
		Chieffi & Limongi (2013) ApJ, 764, 21 provided that the class 
		attribute 'auto_recalc' is set to True. 
		"""
		return self._m_lower

	@m_lower.setter
	def m_lower(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				if self._auto_recalc: self.recalculate_cc_yields()
				self._m_lower = float(value)
			else:
				message = "Attribute m_lower must be positive."
				raise ValueError(message)
			if self._m_lower > 0.2:
				message = "This is a high lower limit on star formation. "
				message += "This may introduce numerical artifacts. "
				message += "Disregard this message if this is intentional."
				warnings.warn(message, UserWarning)
			else:
				pass
		else:
			message = "Attribute m_lower must be a numerical value. Got: %s" % (
				type(value))
			raise TypeError(message)

	@property
	def Z_solar(self):
		"""
		The total solar metallicity Z_sun = M_metals / M_sun to adopt. 

		This parameter only plays a role in scaling the total metallicity 
		of stars for the sake of modelling AGB enrichment. That is, the total 
		metallicity will always be low for integrations that only trace a 
		few elements, and this can introduce numerical artifacts in the 
		enrichment of AGB stars. We therefore employ the following scaling 
		relation: 

		Z = Z_solar * sum(Z_x) / sum(Z_x_solar)

		to estimate the total metallicity at each timestep and therefore 
		mitigate this numerical issue. We nonetheless recommend that if the 
		user is interested in the enrichment of metals from AGB stars, that 
		they include multiple elements in their integration so that the 
		overall metallicity is better determined at each timestep. 
		"""
		return self._Z_solar

	@Z_solar.setter
	def Z_solar(self, value):
		if isinstance(value, numbers.Number):
			if 0 < value < 1:
				self._Z_solar = float(value)
			else: 
				message = "Attribute 'Z_solar' must be between 0 and 1." 
				raise ValueError(message)
			if self._Z_solar > 0.018: 
				message = "VICE implements AGB enrichment up to metallicities "
				message += "of 0.02. We recommend avoiding modeling parameter "
				message += "spaces yielding total metallicities significantly "
				message += "above solar. "
				warnings.warn(message, UserWarning)
			else:
				pass
		else:
			message = "Attribute Z_solar must be a numerical value between 0 "
			message += "an 1. Got: %s" % (type(value))
			raise TypeError(message)

	@property
	def rotating_ccsne(self):
		"""
		A boolean describing whether or not to use a rotating model for CCSNe. 

		Modifying this attribute will automatically recalculate the yields 
		from core-collapse supernovae off of the built-in grid from 
		Chieffi & Limongi (2013) ApJ, 764, 21 provided that the class 
		attribute 'auto_recalc' is set to True. 
		"""
		return self._rotating_ccsne

	@rotating_ccsne.setter
	def rotating_ccsne(self, value):	
		if isinstance(value, numbers.Number):
			if self._auto_recalc: self.recalculate_cc_yields()
			if value:
				self._rotating_ccsne = True
			else:
				self._rotating_ccsne = False
		elif isinstance(value, bool):
			if self._auto_recalc: self.recalculate_cc_yields()
			self._rotating_ccsne = value
		else:
			message = "Attribute 'rotating_ccsne' must be interpretable as "
			message += "a boolean. Got: %s" % (type(value))
			raise TypeError(message) 

	@property
	def auto_recalc(self):
		"""
		A boolean describing whether or not to automatically recalculate 
		CCSNe yields following a respecification of upper/lower mass limit for 
		star formation, IMF, or CCSNe rotating vs. nonrotating model. 
		"""
		return self._auto_recalc

	@auto_recalc.setter
	def auto_recalc(self, value):
		if isinstance(value, numbers.Number):
			if value:
				self._auto_recalc = True
			else:
				self._auto_recalc = False
		elif isinstance(value, bool):
			self._auto_recalc = value
		else:
			message = "Attribute 'auto_recalc' must be interpretable as a " 
			message += "boolean. Got: %s" % (type(value))
			raise TypeError(message) 

		if self._auto_recalc:
			self.recalculate_cc_yields()
		else:
			pass

	def settings(self):
		"""
		Prints the current parameters of the integrator to the screen. 
		"""
		print("Current Parameters:")
		print("===================")
		print("Name: %s" % (self._name))
		print("Func:", self._func)
		print("Mode: %s" % (self._mode))
		print("Elements:", self._elements)
		print("Eta:", self._eta)
		print("Enhancement:", self._enhancement)
		print("Recycling:", self._recycling)
		if len(self.bins) >= 10:
			print("Bins: [%f, %f, %f, ... , %f, %f, %f]" % (self.bins[0], 
				self.bins[1], 
				self.bins[2], 
				self.bins[-3], 
				self.bins[-2], 
				self.bins[-1])
			)
		else:
			print("Bins:", self.bins)
		print("Delay: %g Gyr" % (self._delay))
		print("DTD: %s" % (self._dtd))
		print("Mg0: %e Msun" % (self._Mg0))
		print("Smoothing: %g Gyr" % (self._smoothing))
		print("Tau_Ia: %g Gyr" % (self._tau_Ia))
		if isinstance(self._tau_star, numbers.Number):
			print("Tau_star: %g Gyr" % (self._tau_star))
		else:
			print("Tau_star:", self._tau_star)
		print("Dt: %g Gyr" % (self._dt))
		print("Schmidt: %r" % (self._schmidt))
		print("Schmidt index: %g" % (self._schmidt_index))
		print("MgSchmidt: %e" % (self._MgSchmidt))
		print("Zin:", self._Zin)
		print("M_upper: %g Msun" % (self._m_upper))
		print("M_lower: %g Msun" % (self._m_lower))
		print("Z_solar: %g" % (self._Z_solar))
		print("Rotating CCSNe model: %r" % (self._rotating_ccsne))

	def recalculate_cc_yields(self):
		"""
		Recalculates the core-collapse supernovae yields under the current 
		settings that affect them. 

		Calling this function will modify the values stored in the 
		'ccsne_yields' instance of the _case_insensitive_dataframe implemented 
		in VICE. It will thus affect all subsequent integrations ran by all 
		instances of the integrator class, because this dataframe is 
		package-wide.

		If the class attribute 'auto_recalc' is set to True, modifying any 
		attributes of "imf", "m_upper", "m_lower", or "rotating_ccsne" 
		will automatically call this function. 
		"""
		for i in list(range(len(_globals.RECOGNIZED_ELEMENTS))):
			_globals.ccsne_yields[
				_globals.RECOGNIZED_ELEMENTS[i]] = integrated_cc_yield(
					_globals.RECOGNIZED_ELEMENTS[i], 
					rotating = self._rotating_ccsne, 
					IMF = self.imf, 
					method = "simpson", 
					lower = self._m_lower, 
					upper = self._m_upper, 
					tolerance = 1e-3, 
					Nmin = 64, 
					Nmax = 2e8)

	def run(self, output_times, capture = False, overwrite = False):
		"""
		Runs the integration according to the current values of attributes that 
		the user has specified. Calling this function will always produce two 
		output files:

		self.name/history.out: 	The full-time evolution of the simulation
		self.name/mdf.out:  	The resulting stellar metallicity distribution
					function (MDF) at the final timestep.

		Args:
		=====
		output_times:		An array-like object detailing at what times in the 
					simulation the integrator should write output to the 
					history file. This need not be an array of uniform 
					timesteps, or even in ascending order. The integrator will 
					take care of all of that for you. The only requirement is 
					that all elements be numerical values. 

		Kwargs:
		=======
		capture = False:	Whether or not to return an output object for the 
					results of the integration. See class docstring for 
					type 'output' for details.
		overwrite = False:	Whether or not to force overwrite any files that 
					may be under the same name, perhaps from previous 
					integrations. 

		User's Warning on overwrite:
		============================
		In the event that the user is running many VICE models initialized 
		in their own Python scripts, they will want to pay attention to the 
		names of the models they're running, and to potentially specify 
		overwrite = True. 

		When overwrite = False, and in the event that VICE finds any output 
		files in the user's system under the same name that it is designed 
		to write to, this acts as a halting function. That is, the integrator 
		will stop and wait for the user's input on whether or not to 
		continue and overwrite the existing files. When overwrite = True, 
		VICE interprets this as permission to overwrite any existing files 
		that it finds. If the user is running many integrations with 
		potentially similar names, it is to their advantage to specify 
		overwrite = True so that their integrations do not stall. 
		"""
		if isinstance(self._Zin, dict) and len(self._Zin) != len(
			self._elements):
			message = "Please modify attribute 'Zin' to match the new "
			message += "settings of attribute 'elements'."
			raise AttributeError(message)
		else:
			pass
		output_times = self.__output_times_check(output_times)
		self.__run.MG = self._Mg0
		self.__model.m_upper = self._m_upper
		self.__model.m_lower = self._m_lower
		ptr = c_char_p * len(self._elements)
		syms = ptr(*list([i.encode(
			"latin-1") for i in self._elements]))
		self.__run.num_elements = len(self._elements)
		ptr = c_double * len(self._elements)
		solars = [_globals.solar_z[i] for i in self._elements]
		solars = ptr(*solars[:])
		clib.setup_elements(byref(self.__run), syms, solars)

		for i in list(range(len(self._elements))):
			if sys.version_info[0] == 2:
				clib.read_agb_grid(byref(self.__run), 
					"%sdata/_agb_yields/%s.dat".encode("latin-1") % (
						_globals.DIRECTORY, syms[i]), i)
			elif sys.version_info[0] == 3:
				file = "%sdata/_agb_yields/%s.dat" % (_globals.DIRECTORY, 
					self._elements[i])
				clib.read_agb_grid(byref(self.__run), file.encode("latin-1"), i)
			else:
				# This should be caught at import anyway
				__version_error()
			sneia_yield = _globals.sneia_yields[self._elements[i]]
			ccsne_yield = _globals.ccsne_yields[self._elements[i]]
			clib.set_sneia_yield(byref(self.__run), i, c_double(sneia_yield))
			clib.set_ccsne_yield(byref(self.__run), i, c_double(ccsne_yield))

		eval_times = __times(output_times[-1], self._dt)
		ptr = c_double * len(eval_times)
		if self._mode == "gas":
			self.__run.spec = ptr(*list(map(self._func, eval_times)))
		else:
			self.__run.spec = ptr(*list(map(lambda t: 1e9 * self._func(t), 
				eval_times)))

		if callable(self._eta):
			eta = list(map(self._eta, eval_times))
		else:
			eta = len(eval_times) * [self._eta]

		if callable(self._enhancement):
			enhancement = list(map(self._enhancement, eval_times))
		else:
			enhancement = len(eval_times) * [self._enhancement]
			
		if callable(self._tau_star):
			tau_star = list(map(self._tau_star, eval_times))
		else:
			tau_star = len(eval_times) * [self._tau_star]

		if callable(self._dtd):
			self.__set_ria()
		else:
			pass

		self.__model.Z_solar = self._Z_solar
		self.__model.eta = ptr(*eta[:])
		self.__model.enh = ptr(*enhancement[:])
		self.__model.tau_star = ptr(*tau_star[:])
		self.__run.mdotstar = ptr(*(len(eval_times) * [0.]))
		self.__set_zin(eval_times)

		if self.__outfile_check(overwrite):
			if not os.path.exists(self._name):
				os.system("mkdir %s" % (self._name))
			else:
				pass
			times = ptr(*eval_times[:])
			ptr2 = c_double * len(output_times)
			outtimes = ptr2(*output_times[:])
			enrichment = clib.enrich(byref(self.__run), byref(self.__model), 
				self._name.encode("latin-1"), times, 
				c_long(len(eval_times)), outtimes)
		else:
			enrichment = 0

		if enrichment == 1: 
			# Couldn't open output files
			message = "Couldn't open files under directory: %s\n" % (self._name)
			raise IOError(message)
		elif enrichment == 2:
			message = "Unrecognized SNe Ia delay time distribution: %s" % (
				self._dtd)
			raise ValueError(message)
		elif enrichment == 0:
			if capture:
				return output(self._name)
			else:
				pass
		elif enrichment == -1:
			pass
		else:
			message = "Unknown return parameter: %g\n" % (enrichment)
			message += "Please submit bug reports to giganano9@gmail.com.\n"
			message += "Please also attach a copy of the script that produced "
			message += "the error and a description of the variables it uses.\n"
			message += "Please also make the subject line 'BUG in VICE'."
			raise StandardError(message)

	@staticmethod
	def __output_times_check(output_times):
		if "numpy" in sys.modules and isinstance(output_times, _np.ndarray):
			output_times = output_times.tolist()
		elif "pandas" in sys.modules and isinstance(output_times, 
			_pdf.DataFrame): 
			output_times = [i[0] for i in value.values.tolist()]
		elif isinstance(output_times, list):
			output_times = output_times[:]
		else:
			message = "Argument 'output_times' must be an array-like object."
			raise TypeError(message)
		if not all(list(map(lambda x: isinstance(x, numbers.Number), 
			output_times))):
			message = "All output times must be numerical values. "
			message += "Non-numerical value detected."
			raise TypeError(message)
		elif not all(list(map(lambda x: x >= 0, output_times))):
			message = "All output times must be non-negative. "
			raise ValueError(message)
		else:
			return output_times

	def __outfile_check(self, overwrite):
		"""
		Determines if any of the output files exist and proceeds according to 
		the user specified overwrite preference.
		"""
		outfiles = ["%s/%s" % (self._name, 
			i) for i in ["history.out", "mdf.out"]]
		if os.path.exists(self._name):
			if overwrite:
				return True
			else:
				if any(list(map(os.path.exists, outfiles))):
					question = "At least one of the output files already "
					question += "exists. If you continue with the integration, "
					question += "then their contents will be lost.\n"
					question += "Output directory: %s\n" % (self._name)
					question += "Overwrite? (y | n) "
					answer = raw_input(question)
					while answer.lower() not in ["yes", "y", "no", "n"]:
						question = "Please enter either 'y' or 'n': "
						answer = raw_input(question)
					if answer.lower() in ["y", "yes"]:
						return True
					else:
						return False
				else:
					return True
		else:
			return True


	@staticmethod
	def __args(func):
		"""
		Returns True if the function passed to it takes more than one parameter 
		or any keyword/variable/default arguments.
		"""
		if sys.version_info[0] == 2:
			args = inspect.getargspec(func)
		elif sys.version_info[0] == 3:
			args = inspect.getfullargspec(func)
		else:
			message = "Only Python versions 2.6, 2.7, and >= 3.3 are "
			message += "supported by VICE."
			raise SystemError(message)
		if args[1] != None:
			return True
		elif args[2] != None:
			return True
		elif args[3] != None:
			return True
		elif len(args[0]) != 1:
			return True
		else:
			return False

	def __agb_yields(self, symbol):
		if symbol not in _globals.RECOGNIZED_ELEMENTS:
			raise ValueError("Unrecognized element: %s" % (symbol))
		else:
			return agb_yield_grid(symbol)

	def __set_ria(self):
		times = __times(12.5, self._dt)
		ria = len(times) * [0.]
		for i in list(range(len(ria))):
			if times[i] > self._delay:
				ria[i] = self._dtd(times[i])
				if (m.isnan(ria[i]) or m.isinf(ria[i]) or ria[i] < 0): 
					message = "Custom SNe Ia DTD evaluated to negative, nan, "
					message += "or inf for at least one timestep. "
					raise ArithmeticError(message)
				else:
					continue
			else:
				continue
		norm = sum(ria)
		for i in list(range(len(ria))):
			ria[i] /= norm
		if any(list(map(lambda x: x < 0, ria))):
			message = "Custom SNe Ia DTD evaluated to negative value for at "
			message += "least one timestep."
			raise ArithmeticError(message)
		else:
			ptr = c_double * len(ria)
			self.__model.ria = ptr(*ria[:])

	def __set_zin(self, eval_times):
		"""
		Passes the inflow metallicity information to C.
		"""
		dummy = (len(eval_times) * len(self._elements)) * [0.]
		ptr = c_double * len(dummy)
		if isinstance(self._Zin, float):
			for i in list(range(len(self._elements))):
				for j in list(range(len(eval_times))):
					dummy[len(eval_times) * i + j] = self._Zin
		elif callable(self._Zin):
			for i in list(range(len(self._elements))):
				for j in list(range(len(eval_times))):
					if (m.isnan(self._Zin(eval_times[j])) or 
						m.isinf(self._Zin(eval_times[j])) or 
						self._Zin(eval_times[j]) < 0):
						message = "Inflow metallicity evaluated to negative, "
						message += "nan, or inf for at least one timestep. "
						raise ArithmeticError(message)
					else:
						dummy[len(eval_times) * i + j] = self._Zin(
							eval_times[j])
		elif isinstance(self._Zin, dict):
			for i in list(range(len(self._elements))):
				sym = self._elements[i]
				if isinstance(self._Zin[sym], float):
					for j in list(range(len(eval_times))):
						dummy[len(eval_times) * i + j] = self._Zin[sym]
				elif callable(self._Zin[sym]):
					for j in list(range(len(eval_times))):
						if (m.isnan(self._Zin[sym](eval_times[j])) or 
							m.isinf(self._Zin[sym](eval_times[j])) or 
							self._Zin[sym](eval_times[j]) < 0): 
							message = "Infow metallicity evaluated to negative, " 
							message += "nan, or inf for at least one timestep." 
							raise ArithmeticError(message)
						else:
							dummy[len(eval_times) * i + j] = self._Zin[sym](
								eval_times[j])
				else:
					raise SystemError("This error shouldn't be raised.")
		else:
			raise SystemError("This error shouldn't be raised.")
		clib.setup_Zin(self.__run, byref(self.__model), ptr(*dummy[:]), 
			len(eval_times))


class __model_struct(Structure):

	"""
	The wrapping of the model struct defined in specs.h.

	User access of this class is strongly discouraged.
	"""

	_fields_ = [
		("imf", c_char_p), 
		("dtd", c_char_p), 
		("mdf", POINTER(POINTER(c_double))), 
		("bins", POINTER(c_double)), 
		("num_bins", c_long), 
		("eta", POINTER(c_double)), 
		("enh", POINTER(c_double)), 
		("Zin", POINTER(POINTER(c_double))), 
		("R", POINTER(c_double)), 
		("H", POINTER(c_double)), 
		("tau_star", POINTER(c_double)),
		("schmidt_index", c_double), 
		("mgschmidt", c_double), 
		("t_d", c_double), 
		("tau_ia", c_double), 
		("ria", POINTER(c_double)), 
		("smoothing_time", c_double), 
		("m_upper", c_double), 
		("m_lower", c_double), 
		("R0", c_double), 
		("continuous", c_int), 
		("schmidt", c_int), 
		("Z_solar", c_double)
	]


class __element_struct(Structure):

	"""
	The wrapping of the element struct defined in specs.h.

	User access of this class is strongly discouraged.
	"""

	_fields_ = [
		("symbol", c_char_p), 
		("ccsne_yield", c_double), 
		("sneia_yield", c_double), 
		("agb_grid", POINTER(POINTER(c_double))), 
		("agb_m", POINTER(c_double)), 
		("agb_z", POINTER(c_double)), 
		("num_agb_m", c_long), 
		("num_agb_z", c_long),
		("m_ccsne", c_double), 
		("m_sneia", c_double), 
		("m_ag", c_double), 
		("m_tot", c_double), 
		("breakdown", POINTER(POINTER(c_double))), 
		("solar", c_double)
	]


class __integration_struct(Structure):

	"""
	The wrapping of the integration struct defined in specs.h.

	User access of this class is strongly discouraged.
	"""

	_fields_ = [
		("out1", c_void_p), 
		("out2", c_void_p), 
		("out3", c_void_p), 
		("mode", c_char_p), 
		("spec", POINTER(c_double)), 
		("MG", c_double), 
		("SFR", c_double), 
		("IFR", c_double), 
		("num_elements", c_int), 
		("mdotstar", POINTER(c_double)), 
		("Zall", POINTER(POINTER(c_double))), 
		("dt", c_double), 
		("current_time", c_double), 
		("timestep", c_long), 
		("elements", c_void_p)
	]


# Returns the evaluation times given a stopping time and a timestep size
def __times(stop, dt):
	arr = (long(stop / dt) + 2) * [0.]
	for i in list(range(len(arr))):
		arr[i] = i * dt
	return arr




