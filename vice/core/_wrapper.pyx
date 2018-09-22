
# Python Functions
from __future__ import print_function, division, unicode_literals
# from _agb_yields import yield_grid as agb_yield_grid
from ..data import agb_yield_grid
from _data_management import output
import _globals
import warnings
import numbers
import inspect
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
def version_error():
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
	imf:				The initial mass function
	eta:				The mass loading factor
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



	Built-in Attributes:
	====================
	recognized_elements:		The elements that this software is built to 
					model the enrichment for
	recognized_imfs:		The stellar initial mass functions that this 
					software has built in



	Functions:
	==========
	settings:			Prints the current model parameters
	run:				Runs the integration functions on the parameters



	While the attribute func must be a function of time in Gyr, the user has 
	the option to do the same with attributes eta and tau_star. If the user 
	passes a numerical value for these parameters, then it will be that 
	numerical value at all times in the integration. However, in the event that 
	the user initializes one of these attributes as a callable python function, 
	then this software will let that parameter take on the value the function 
	returns at all times during the integration. This allows the user to 
	specify models of star formation efficiency and mass loading parameters 
	that are time-dependent with arbitrary degrees of complexity. 



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

	>>> import onezone as oz
	>>> import numpy as np
	>>> i = oz.integrator(func = np.exp)

	If the user desires NumPy's exp function to be passed as the func 
	attribute, then this can be implemented in the following manner:

	>>> import onezone as oz
	>>> import numpy as np
	>>> def f(t):
	>>>     return np.exp(t)
	>>> i = oz.integrator(func = f)

	This sort of wrapping can also be done in a single line at the time of 
	initialization using a <lambda>:

	>>> import onezone as oz
	>>> import numpy as np
	>>> i = oz.integrator(func = lambda t: np.exp(t))

	See docstrings for attributes eta, tau_star, and func for more direction on 
	how to specify these parameters according to your model.



	USERS' WARNING ON EMULATING DELTA FUNCTIONS IN ATTRIBUTES:
	==========================================================
	Here we simply wish to make the user aware of a couple things so that when 
	they emulate delta functions, the output of their integration properly 
	reflects that. These can be done in effect by letting one quantity take on 
	some very high value for one timestep. If the user wishes to build a delta 
	function into their model, they simply need to make sure that:

	1) They let their delta function have an intrinsic finite width of at 
	   least one timestep. Otherwise, it is not guaranteed that the numerical 
	   integrator will find the delta function. 

	2) They have set their output times such that the integrator will write 
	   to the output file at the time of the delta function. Otherwise, the 
	   integrator will still exhibit the behavior of the delta function 
	   they've built in, but it will not be shown in the output file in the 
	   quantity in which they've built-in a delta function. 

	Delta functions of any kind tend to make any physical system behave 
	eradically for a brief period. Thus we recommend that when you employ a 
	delta function, you set your integration to write output at every timestep 
	following the delta function for a brief time interval. This merely 
	ensures that the output and subsequent plots will show the full behavior 
	of the integration. Otherwise the output may show breaks and 
	discontinuities where there are none when finer output time intervals are 
	used. 

	See docstring of integrator.run() for instructions on how to specify your 
	output times. 
	"""
	def __init__(self, name = "onezonemodel", 
		func = _globals._DEFAULT_FUNC, 
		mode = "ifr", 
		imf = "kroupa", 
		schmidt = False, 
		eta = 2.5, 
		zeta = 2.5, 
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
		MgSchmidt = 6.0e9):

		"""
		Kwargs, Defaults, and Units:
		============================
		name 		= "onezonemodel"
		func 		= def f(t): return 9.1 [mode-dependent]
		mode 		= "ifr"  
		eta  		= 2.5 
		zeta 		= 2.5 
		recycling 	= "continuous"
		bins 		= [-3, -2.99, -2.98, ... , 0.98, 0.99, 1]
		delay		= 0.15 [Gyr]
		dtd 		= "plaw"
		Mg0		= 6.0e9 [Msun]
		smoothing 	= 0.0 [Gyr]
		tau_Ia		= 1.5 [Gyr]
		tau_star 	= 2.0 [Gyr]
		dt 		= .001 [Gyr]
		"""

		# The integration and model structs from the C-wrapping
		# User access of these parameters is strongly discouraged
		self.__model = __model_struct()
		self.__run = __integration_struct()

		# Call the setter methods for each attribute for type-checking
		self.name = name
		self.func = func
		self.mode = mode
		self.imf = imf
		self.eta = eta
		self.zeta = zeta
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

	@property
	def recognized_elements(self):
		"""
		The symbols of the elements whose enrichment properties are built into 
		this software. This is also the order in which they will appear in the 
		output files.
		"""
		return _globals.RECOGNIZED_ELEMENTS

	@property
	def recognized_imfs(self):
		"""
		The initial mass functions (IMFs) that are built into this software. 
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

		>>> example = onezone.integrator()
		>>> example.name = "onezonemodel"
				
		The above will create an output file under the name 
		onezonemodel in your current working directory at the time of 
		integration. 

		>>> example = onezone.integrator()
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
			version_error()

		#Type Error
		if throw:
			message = "Attribute name must be of type string. Got: %s" % (
				type(value))
			raise TypeError(message)
		else:
			pass

	# @name.deleter
	# def name(self):
	# 	del self._name

	@property
	def func(self):
		"""
		The specified function of time. This can represent either the 
		infall rate in Msun/yr, the star formation rate in Msun/yr, or the gas 
		gass in Msun. The specification between these is set by the 
		attribute 'mode'. Note that the parameter this function takes will 
		always be interpreted as time in Gyr. 

		See class docstring for users' note on setting functions as attribute 
		values.

		Example: An exponentially declining infall rate with an e-folding 
		timescale of 6 Gyr:

		>>> import onezone as oz
		>>> import numpy as np
		>>> def f(t):
		>>>     return 9.1 * num.exp( -t / 6 )
		>>> i = oz.integrator(mode = "ifr", func = f)

		Example: An exponentially declining infall rate with an e-folding 
		timescale of 6 Gyr, but very little gas at the start of integration, 
		emulating a linear-exponential gas history:

		>>> import onezone as oz
		>>> import numpy as np
		>>> def f(t):
		>>>     return 9.1 * num.exp( -t / 6 )
		# Specify only 1 solar mass of gas at the first timestep
		>>> i = oz.integrator(mode = "ifr", func = f, Mg0 = 1)

		Example: The previous history, but with attributes initialized in 
		different steps rather than in one line:

		>>> import onezone as oz
		>>> import numpy as np
		>>> def f(t):
		>>>     return 9.1 * num.exp( -t / 6 )
		>>> i = oz.integrator()
		>>> i.mode = "ifr"
		>>> i.func = f
		>>> i.Mg0 = 1

		See docstring of attribute mode for more details.
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

	# @func.deleter
	# def func(self):
	# 	del self._func

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
			version_error()

		# TypeError
		if throw:
			message = "Attribute name must be of type string. Got: %s" % (
				type(value))
			raise TypeError(message)
		else:
			pass

	# @mode.deleter
	# def mode(self):
	# 	del self._mode

	@property
	def Mg0(self):
		"""
		The gas mass in Msun at time = 0, when the integration will start. 

		Note that this parameter is only relevant in infall mode. When in 
		gas mode, the initial gas supply will simply be taken as self._func(0), 
		and in sfr mode, the initial gas supply is taken from the star 
		formation rate at time 0 times the depletion time at time 0.
		"""
		return self._Mg0

	@Mg0.setter
	def Mg0(self, double value):
		self._Mg0 = value
		self.__run.MG = value

	# @Mg0.deleter
	# def Mg0(self):
	# 	del self._Mg0

	@property
	def imf(self):
		"""
		The initial mass function (IMF) to use in the model as a string. This 
		parameter is case-insensitive and will always be converted to a 
		lower-case string.

		Note that this software currently only recognized Salpeter and 
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
					self._imf = value.lower()
					self.__model.imf = value.lower().encode("latin-1")
				else:
					raise ValueError("Unrecognized IMF: %s" % (value))
			else:
				throw = True
		else:
			# This should be caught at import anyway
			version_error()

		# TypeError
		if throw:
			message = "Attribute imf must be of type string. Got: %s" % (
				type(value))
			raise TypeError(message)
		else:
			pass

	# @imf.deleter
	# def imf(self):
	# 	del self._imf

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

	# @eta.deleter
	# def eta(self):
	# 	del self._eta

	@property
	def zeta(self):
		"""
		The unitless metal-loading factor. Along with eta, this attribute 
		determines the metallicity of the outflowing gas in the following 
		manner:

		Z_out / Z_gas = zeta / eta

			raise TypeError(message)

	# @eta.deleter
	# def eta(self):
		This parameter can be a single numerical value or a callable function 
		of time in Gyr.
		"""
		return self._zeta

	@zeta.setter
	def zeta(self, value):
		if callable(value):
			if self.__args(value):
				message = "Attribute 'zeta', when callable, must take only one "
				message += "parameter and no keyword/variable/defaults "
				message += "parameters."
				raise ValueError(message)
			else:
				self._zeta = value
		elif isinstance(value, numbers.Number):
			self._zeta = float(value)
		else:
			message = "Attribute 'zeta' must be either a callable python "
			message += "function or a numerical value. Got: %s" % (type(value))
			raise TypeError(message)

	@property
	def recycling(self):
		"""
		The recycling specification. This represents the cumulative return 
		fraction following a single episode of star formation (i.e. the 
		mass fraction that is returned to the ISM from stars). 

		If a numerical value is specified, this will be treated as the an 
		instantaneous return fraction. For example, if recycling = 0.4, then 
		at all timesteps, the integrator will return 40%% of all mass that 
		goes into star formation back to the ISM at that timestep. 

		Otherwise, the user may specify the string "continuous" (case-
		insensitive) and the integrator will use a more sophisticated time-
		dependent formulation of the cumulative return fraction given the 
		initial mass function and the mass in stellar remnants following a 
		single episode of star formation. 

		See seciont ##.## of Johnson & Weinberg (2018, in prep) for details.
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

	# @recycling.deleter
	# def recycling(self):
	# 	del self._recycling

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
	def delay(self, double value):
		self._delay = value
		self.__model.t_d = value

	# @delay.deleter
	# def delay(self):
	# 	del self._delay

	@property
	def tau_Ia(self):
		"""
		The e-folding timescale of SNe Ia in Gyr. This attribute is only 
		relevant if the delay-time distribution (attribute dtd) is set to 
		"exp", in which case, the SNe Ia rate goes as exp( -t / tau_Ia ).

		If a power law DTD is used (i.e. if self.dtd == "plaw"), then this 
		parameter plays no role in the integration.
		"""
		return self._tau_Ia

	@tau_Ia.setter
	def tau_Ia(self, double value):
		self._tau_Ia = value
		self.__model.tau_ia = value

	# @tau_Ia.deleter
	# def tau_Ia(self):
	# 	del self._tau_Ia

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
		"""
		return self._tau_star

	@tau_star.setter
	def tau_star(self, value):
		if isinstance(value, numbers.Number):
			self._tau_star = float(value)
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

	# @tau_star.deleter
	# def tau_star(self):
	# 	del self._tau_star

	@property
	def schmidt(self):
		"""
		A boolean describing whether or not to use Schmidt-law efficiency, the 
		specifications for which are set by the attributes schmidt_index and 
		MgSchmidt.
		"""
		return self._schmidt

	@schmidt.setter
	def schmidt(self, value):
		try:
			self._schmidt = bool(value)
			if self._schmidt:
				self.__model.schmidt = 1
			else:
				self.__model.schmidt = 0
		except:
			raise TypeError("Attribute Schmidt must be of type boolean.")

	@property
	def schmidt_index(self):
		"""
		The power-law index for the depletion time derived from a schmidt-law 
		star formation efficiency:

		SFE = tau_star(t)^-1 * (Mgas / MgSchmidt)**(schmidt_index)
		"""
		return self._schmidt_index

	@schmidt_index.setter
	def schmidt_index(self, double value):
		self._schmidt_index = value
		self.__model.schmidt_index = value

	@property
	def MgSchmidt(self):
		"""
		The normalization on the Schmidt-Law: 

		SFE \propto (Mgas / MgSchmidt)**(schmidt_index)

		In practice, this should be some fiducial gas mass. In that case, the 
		star-formation efficiency is close to what the user specifies as the 
		normalization constant tau_star(t).
		"""
		return self._MgSchmidt

	@MgSchmidt.setter
	def MgSchmidt(self, double value):
		self._MgSchmidt = value
		self.__model.mgschmidt = value

	@property
	def dtd(self):
		"""
		The delay-time distribution (DTD) of SNe Ia passed as a string. It must 
		be either "exp" for an exponential DTD or "plaw" for a power-law. 

		In the case of an exponential DTD, attribute tau_ia sets the e-folding 
		timescale. See its docstring for details.

		In the case of a power-law DTD, the power law index is -1.1. That is, 
		the integrator will treat the SNe Ia rate as t^-1.1 following every 
		episode of star formation.
		"""
		return self._dtd

	@dtd.setter
	def dtd(self, value):
		throw = False
		# Python 2.x string treatment
		if sys.version_info[0] == 2:
			if isinstance(value, basestring):
				if value.lower() in ["exp", "plaw"]:
					self._dtd = value.lower()
					self.__model.dtd = value.lower().encode("latin-1")
				else:
					raise ValueError("Unrecognized DTD: %s" % (value))
			else:
				throw = True
		# Python 3.x string treatment
		elif sys.version_info[0] == 3:
			if isinstance(value, str):
				if value.lower() in ["exp", "plaw"]:
					self._dtd = value.lower()
					self.__model.dtd = value.lower().encode("latin-1")
				else:
					raise ValueError("Unrecognized DTD: %s" % (value))
			else:
				throw = True
		else:
			# This should be caught at import anyway
			version_error()

		# TypeError
		if throw:
			message = "Attribute dtd must be of type string. Got: %s" % (
				type(value))
			raise TypeError(message)
		else:
			pass

	# @dtd.deleter
	# def dtd(self):
	# 	del self._dtd

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

		See section ##.## of Johnson & Weinberg (2018, in prep) for more details 
		on smoothing timescales.
		"""
		return self._smoothing

	@smoothing.setter
	def smoothing(self, double value):
		self._smoothing = value
		self.__model.smoothing_time = value

	# @smoothing.deleter
	# def smoothing(self):
	# 	del self._smoothing

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
		if isinstance(value, str):
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
		The time difference to use in the integration in Gyr.
		"""
		return self._dt

	@dt.setter
	def dt(self, double value):
		self._dt = value
		self.__run.dt = value

	# @dt.deleter
	# def dt(self):
	# 	del self._dt

	def settings(self):
		"""
		Prints the current parameters of the integrator to the screen. 
		"""
		print("Current Parameters:")
		print("===================")
		print("Name: %s" % (self._name))
		print("Func:", self._func)
		print("Mode: %s" % (self._mode))
		print("Eta:", self._eta)
		print("Zeta:", self._zeta)
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
					that it all elements be numerical values. The user may even 
					specify that they would like output at time 'inf', 
					which, unless one of their attributes would result in an 
					overflow error, would result in an indefinitely running 
					integration. They may specify this if they so wish. 

		Kwargs:
		=======
		capture = False:	Whether or not to return an output object for the 
					results of the integration. See class docstring for 
					type 'output' for details.
		overwrite = False:	Whether or not to force overwrite any files that 
					may be under the same name, perhaps from previous 
					integrations.

		User's Warning on Overwrite:
		============================
		In the event that the user is running many onezone models initialized 
		in their own Python scripts, they will want to pay attention to the 
		names of the models they're running. 

		This acts as a halting function in that if it finds any files under the 
		same name that it is attempting to create and write to, then it will 
		stop and wait for the user's input on whether or not to continue. 
		However, if many models are running with potentially the same name, 
		then it is to the user's advantage to set overwrite = True so that 
		their code doesn't halt and wait for their input.

		This feature can be turned off by simply specifying overwrite = True 
		when this function is called, and this software will take that as 
		permission from the user to destroy all files with the same name that 
		they have specified. 
		"""
		output_times = sorted(output_times)
		self.__run.MG = self._Mg0
		self.__model.m_upper = 100
		self.__model.m_lower = 0.08
		ptr = c_char_p * len(_globals.RECOGNIZED_ELEMENTS)
		syms = ptr(*list([i.encode(
			"latin-1") for i in _globals.RECOGNIZED_ELEMENTS]))
		self.__run.num_elements = len(_globals.RECOGNIZED_ELEMENTS)
		ptr = c_double * len(_globals.RECOGNIZED_ELEMENTS)
		solars = [_globals.solar_z[i] for i in _globals.RECOGNIZED_ELEMENTS]
		solars = ptr(*solars[:])
		clib.setup_elements(byref(self.__run), syms, solars)

		for i in list(range(len(_globals.RECOGNIZED_ELEMENTS))):
			if sys.version_info[0] == 2:
				clib.read_agb_grid(byref(self.__run), 
					"%s/data/_agb_yields/%s.dat".encode("latin-1") % (
						_globals.DIRECTORY, syms[i]), i)
			elif sys.version_info[0] == 3:
				clib.read_agb_grid(byref(self.__run), 
					b"%s/data/_agb_yields/%s.dat" % (
						_globals.DIRECTORY, syms[i], i))
			else:
				# This should be caught at import anyway
				version_error()
			sneia_yield = _globals.sneia_yields[_globals.RECOGNIZED_ELEMENTS[i]]
			ccsne_yield = _globals.ccsne_yields[_globals.RECOGNIZED_ELEMENTS[i]]
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

		if callable(self._zeta):
			zeta = list(map(self._zeta, eval_times))
		else:
			zeta = len(eval_times) * [self._zeta]
			
		if callable(self._tau_star):
			tau_star = list(map(self._tau_star, eval_times))
		else:
			tau_star = len(eval_times) * [self._tau_star]

		self.__model.Z_solar = 0.014
		self.__model.eta = ptr(*eta[:])
		self.__model.zeta = ptr(*zeta[:])
		self.__model.tau_star = ptr(*tau_star[:])
		self.__run.mdotstar = ptr(*(len(eval_times) * [0.]))

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

	def __outfile_check(self, overwrite):
		"""
		Determines if any of the output files exist and proceeds according to 
		the user specified overwrite preference.
		"""
		outfiles = [b"%s/%s" % (self._name, 
			i) for i in [b"history.out", b"mdf.out"]]
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
					while answer.lower() not in [b"yes", b"y", b"no", b"n"]:
						question = "Please enter either 'y' or 'n': "
						answer = raw_input(question)
					if answer.lower() in [b"y", b"yes"]:
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
		("zeta", POINTER(c_double)), 
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




