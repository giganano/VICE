"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 

This file wraps the C subroutines of the single_stellar_population function 
and the singlezone class. Most of the scientific utility of VICE that the user 
interacts with is scripted in this file. 
"""

# Python Functions
from __future__ import (print_function, division, unicode_literals, 
	absolute_import)
from . import _yields 
from . import _data_utils as _du
from ._globals import _RECOGNIZED_ELEMENTS
from ._globals import _RECOGNIZED_IMFS
from ._globals import _version_error
from ._globals import ScienceWarning
from ._globals import _DEFAULT_FUNC 
from ._globals import _DEFAULT_BINS
from ._globals import _DIRECTORY
import math as m
import warnings
import numbers
import inspect
import pickle
import sys
import os
try:
	# NumPy compatible but not NumPy dependent
	import numpy as _np
except ImportError:
	pass
try:
	# Pandas compatible but not Pandas dependent
	import pandas as _pd
except ImportError:
	pass
try: 
	# dill for function encoding in saving an output object 
	import dill 
except ImportError: 
	pass

# C Functions
from libc.stdlib cimport malloc, free
from ctypes import *
clib = pydll.LoadLibrary("%ssrc/enrichment.so" % (_DIRECTORY))

__all__ = ["singlezone", "single_stellar_population", "mirror"] 
__all__ = [str(i) for i in __all__] # appease python 2 strings  

if sys.version_info[0] == 2: 
	strcomp = basestring
elif sys.version_info[0] == 3:
	strcomp = str
else:
	_version_error()



#------------------------------ MIRROR FUNCTION ------------------------------# 
def mirror(output_obj): 
	"""
	Returns a singlezone integrator with the same attributes as that which 
	ran a given VICE output. 

	Args:
	=====
	output_obj: 		An instance of the vice.output class 

	Encoding functional parameters from VICE output objects as well as 
	re-loading them back into a singlezone integrator object depends on the 
	package dill (installable via pip). If the user does not have dill installed, 
	functional attributes of the singlezone class (including the attribute 
	'func') will be initialized according to the default parameters. 
	"""
	# First Type-check the parameter 
	if isinstance(output_obj, _du.output): 
		"""
		With or without dill, the saved parameters will load fine. If the 
		user does not have dill, they will be switched to None and everything 
		at this point will proceed just fine. 

		One potential error of this function is that if the integration was 
		ran on a computer with dill and is being read in on a computer without 
		dill, this will likely cause an error upon reading it back in. 
		Unfortunately there is no way of knowing this until the parameters are 
		read. 
		"""
		try:
			params = pickle.load(open("%s.vice/params.config" % (
				output_obj.name), "rb")) 
		except ImportError: 
			message = "This output has encoded functional attributes, " 
			message += "indicating that it was ran on a system in which " 
			message += "dill is installed (installable via pip). To " 
			message += "instantiate a singlezone object off of this object, "
			message += "please install dill, or rerun the original singlezone " 
			message += "object on this machine if its parameters are known." 
			raise ImportError(message) 
		
		if "dill" in sys.modules: 
			# Proceed without hesitation about functional attributes 
			return singlezone(**params) 

		else: 
			# Warn the user that given attributes will be the default 
			copy = {} 
			functional = []
			# Simply remove those parameters from the kwargs to singlezone
			for i in params: 
				if params[i] == None: 
					functional.append(i)
				else:
					# Only copy those which aren't functional 
					copy[i] = params[i]  

			if isinstance(params["zin"], dict): 
				# check for callable functions in the zin object 
				for i in params["elements"]: 
					if params["zin"][i.lower()] == None:  
						functional.append("zin(%s)" % (i))
						copy["zin"][i.lower()] = 0 
					else:
						copy["zin"][i.lower()] = params["zin"][i.lower()] 
				# Cast it back to a list for the integrator 
				copy["zin"] = [copy["zin"][i.lower()] for i in copy["elements"]]

			message = "Re-instancing functional attributes from VICE output " 
			message += "objects requires the python package dill (included "
			message += "with anaconda). The following attributes will not " 
			message += "reflect the attributes of the simulation that produced " 
			message += "this output, and will instead be set to the default "
			message += "value: "
			for i in functional: 
				message += "%s " % (i) 

			warnings.warn(message, UserWarning) 

			return singlezone(**copy) 
	else:
		message = "Argument must be a vice.output object. Got: %s" % (
			type(output_obj)) 
		raise TypeError(message)



#--------------- SINGLE STELLAR POPULATION ENRICHMENT FUNCTION ---------------# 
def single_stellar_population(element, mstar = 1e6, Z = 0.014, time = 10, 
	dt = 0.01, m_upper = 100, m_lower = 0.08, IMF = "kroupa", RIa = "plaw", 
	delay = 0.15, agb_model = "cristallo11"):
	"""
	Calculates the mass of a given element produced by a single stellar 
	population from core-collapse supernovae, type Ia supernovae, and asymptotic 
	giant branch stars as a function of time.

	Args:
	=====
	element:		A string for the symbol of the element to simulate

	Kwargs:
	=======
	mstar = 1e6:		The mass of the stellar population that forms at t = 0
	Z = 0.014:		The metallicity by mass of the stellar population
	time = 10:		The amount of time in Gyr to simulate
					This value, by VICE's design, must be < 15 Gyr. 
	dt = 0.01:		The timestep size in Gyr to use
	m_upper = 100:		The upper mass limit on star formation in Msun
	m_lower = 0.08:		The lower mass limit on star formation in Msun
	IMF = "kroupa":		A string denoting the IMF to assume
	RIa = "plaw":		The SNe Ia delay-time distribution to assume
				Can be either "plaw", "exp", or a custom function of time in Gyr
	delay = 0.15:		The minimum delay time on SNe Ia in Gyr
	agb_model = "cristallo11":	The keyword for the AGB yield model to adopt. 
					See below for a list of recognized keywords

	Returns:
	========
	A 2-element python list ---> Both elements of type <list> 
	returned[0]: 		The mass of the given element in Msun at each time in Gyr 
	returned[1]: 		The times in Gyr 
	
	AGB yield models and their keywords:
	====================================
	cristallo11:		Cristallo et al. (2011), ApJS, 197, 17
	karakas10:		Karakas et al. (2010), MNRAS, 403, 1413
	"""
	
	# Type error checks
	if not isinstance(element, strcomp): # The element must be a string
		message = "First argument must be of type string. Got: %s" % (
			type(element))
		raise TypeError(message)
	elif not isinstance(IMF, strcomp): # The IMF must be a string
		message = "Keyword arg 'IMF' must be of type string. Got: %s" % (
			type(IMF))
		raise TypeError(message)
	else:
		pass
	if isinstance(RIa, strcomp):
		# Value error check here
		if RIa.lower() not in ["exp", "plaw"]: 
			"""
			SNe Ia DTD can be either a string or a user-specified 
			function of time, just like in the singlezone object. 
			"""
			message = "When a string, keyword arg 'RIa' must be either "
			message = "'exp' or 'plaw'. Got: %s" % (RIa)
			raise ValueError(message)
		else:
			pass
	elif callable(RIa):
		if singlezone()._singlezone__args(RIa):
			# If callable, RIa must take only one parameter
			message = "When callable, keyword arg 'RIa' must take only "
			message = "one parameter and no keyword/variable/default "
			message = "arguments."
			raise ValueError(message)
		else:
			pass
	else:
		message = "Keyword arg 'RIa' must be either of type string or a "
		message = "callable function with only one parameter. Got: %s" % (
			type(RIa))
		raise TypeError(message)
	if not isinstance(agb_model, strcomp):
		# agb_model has to be a string ---> a keyword 
		message = "Keyword argument 'agb_model' must be of type string. "
		message += "Got: %s" % (type(agb_model))
		raise TypeError(message)
	else:
		pass

	"""
	Mstar, Z, dt, m_upper, m_lower, and delay must all be numerical values. 
	The numbers package allows Python to catch all of these types. Simply 
	raise a TypeError if it is not a numbers.Number instance. 
	"""
	if not isinstance(mstar, numbers.Number):
		message = "Keyword arg 'mstar' must be a numerical value. Got: %s" % (
			type(mstar))
		raise TypeError(message)
	elif not isinstance(Z, numbers.Number):
		message = "Keyword arg 'Z' must be a numerical value. Got: %s" % (
			type(Z))
		raise TypeError(message)
	elif not isinstance(time, numbers.Number):
		message = "Keyword arg 'time' must be a numerical value. Got: %s" % (
			type(time))
		raise TypeError(message0)
	elif not isinstance(dt, numbers.Number):
		message = "Keyword arg 'dt' must be a numerical value. Got: %s" % (
			type(dt))
		raise TypeError(message)
	elif not isinstance(m_upper, numbers.Number):
		message = "Keyword arg 'm_upper' must be a numerical value. Got: %s" % (
			type(m_upper))
		raise TypeError(message)
	elif not isinstance(m_lower, numbers.Number):
		message = "Keyword arg 'm_lower' must be a numerical value. Got: %s" % (
			type(m_lower))
		raise TypeError(message)
	elif not isinstance(delay, numbers.Number):
		message = "Keyword arg 'delay' must be a numerical value. Got: %s" % (
			type(delay))
		raise TypeError(message)
	else:
		pass

	# Study keywords to their full citations ---> agb_model keywords 
	studies = {
		"cristallo11":		"Cristallo et al. (2011), ApJS, 197, 17", 
		"karakas10":		"Karakas et al. (2010), MNRAS, 403, 1413"
	}

	"""
	Value check errors
	==================
	These lines simply check for unphysical values or unrecognized keywords, 
	and raise a ValueError if the conditions are not met. In the case of time, 
	VICE by design does not simulate evolution on timescales longer than 15 Gyr. 

	Also of note is that the Karakas et al. (2010) study of AGB star 
	nucleosynthetic yields did not study elements heavier than nickel.  
	"""
	if element.lower() not in _RECOGNIZED_ELEMENTS:
		message = "Unrecognized element: %s" % (element)
		raise ValueError(message)
	elif mstar <= 0:
		message = "Keyword arg 'mstar' must be greater than zero." 
		raise ValueError(message)
	elif Z < 0:
		message = "Keyword arg 'Z' must be non-negative." 
		raise ValueError(message)
	elif time <= 0:
		message = "Keyword arg 'time' must be greater than zero."
		raise ValueError(message)
	elif time > 15:
		message = "By design, VICE does not simulate enrichment on timescales "
		message += "longer than 15 Gyr as this introduces numerical artifacts." 
		raise ValueError(message)
	elif dt <= 0:
		message = "Keyword arg 'dt' must be greater than zero."
		raise ValueError(message)
	elif m_upper <= 0: 
		message = "Keyword arg 'm_upper' must be greater than zero."
		raise ValueError(message)
	elif m_lower <= 0:
		message = "Keyword arg 'm_lower' must be greater than zero."
		raise ValueError(message)
	elif m_lower >= m_upper:
		message = "Keyword arg 'm_upper' must be larger than 'm_lower'."
		raise ValueError(message)
	elif IMF.lower() not in _RECOGNIZED_IMFS:
		raise ValueError("Unrecognized IMF: %s" % (IMF))
	elif delay < 0:
		message = "Keyword arg 'delay' must be non-negative."
		raise ValueError(message)
	elif agb_model.lower() not in studies:
		message = "Unrecognized AGB yield model: %s" % (agb_model)
		message = "See docstring for list of recognized models." 
		raise ValueError(message)
	elif (agb_model.lower() == "karakas10" and 
		_yields.atomic_number[element.lower()] > 28):
		message = "The %s study did not report yields for elements: " % (
			studies["karakas10"])
		message += "heavier than nickel."
		raise LookupError(message)
	else:
		pass

	# Create dummy model and integration structs 
	ms = __model_struct()
	r = __integration_struct()
	clib.setup_dummy_element(byref(r)) # Setup a dummy element for ease 
	ms.m_upper =  m_upper				# Fill the struct w/kwargs 
	ms.m_lower = m_lower
	ms.imf = IMF.lower().encode("latin-1")

	# Find the file associated with the AGB yield grid
	agbfile = ("%sdata/_agb_yields/%s/%s.dat" % (_DIRECTORY, 
		agb_model.lower(), element.lower()))
	if os.path.exists(agbfile):
		clib.read_agb_grid(byref(r), agbfile.encode("latin-1"), 0)
	else:
		message = "The associated AGB star yield file was not found. "
		message += "Please re-install VICE."
		raise LookupError(message)

	# Construct time arrays
	eval_times = __times(time + 10 * dt, dt)[:-1]
	ria_times = __times(15, dt)
	ria = len(ria_times) * [0.] 
	# Fill the DTD at all evaluation times 
	for i in list(range(len(ria))):
		if i * dt < delay:
			continue
		elif i * dt >= 13.8:
			continue
		else:
			if RIa.lower() == "plaw":
				ria[i] = (ria_times[i] + 1.e-12)**(-1.1)
			elif RIa.lower() == "exp":
				ria[i] = m.exp( -ria_times[i] / 1.5)
			elif callable(RIa):
				ria = RIa(ria_times[i])
	# Check the RIa array for any numerical artifacts ... 
	if any(list(map(lambda x: m.isnan(x) or m.isinf(x) or x < 0, ria))):
		message = "Custon SNe Ia DTD evaluated to negative, nan, or inf for at "
		message += "at least one timestep."
		raise ArithmeticError(message)
	else:
		pass
	norm = sum(ria) # ... and then normalize it 
	ria = list(map(lambda x: x / norm, ria))[:len(eval_times)]

	# Setup the core-collapse yield of the element
	ccsne_yield = _yields.ccsne_yields[element.lower()]
	if callable(ccsne_yield):
		# If the core-collapse yield is callable, need to check its args 
		if singlezone()._singlezone__args(ccsne_yield):
			message = "Yields from core-collapse supernovae, when passed as a "
			message += "function of metallicity, must take only one parameter "
			message += "and no variable/keyword/default arguments."
			raise ValueError(message)
		else:
			"""
			These lines need changed if the user modifies their copy of VICE 
			and changes the step size of the core-collapse yield grid. By 
			default it is 1e-5, and the treatment of this in C at the top of 
			the ccsne.c file. 
			"""
			z_arr = __times(0.5 + 1.e-5, 1.e-5)
			ptr = c_double * len(z_arr)
			arr = list(map(ccsne_yield, z_arr))
			if not all(list(map(lambda x: isinstance(x, numbers.Number), arr))):
				message = "Yield as a function of metallicity mapped "
				message += "to non-numerical value."
				raise TypeError(message)
			elif any(list(map(lambda x: x < 0, arr))):
				message = "Yield as a function of metallicity mapped to "
				message += "negative value."
				raise ValueError(message)
			else:
				clib.fill_cc_yield_grid(byref(r), 0, ptr(*arr[:]))
	elif isinstance(ccsne_yield, numbers.Number):
		# If its just a number, this is a lot easier 
		if ccsne_yield < 0:
			message = "Yield from core-collapse supernovae must be " 
			message += "non-negative."
			raise ValueError(message)
		else:
			arr = len(__times(0.5 + 1.e-5, 1.e-5)) * [ccsne_yield]
			ptr = c_double * len(arr)
			clib.fill_cc_yield_grid(byref(r), 0, ptr(*arr[:]))
	else:
		message = "IMF-integrated yield from core-collapse supernovae must "
		message += "be either a numerical value or a function of metallicity."
		raise TypeError(message)
	# Setting the SNe Ia yield is a lot easier with the current version of VICE 
	clib.set_sneia_yield(byref(r), 0, 
		c_double(_yields.sneia_yields[element.lower()]))
	ptr = c_double * len(eval_times)

	# Set up a pointer to a double to modify in the C code 
	mass = len(eval_times) * [0.]
	mass = ptr(*mass[:])
	clib.single_population(mass, byref(r), byref(ms), c_double(Z), 
		ptr(*ria[:]), ptr(*eval_times[:]), len(eval_times), c_double(mstar))

	# Copy the results into Python and return
	results = [mass[i] for i in range(len(eval_times))]
	return [results[:-10], eval_times[:-10]]




#----------------------------- SINGLEZONE OBJECT -----------------------------# 
class singlezone(object):

	"""
	CLASS: singlezone
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
	zin: 				The inflow metallicity
	recycling:			The instantaneous recycling parameter
	bins:				The bins in [X/Y] to sort the final stellar metallicity 
					distribution function into
	delay:				The minimum delay time of SNe Ia in Gyr.
	ria:				The delay time distribution (DTD) of SNe Ia
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
	agb_model:			A keyword denoting which model for AGB enrichment to adopt
	z_solar:			The value to adopt for solar metallicity by mass Z


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
	the option to do the same with attributes eta, enhancement, zin 
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
	>>> i = vice.singlezone(func = np.exp)

	If the user desires NumPy's exp function to be passed as the func 
	attribute, then this can be implemented in the following manner:

	>>> import vice
	>>> import numpy as np
	>>> def f(t):
	>>>     return np.exp(t)
	>>> i = vice.singlezone(func = f)

	This sort of wrapping can also be done in a single line at the time of 
	initialization using a <lambda>:

	>>> import vice
	>>> import numpy as np
	>>> i = vice.singlezone(func = lambda t: np.exp(t))

	See docstrings for individual attributes for more direction on how to 
	specify these parameters according to your model. 


	USERS' WARNING ON EMULATING DELTA FUNCTIONS IN ATTRIBUTES:
	==========================================================
	Here we detail a simple warning on emulating delta function in attributes. 
	VICE is a timestep-style singlezone, and therefore, these can be 
	achieved by letting a quantity take on some very high value for one 
	timestep. If the user wishes to build a delta function into their model, 
	they need to make sure that: 

	1) They let their delta function have an intrinsic finite width of at 
	   least one timestep. Otherwise, it is not guaranteed that the numerical 
	   integrator will find the delta function. 

	2) They have set their output times such that the simulation will write 
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
	to disk at every timestep. See docstring of singlezone.run for 
	instructions on how to specify your output times.
	"""

	def __init__(self, 
		name = "onezonemodel", 
		func = _DEFAULT_FUNC, 
		mode = "ifr", 
		elements = ["fe", "sr", "o"], 
		imf = "kroupa", 
		eta = 2.5, 
		enhancement = 1, 
		zin = 0, 
		recycling = "continuous", 
		bins = _DEFAULT_BINS,
		delay = 0.15, 
		ria = "plaw", 
		Mg0 = 6.0e9, 
		smoothing = 0., 
		tau_ia = 1.5, 
		tau_star = 2., 
		dt = 0.01, 
		schmidt = False, 
		schmidt_index = 0.5, 
		MgSchmidt = 6.0e9, 
		m_upper = 100, 
		m_lower = 0.08, 
		z_solar = 0.014, 
		agb_model = "cristallo11"):
		"""
		Kwargs, Defaults, and Units:
		============================
		name 		= "onezonemodel"
		func 		= def f(t): return 9.1 [mode-dependent]
		mode 		= "ifr"  
		elements 	= ["fe", "o", "sr"]
		imf 		= "kroupa" 
		eta  		= 2.5 
		enhancement 	= 2.5 
		zin		= 0
		recycling 	= "continuous"
		bins 		= [-3, -2.99, -2.98, ... , 0.98, 0.99, 1]
		delay		= 0.15 [Gyr]
		ria			= "plaw"
		Mg0		= 6.0e9 [Msun]
		smoothing 	= 0.0 [Gyr]
		tau_ia		= 1.5 [Gyr]
		tau_star 	= 2.0 [Gyr]
		dt 		= .001 [Gyr]
		schmidt 	= False 
		schmidt_index	= 0.5 
		MgSchmidt 	= 6.0e9
		m_upper 	= 100 [M_sun]
		m_lower 	= 0.08 [M_sun]
		z_solar 	= 0.014 
		agb_model 	= "cristallo11"
		"""

		"""
		The integration and model structs from the C-wrapping
		User access of these parameters is strongly discouraged
		"""
		self.__model = __model_struct()
		self.__run = __integration_struct()

		"""
		Initializing the attributes in this way calls the setter functions, 
		which allows type-checking to be done immediately with no extra 
		lines of code. 
		"""
		self.name = name
		self.func = func
		self.mode = mode
		self.elements = elements
		self.imf = imf
		self.eta = eta
		self.enhancement = enhancement
		self.zin = zin
		self.recycling = recycling
		self.bins = bins
		self.delay = delay
		self.ria = ria
		self.Mg0 = Mg0
		self.smoothing = smoothing
		self.tau_ia = tau_ia
		self.tau_star = tau_star
		self.schmidt = schmidt
		self.schmidt_index = schmidt_index 
		self.MgSchmidt = MgSchmidt
		self.dt = dt
		self.m_upper = m_upper
		self.m_lower = m_lower
		self.z_solar = z_solar
		self.agb_model = agb_model

	@property
	def recognized_elements(self):
		"""
		The symbols of the elements whose enrichment properties are built into 
		this software. The user can specify which elements are tracked in 
		each integration via the 'elements' attribute.
		"""
		return _RECOGNIZED_ELEMENTS

	@property
	def recognized_imfs(self):
		"""
		The initial mass functions (IMFs) that are built into this software. 
		The user can specify which one to use via the attribute 'imf'.
		"""
		return _RECOGNIZED_IMFS

	@property
	def name(self):
		"""
		The name of the model being run. The output of the 
		integration will be placed in a file in the user's 
		current working directory under the same name. To place the 
		output file under a different directory, then this 
		parameter should be initialized as the full path to the 
		desired output file. For example:

		>>> example = vice.singlezone()
		>>> example.name = "onezonemodel"
				
		The above will create an output file under the name 
		onezonemodel in your current working directory at the time of 
		integration. 

		>>> example = vice.singlezone()
		>>> example.name = "/path/to/output/directory/onezonemodel"

		The above, however, will create a folder named onezonemodel in 
		the directory /path/to/output/directory/ at the time of 
		integration and the output will be stored there. 

		It does not matter whether or not the user places a '/' at the end of 
		the name; this possibility is taken into account.
		"""
		return self._name[:-5] # remove the '.vice' extension 

	@name.setter
	def name(self, value):
		if isinstance(value, strcomp): 
			self._name = value 
			while self._name[-1] == '/': 
				# Remove any '/' the user puts on 
				self._name = self._name[:-1] 
			if self._name[-5:].lower() == ".vice": 
				# force the '.vice' extension 
				self._name = "%s.vice" % (self._name[:-5]) 
			else:
				self._name = "%s.vice" % (self._name)
		else: 
			# If it's not a string it's a TypeError 
			message = "Attribute name must be of type string. Got: %s" % (
				type(value))
			raise TypeError(message)


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
		>>> i = vice.singlezone(mode = "ifr", func = f)

		Example: An exponentially declining infall rate with an e-folding 
		timescale of 6 Gyr, but very little gas at the start of integration, 
		emulating a linear-exponential gas history:

		>>> import vice
		>>> import numpy as np
		>>> def f(t):
		>>>     return 9.1 * np.exp( -t / 6 )
		# Specify only 1 solar mass of gas at the first timestep
		>>> i = vice.singlezone(mode = "ifr", func = f, Mg0 = 1)

		Example: The previous history, but with attributes initialized in 
		different steps rather than in one line:

		>>> import vice
		>>> import numpy as np
		>>> def f(t):
		>>>     return 9.1 * np.exp( -t / 6 )
		>>> i = vice.singlezone()
		>>> i.mode = "ifr"
		>>> i.func = f
		>>> i.Mg0 = 1

		See docstring of attribute 'mode' for more details.
		"""
		return self._func

	@func.setter
	def func(self, value):
		if callable(value):
			"""
			The function by design must be called. It must also take only 
			one parameter. 
			"""
			if self.__args(value):
				message = "Attribute 'func' must be a callable function that "
				message += "takes only one parameter with no variable, "
				message += "keyword, or default arguments."
				raise ValueError(message)
			else:
				self._func = value
		else:
			# Type error otherwise 
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
		if isinstance(value, strcomp): 
			# Make sure it's recognized 
			if value.lower() in ["ifr", "sfr", "gas"]: 
				self._mode = value.lower() 
				self.__run.mode = value.lower().encode("latin-1") 
			else:
				raise ValueError("Unrecognized mode: %s" % (value)) 
		else:
			# If it's not a string it's a TypeError
			message = "Attribute mode must be of type string. Got: %s" % (
				type(value))
			raise TypeError(message)

	@property
	def elements(self):
		"""
		The elements that are to be modeled while the integration is running. 
		They're encoded as their one- or two-letter symbols (case-insensitive). 
		This attribute accepts array-like objects and stores them in a python 
		tuple. 

		The order in which the elements appear in this tuple will dictate the 
		ratios that are quoted in the MDF. If element X appears before element 
		Y in this tuple, then VICE will determine the mdf in dN/d[Y/X]. 
		"""
		return self._elements

	@elements.setter
	def elements(self, value):
		if "numpy" in sys.modules and isinstance(value, _np.ndarray):
			# If the user passes a NumPy array, turn it into a list 
			copy = value.tolist()
		elif "pandas" in sys.modules and isinstance(value, _pd.DataFrame):
			# If the user passes a Pandas DataFrame, turn it into a list 
			copy = [i[0] for i in value.values.tolist()]
		elif type(value) in [list, tuple]:
			# If it is a Python list or tuple, pull a copy 
			copy = value[:]
		else:
			# Throw a TypeError otherwise 
			message = "Attribute 'elements' must be either a NumPy array, "
			message += "Pandas DataFrame, python list, or python tuple. "
			raise TypeError(message)

		for i in copy:
			# Make sure each element is recognized by VICE first 
			if i.lower() not in _RECOGNIZED_ELEMENTS: 
				message = "Unrecognized element: %s" % (i)
				raise ValueError(message)
			else:
				continue

		# Store the copy in the attribute ---> make it a tuple so it's immutable 
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
				""" 
				Set the initial gas supply to be barely above zero in this 
				case to avoid numerical errors  
				"""
				self._Mg0 = 1.e-12
				self.__run.MG = 1.e-12
			else:
				# Negative gas supply is unphysical 
				message = "Initial gas supply must be a positive float."
				raise ValueError(message)
		else:
			# Otherwise throw a TypeError ---> Mg0 must be a number 
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
		if isinstance(value, strcomp): 
			# Make sure it's recognized 
			if value.lower() in _RECOGNIZED_IMFS:
				# Save the copy  
				self._imf = value.lower() 
				self.__model.imf = value.lower().encode("latin-1") 
			else:
				raise ValueError("Unrecognized IMF: %s" % (value))
		else: 
			# If it's not a string it's a TypeError
			message = "Attribute imf must be of type string. Got: %s" % (
				type(value))
			raise TypeError(message) 

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
			"""
			If the user passed a function, it must take only one parameter, 
			which will be interpreted as time. 
			"""
			if self.__args(value):
				message = "Attribute 'eta', when callable, must take only one "
				message += "parameter and no keyword/variable/default "
				message += "parameters."
				raise ValueError(message)
			else:
				self._eta = value
		elif isinstance(value, numbers.Number):
			"""
			If they've passed a number, make sure it's non-negative. Negative 
			mass loading factors are unphysical. 
			"""
			if value > 0: 
				self._eta = float(value) 
			elif value == 0: 
				# raise a science warning about closed-box models 
				message = "Closed-box GCE models have been shown to over-" 
				message += "predict the metallicities of solar-neighborhood "
				message += "stars. This is known as the G-dwarf problem "
				message += "(Tinsley 1980, Fundamentals Cosmic Phys., 5, 287. "
				message += "Outflows are necessary for maintaining long-term " 
				message += "chemical equilibrium (Dalcanton 2007, ApJ, 658, 941." 
				warnings.warn(message, ScienceWarning)
			else:
				message = "Attribute 'eta' must be non-negative." 
				raise ValueError(message)
		else:
			# Otherwise throw a TypeError 
			message = "Attribute eta must be either a callable python "
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
			"""
			If the user passes a function, it must take only one parameter which 
			will be interpreted as time in Gyr. 
			""" 
			if self.__args(value):
				message = "Attribute 'enhancement', when callable, must take "
				message += "only one parameter and no keyword/variable/default "
				message += "parameters."
				raise ValueError(message)
			else:
				self._enhancement = value
		elif isinstance(value, numbers.Number):
			if value >= 0:
				# Negative enhancement factors are unphysical 
				self._enhancement = float(value)
			else:
				message = "Attribute enhancement must be non-negative." 
				raise ValueError(message)
		else:
			# Otherwise throw a TypeError 
			message = "Attribute 'enhancement' must be either a callable "
			message += "python function or a numerical value."
			raise TypeError(message)

	@property
	def zin(self):
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
			>>> example = vice.singlezone()
			>>> example.zin = len(example.elements) * [0.]
			>>> example.zin
			{"fe": 0.0, "o": 0.0, "sr": 0.0}
			>>> example.zin["fe"] = vice.solar_z["fe"]
			>>> example.zin["o"] = lambda t: vice.solar_z["o"] * (t / 10.0)
			>>> example.zin
			{"fe": 0.0012, "o": <function <lambda> at XXXXXXX>, "sr": 0.0}
		"""
		return self._zin

	@zin.setter
	def zin(self, value):
		is_array = False		# Tracking whether or not an array was passed 
		if isinstance(value, numbers.Number):
			# This must be a positive definite number 
			if value >= 0: 
				self._zin = float(value)
			else: 
				message = "Attribute zin must be a positive definite value." 
				raise ValueError(message) 
		elif callable(value):
			"""
			If they passed a function, it must take only one parameter, which 
			will be interpreted as time in Gyr. 
			"""
			if self.__args(value):
				message = "Attribute zin, when callable, must take only one "
				message += "parameter and no keyword/variable/default "
				message += "parameters."
				raise ValueError(message)
			else:
				self._zin = value 
		# Array treatment from here on out 
		elif "numpy" in sys.modules and isinstance(value, _np.ndarray):
			# Copy a NumPy array over to a list 
			copy = value.tolist()
			is_array = True
		elif "pandas" in sys.modules and isinstance(value, _pd.DataFrame):
			# Copy a Pandas DataFrame over to a list 
			copy = [i[0] for i in value.values.tolist()]
			is_array = True
		elif type(value) in [tuple, list]: 
			# Native Python array-like data structures 
			copy = value[:]
			is_array = True
		elif isinstance(value, dict): 
			# If they passed something for each element 
			frame = {} 
			# get a copy of the dictionary with lower case keys 
			try: 
				copy = dict(zip([i.lower() for i in value.keys()], 
					[value[i] for i in value.keys()]))
			except AttributeError: 
				# One of the keys wasn't a string 
				message = "When initializing attribute zin as a dictionary, " 
				message += "it must take only strings as keys."
				raise TypeError(message) 

			# Treat each element individually 	
			for i in self._elements: 
				# Check to see if the element is tracked 
				if i.lower() not in [j.lower() for j in self._elements]: 
					if i.lower() in _RECOGNIZED_ELEMENTS: 
						message = "Element not tracked by current " 
						message += "settings: %s" % (i) 
						raise ValueError(message)
					else:
						message = "Unrecognized element: %s" % (i) 
					raise ValueError(message) 
				# Check to see if they secified a value for this element 
				elif i.lower() in copy.keys(): 
					frame[i.lower()] = copy[i.lower()] 
				# Else adopt the current setting for this element 
				elif isinstance(self._zin, float) or callable(self._zin): 
					frame[i.lower()] = self._zin
				elif isinstance(self._zin, 
					_du._customizable_yield_table): 
					frame[i.lower()] = self._zin[i.lower()]
				else: 
					# Include this as a failsafe 
					raise SystemError("This shouldn't be raised.") 

			# Now cast everything to a case insensitive dataframe 
			self._zin = _du._customizable_yield_table(frame, True, "foo")

		else:
			# Otherwise throw a TypeError 
			message = "Attribute zin must be either a callable function of " 
			message += "time, a numerical value, a list of any combination "
			message += "thereof for each element, or a dictionary containing " 
			message += "any combination thereof for any subset of elements." 
			raise TypeError(message)

		"""
		Now handle the array that they passed. It must have one entry per 
		element in the simulation. 
		""" 
		if is_array:
			if len(value) != len(self._elements):
				message = "Attribute 'zin', when initialized as an array, "
				message += "must have one entry for each element. Please "
				message += "modify the attribute 'elements' first if you "
				message += "wish to add or remove elements from the " 
				message += "integration in this manner, else you can pass a "
				message += "dictionary to this function. "
				raise ValueError(message)
			else:
				pass
			dummy = len(value) * [None]
			for i in range(len(dummy)):
				# The list may contain either numbers or functions 
				if isinstance(value[i], numbers.Number):
					dummy[i] = float(value[i])
				elif callable(value[i]):
					if self.__args(value[i]):
						# Functions must take only one parameter - time in Gyr 
						message = "Attribute 'zin', when passed as an array "
						message += "containing callable functions of time, "
						message += "must contain functions which each take "
						message += "exactly one parameter with no keyword/"
						message += "variable/default arguments." 
						raise ValueError(message)
					else:
						dummy[i] = value[i]
				else:
					# Throw a TypeError if anything isn't a number or function 
					message = "Attribute 'zin', when passed as an array, "
					message += "must contain only numerical values and " 
					message += "functions of time as array elements. Error "
					message += "found at index %d. Got %s" % (i, 
						type(value[i]))
					raise TypeError(message)

			# Now cast the attribute as a case insensitive dataframe 
			self._zin = _du._customizable_yield_table(
				dict(zip([i.lower() for i in self._elements], dummy)), 
				True, "foo")	

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
		at all timesteps, the simulation will return 40% of all mass that 
		goes into star formation back to the ISM at that timestep. 

		Otherwise, the user may specify the string "continuous" (case-
		insensitive) and VICE will use a more sophisticated time-
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
			# The cumulative return fraction is by definition between 0 and 1 ... 
			if 0 <= value <= 1:
				self._recycling = float(value)
				self.__model.R0 = value
				self.__model.continuous = 0
			else:
				# ... or else it's unphysical
				message = "The cumulative return fraction must be between "
				message += "0 and 1 to be physical."
				raise ValueError(message)
		# Continuous recycling is done via a string 
		elif isinstance(value, strcomp):
			if value.lower() == "continuous":
				self._recycling = value.lower()
				self.__model.R0 = 0
				self.__model.continuous = 1
			else:
				# "continuous" is the only recognized string 
				message = "If attribute 'recycling' is to be a string, it must "
				message += "be 'continuous' (case-insensitive). "
				message += "Got: %s" % (value)
				raise ValueError(message)
		else:
			# Otherwise throw a TypeError 
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
			# Minimum delay time must be non-negative
			if value >= 0: 
				self._delay = value 
				self.__model.t_d = value
			else:
				message = "Attribute 'delay' must be a positive value."
				raise ValueError(message)
		else:
			# If it's not a number, throw a TypeError 
			message = "Attribute 'delay' must be a positive numerical value. "
			message += "Got: %s" % (type(value))
			raise TypeError(message)

	@property
	def tau_ia(self):
		"""
		The e-folding timescale of SNe Ia in Gyr. This attribute is only 
		relevant if the delay-time distribution (attribute dtd) is set to 
		"exp", in which case, the SNe Ia rate goes as exp( -t / tau_ia ).

		If a power law DTD is used (i.e. if self.dtd == "plaw"), or if the 
		user specifies their own custom DTD, then this parameter plays no role 
		in the integration.
		"""
		return self._tau_ia

	@tau_ia.setter
	def tau_ia(self, value):
		if isinstance(value, numbers.Number):
			# A physical e-folding timescale must be positive definite 
			if value > 0: 
				self._tau_ia = value
				self.__model.tau_ia = value
			else:
				message = "Attribute 'tau_ia' must be a positive value. "
				raise ValueError(message)
		else:
			# If it's not a number, throw a TypeError 
			message = "Attribute 'tau_ia' must be a positive numerical value." 
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
			# Depletion times must be positive definite 
			if value > 0:
				self._tau_star = float(value)
			else:
				message = "Attribute 'tau_star' must be positive value. "
				raise ValueError(message)
		elif callable(value):
			"""
			If the user passes a function, it must take only parameter, which 
			will be interpreted as time in Gyr. 
			"""
			if self.__args(value):
				message = "When callable, attribute 'tau_star' must take only "
				message += "one parameter and no keyword/variable/default "
				message += "arguments."
				raise ValueError(message)
			else:
				self._tau_star = value
		else:
			# Otherwise throw a TypeError 
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
			# Numbers can be interpreted as booleans 
			if value:
				self._schmidt = True
				self.__model.schmidt = 1
			else:
				self._schmidt = False
				self.__model.schmidt = 0
		if isinstance(value, bool):
			# If it's a boolean, that'll obviously work too
			self._schmidt = value
			if value:
				self.__model.schmidt = 1
			else:
				self.__model.schmidt = 0
		else:
			# Otherwise a TypeError needs thrown. 
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
		# Power law index must be a numerical value 
		if isinstance(value, numbers.Number):
			self._schmidt_index = value
			self.__model.schmidt_index = value
		else:
			message = "Attribute 'schmidt_index' must be a numerical value."
			raise TypeError(message)
		if self._schmidt_index < 0:
			"""
			A negative power law index for the Kennicutt-Schmidt law isn't 
			necessarily unphysical, but definitely unrealistic. Warn the 
			user if they passed one in case it's a bug in their code. 
			"""
			message = "Attribute 'schmidt_index' is now a negative value. "
			message += "This may introduce numerical artifacts. "
			warnings.warn(message, ScienceWarning)

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
			# Normalization of Kennicutt-Schmidt Law must be positive definite 
			if value > 0:
				self._MgSchmidt = value
				self.__model.mgschmidt = value
			else:
				message = "Attribute 'MgSchmidt' must be a positive definite "
				message += "value."
				raise ValueError(message)
		else:
			# Otherwise throw a TypeError 
			message = "Attribute 'MgSchmidt' must be a numerical value."
			raise TypeError(message)

	@property
	def ria(self):
		"""
		The SNe Ia delay-time distribution (DTD). There are two built-in 
		DTDs that VICE will automatically treat, and to use one of these 
		this attribute must be set to a particular string. 

		"exp": An exponential DTD with e-folding timescale set by the 
		attribute 'tau_ia'

		"plaw": A power-law dtd proportional to t^-1.1

		In addition to these built-in DTDs, the user also has the option to 
		pass their own function of time. Like all other attributes that 
		accept functions as parameters in VICE, it must take only one 
		parameter and no keyword/default/variable arguments. It will be 
		interpreted as the rate R as a function of time in Gyr. 

		The user need not worry about the normalization of their DTD. Prior 
		to the integration, VICE will integrate the DTD up to 13.8 Gyr and 
		normalize it automatically. Therefore, the user also need not worry 
		about how long their integrations run - the DTD will always be 
		treated the same. 
		"""
		return self._ria

	@ria.setter
	def ria(self, value):
		if callable(value):
			"""
			Allow functionality for user-specified delay-time distributions. 
			As usual, the specified function must take only one parameter, 
			which will be interpreted as time in Gyr. 
			"""
			if self.__args(value):
				message = "When callable, attribute 'ria' must take only "
				message += "one parameter and no keyword/variable/default "
				message += "parameters."
				raise ValueError(message)
			else:
				self._ria = value
				"""
				This next line just lets the C routines know that it doesn't 
				need to automatically calculate the DTD 
				"""
				self.__model.dtd = "custom".encode("latin-1")
		elif isinstance(value, strcomp):
			if value.lower() in ["exp", "plaw"]:
				# Automated functionality for exponential and power law DTDs
				self._ria = value.lower()
				self.__model.dtd = value.lower().encode("latin-1")
			else:
				raise ValueError("Unrecognized SNe Ia DTD: %s" % (value))
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
			# The smoothing time must be a positive definite float
			if value >= 0:
				self._smoothing = value
				self.__model.smoothing_time = value
			else:
				message = "Attribute 'smoothing' must be non-negative."
				raise ValueError(message)
		else:
			# If it's not a number it's a TypeError 
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
		"""
		Python 3.x will evaluate to True before reaching basestring and 
		throwing an error so no extra lines necessary here. 

		Check for anything array-like by attempting to pull a copy first, but 
		filter out strings. 
		"""
		if isinstance(value, strcomp) or isinstance(value, basestring):
			message = "Attribute 'bins' must be an array-like object of "
			message += "numerical values."
			raise TypeError(message)
		else:
			try:
				copy = value[:]
			except TypeError:
				message = "Attribute 'bins' must be an array-like object of "
				message += "numerical values."
				raise TypeError(message)

		"""
		NumPy and Pandas compatibility. Checking for their names in 
		sys.modules first ensures that there won't be an error for not 
		recognizing these packages thrown by VICE. 
		"""
		if "numpy" in sys.modules and isinstance(value, _np.ndarray):
			copy = value.tolist()
		elif "pandas" in sys.modules and isinstance(value, _pd.DataFrame):
			copy = [i[0] for i in value.values.tolist()]
		else:
			pass

		"""
		Double-check that everything is a number. If the code gets to this 
		point, the value had to be an array-like object containing numbers, 
		which is the only requirement. 
		"""
		if all(list(map(lambda x: isinstance(x, numbers.Number), copy))):
			copy = [float(i) for i in copy]
			copy = sorted(copy) # sort from least to greatest
		else:
			message = "Attribute 'bins' must be an array-like object of "
			message += "numerical values. If you've passed a NumPy or Pandas "
			message += "array, ensure that it is 1-dimensional.\n"
			message += "Got: ", value
			raise TypeError(message)

		# This property is not even stored in Python ---> only in C. 
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
			# This attribute must be a positive definite float 
			if value > 0:
				self._dt = value
				self.__run.dt = value
			else:
				message = "Attribute 'dt' must be positive definite."
				raise ValueError(message)
		else:
			# Anything non-numerical is a TypeError. 
			message = "Attribute 'dt' must be a numerical value. Got: %s" % (
				type(value))
			raise TypeError(message)

	@property
	def m_upper(self):
		"""
		The upper mass limit on star formation in solar masses.

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
			# This value must be a positive definite float 
			if value > 0: 
				self._m_upper = float(value)
				self.__model.m_upper = float(value) 
			else: 
				# Negative values are unphysical 
				message = "Attribute m_upper must be positive."
				raise ValueError(message)
			if self._m_upper < 80:
				# Science warning if the upper mass limit is below 80 
				message = "This a low upper mass limit on star formation. "
				message += "This may introduce numerical artifacts. " 
				message += "Disregard this message if this is intentional."

				warnings.warn(message, ScienceWarning)
			else:
				pass
		else:
			# Anything non-numerical is a TypeError 
			message = "Attribute m_upper must be a numerical value. Got: %s" % (
				type(value))
			raise TypeError(message)

	@property
	def m_lower(self):
		"""
		The lower mass limit on star formation in solar masses. 
		"""
		return self._m_lower

	@m_lower.setter
	def m_lower(self, value):
		if isinstance(value, numbers.Number):
			# This value must be a positive definite float 
			if value > 0:
				self._m_lower = float(value)
				self.__model.m_lower = float(value) 
			else:
				# Negative values are unphysical 
				message = "Attribute m_lower must be positive."
				raise ValueError(message)
			if self._m_lower > 0.2:
				# Science warning if the upper mass limit is sufficiently high 
				message = "This is a high lower limit on star formation. "
				message += "This may introduce numerical artifacts. "
				message += "Disregard this message if this is intentional."

				warnings.warn(message, ScienceWarning)
			else:
				pass
		else:
			# Anything non-numerical is a TypeError 
			message = "Attribute m_lower must be a numerical value. Got: %s" % (
				type(value))
			raise TypeError(message)

	@property
	def z_solar(self):
		"""
		The total solar metallicity Z_sun = M_metals / M_sun to adopt. 

		This parameter only plays a role in scaling the total metallicity 
		of stars for the sake of modelling AGB enrichment. That is, the total 
		metallicity will always be low for integrations that only trace a 
		few elements, and this can introduce numerical artifacts in the 
		enrichment of AGB stars. We therefore employ the following scaling 
		relation: 

		Z = z_solar * sum(Z_x) / sum(Z_x_solar)

		to estimate the total metallicity at each timestep and therefore 
		mitigate this numerical issue. We nonetheless recommend that if the 
		user is interested in the enrichment of metals from AGB stars, that 
		they include multiple elements in their integration so that the 
		overall metallicity is better determined at each timestep. 

		The default value is Z_sun = 0.014 (Asplund et al. 2009, ARA&A, 47, 
		481). 
		"""
		return self._z_solar

	@z_solar.setter
	def z_solar(self, value):
		if isinstance(value, numbers.Number):
			# This value is a fraction, and as such must be between 0 and 1. 
			if 0 < value < 1:
				self._z_solar = float(value)
				self.__model.Z_solar = float(value) 
			else: 
				message = "Attribute 'z_solar' must be between 0 and 1." 
				raise ValueError(message)
			if self._z_solar > 0.018: 
				"""
				Science warning if the adopted solar metallicity is high 
				enough to potentially worry about the AGB yield grid. 
				"""
				message = "VICE by default implements yields from AGB stars "
				message += "on a grid of metallicities extending up to Z = " 
				message += "0.02. We recommend avoiding modeling parameter "
				message += "spaces yielding significantly super-solar total "
				message += "metallicities."

				warnings.warn(message, ScienceWarning)
			else:
				pass
		else:
			# Anything non-numerical is a TypeError 
			message = "Attribute z_solar must be a numerical value between 0 "
			message += "an 1. Got: %s" % (type(value))
			raise TypeError(message)

	@property
	def agb_model(self):
		"""
		A keyword denoting which model of asymptotic giant branch star 
		enrichment to employ. 

		Recognized keywords and their associated papers: 
		================================================
		cristallo11:		Cristallo et al. (2011), ApJS, 197, 17
		karakas10:			Karakas (2010), MNRAS, 403, 1413
		"""
		return self._agb_model

	@agb_model.setter
	def agb_model(self, value):
		# The recognized AGB yield studies 
		recognized = ["cristallo11", "karakas10"] 
		if any(list(map(lambda x: _yields.atomic_number[x] > 28, 
			self._elements))) and value.lower() == "karakas10":
			# The Karakas (2010) yields do not go heavier than nickel 
			message = "The Karakas et al. (2010), MNRAS, 403, 1413 study "
			message += "did not report yields for elements heavier than nickel."
			message += "Modify the attribute 'elements' before proceeding."
			raise LookupError(message)
		else:
			pass
		if isinstance(value, strcomp):
			if value.lower() in recognized: 
				self._agb_model = value
			else:
				message = "Unrecognized AGB model: %s" % (value)
				raise ValueError(message)
		else:
			# Not a string ---> TypeError 
			message = "Attribute 'agb_model' must be of type string."
			raise TypeError(message)

	def settings(self):
		"""
		Prints the current parameters of the simulation to the screen. 
		"""
		frame = {}
		frame["name"] = self._name[:-5]
		frame["func"] = self._func
		frame["mode"] = self._mode 
		frame["imf"] = self._imf 
		frame["elements"] = self._elements
		frame["eta"] = self._eta
		frame["enhancement"] = self._enhancement
		frame["recycling"] = self._recycling 
		if len(self.bins) >= 10: 
			frame["bins"] = "[%g, %g, %g, ... , %g, %g, %g]" % (
				self.bins[0], self.bins[1], self.bins[2], 
				self.bins[-3], self.bins[-2], self.bins[-1]
			)
		else:
			frame["bins"] = self.bins
		frame["delay"] = self._delay
		frame["ria"] = self._ria
		frame["Mg0"] = self._Mg0
		frame["smoothing"] = self._smoothing
		frame["tau_ia"] = self._tau_ia 
		frame["tau_star"] = self._tau_star 
		frame["dt"] = self._dt 
		frame["schmidt"] = self._schmidt 
		frame["schmidt_index"] = self._schmidt_index 
		frame["MgSchmidt"] = self._MgSchmidt 
		frame["zin"] = self._zin
		frame["m_upper"] = self._m_upper 
		frame["m_lower"] = self._m_lower 
		frame["z_solar"] = self._z_solar
		frame["agb_model"] = self._agb_model

		print("Current Settings:")
		print("=================")
		for i in frame.keys(): 
			rep = "%s " % (i) 
			arrow = ""
			for j in range(15 - len(i)): 
				arrow += "-"
			rep += "%s> %s" % (arrow, str(frame[i]))
			print(rep)
		del frame


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
					simulation that VICE should write output to the 
					history file. This need not be an array of uniform 
					timesteps, or even in ascending order. VICE will 
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
		to write to, this acts as a halting function. That is, the simulation 
		will stop and wait for the user's input on whether or not to 
		continue and overwrite the existing files. When overwrite = True, 
		VICE interprets this as permission to overwrite any existing files 
		that it finds. If the user is running many integrations with 
		potentially similar names, it is to their advantage to specify 
		overwrite = True so that their integrations do not stall. 
		"""

		# Make sure the output times are as they should be 
		output_times = self.__output_times_check(output_times)

		"""
		Set the initial gas supply here so that it resets for simulations  
		ran more than once. 
		"""
		self.__run.MG = self._Mg0

		"""
		Set up the element structs with their solar abundances and symbols 
		"""
		ptr = c_char_p * len(self._elements)
		syms = ptr(*list([i.encode(
			"latin-1") for i in self._elements]))
		self.__run.num_elements = len(self._elements)
		ptr = c_double * len(self._elements)
		solars = [_yields.solar_z[i] for i in self._elements]
		solars = ptr(*solars[:])
		clib.setup_elements(byref(self.__run), syms, solars)

		"""
		Setup each element's AGB yield grid, SNe Ia yield, and CCSNe yield. 
		These are declared in the vice/core/_yields.pyx file. This for-loop 
		pulls all of the appropriate values from those dataframes. 
		"""
		for i in list(range(len(self._elements))):
			# AGB yield grids are stored in files 
			agbfile = ("%sdata/_agb_yields/%s/%s.dat" % (_DIRECTORY, 
				self._agb_model.lower(), 
				self._elements[i].lower())).encode("latin-1")
			clib.read_agb_grid(byref(self.__run), agbfile, i)
			
			"""
			Under the current version of VICE, SNe Ia yields can only be 
			numbers. 
			"""
			sneia_yield = _yields.sneia_yields[self._elements[i]]
			clib.set_sneia_yield(byref(self.__run), i, c_double(sneia_yield))
			
			# CCSNe yields, however, can be functions of metallicity Z 
			ccsne_yield = _yields.ccsne_yields[self._elements[i]]
			if callable(ccsne_yield): 
				if self.__args(ccsne_yield): 
					message = "Yields from core-collapse supernovae, when " 
					message += "passed as a function of metallicity, must "
					message += "take only one parameter and no variable/"
					message += "keyword/default arguments."
					raise ValueError(message)
				else:
					"""
					VICE maps the CCSNe yields onto a grid every 1e-5 step in 
					Z between Z = 0 and Z = 0.5. These values are copied over 
					from ccsne.c ---> if this structure ever changes, the 
					following line needs to change. 
					"""
					z_arr = __times(0.5 + 1.e-5, 1.e-5)
					ptr = c_double * len(z_arr)
					arr = list(map(ccsne_yield, z_arr))

					# Check for Type- and ValueErrors in the mapped function 
					if not all(list(map(lambda x: isinstance(x, numbers.Number), 
						arr))):
						message = "Yield as a function of metallicity mapped "
						message += "to non-numerical value." 
						raise TypeError(message)
					elif any(list(map(lambda x: x < 0, arr))):
						message = "Yield as a function of metallicity mapped "
						message += "to negative value. This is unphysical for " 
						message += "the current set of elements recognized " 
						message += "by VICE."
						raise ValueError(message)
					else:
						clib.fill_cc_yield_grid(byref(self.__run), i, 
							ptr(*arr[:]))

			# If the user passed only a number 
			elif isinstance(ccsne_yield, numbers.Number):
				if ccsne_yield < 0: 
					message = "Yield from core-collapse supernovae must be "
					message += "non-negative. This is unphysical for the " 
					message += "current set of elements recognized by VICE."
					raise ValueError(message)
				else:
					arr = len(__times(0.5 + 1.e-5, 1.e-5)) * [ccsne_yield]
					ptr = c_double * len(arr)
					clib.fill_cc_yield_grid(byref(self.__run), i, ptr(*arr[:]))

			else:
				# Otherwise it's a TypeError 
				message = "IMF-integrated yield from core collapse supernovae "
				message += "must be either a numerical value or a function "
				message += "of metallicity."
				raise TypeError(message)

		"""
		Construct the array of times at which the integration will evaluate, 
		and map the specified function across those times. In the case of 
		sfr or ifr mode, it is specified in Msun yr^-1 and it must be 
		converted to Msun Gyr^-1 (hence the factor of 1e9). 
		"""
		eval_times = __times(output_times[-1] + 10 * self._dt, self._dt)
		ptr = c_double * len(eval_times)
		if self._mode == "gas":
			self.__run.spec = ptr(*list(map(self._func, eval_times)))
		else:
			self.__run.spec = ptr(*list(map(lambda t: 1e9 * self._func(t), 
				eval_times)))

		# Map the mass loading factor across eval_times
		if callable(self._eta):
			eta = list(map(self._eta, eval_times))
		else:
			eta = len(eval_times) * [self._eta]
		# Map the enhancement factor across eval_times 
		if callable(self._enhancement):
			enhancement = list(map(self._enhancement, eval_times))
		else:
			enhancement = len(eval_times) * [self._enhancement]
		# Map the SFE timescale across eval_times
		if callable(self._tau_star):
			tau_star = list(map(self._tau_star, eval_times))
		else:
			tau_star = len(eval_times) * [self._tau_star]

		# Set a custom DTD if specified 
		if callable(self._ria):
			self.__set_ria()
		else:
			pass

		"""
		Pass the mass loading factor, enhancement factor, SFE timescale, and 
		inflow metallicities to C. 
		"""
		self.__model.eta = ptr(*eta[:])
		self.__model.enh = ptr(*enhancement[:])
		self.__model.tau_star = ptr(*tau_star[:])
		self.__set_zin(eval_times)

		# Setup the star formation history for bookkeeping 
		self.__run.mdotstar = ptr(*(len(eval_times) * [0.]))

		"""
		Make sure that the output files aren't overwriting anything the user 
		doesn't want overwritten. 
		"""
		if self.__outfile_check(overwrite):
			if not os.path.exists(self._name):
				os.system("mkdir %s" % (self._name))
			else:
				pass

			# Warn the user about r-process elements and bad solar calibrations 
			self.__nsns_warning()
			self.__solar_z_warning() 

			# Pass the arguments to C and run the integration
			times = ptr(*eval_times[:])
			ptr2 = c_double * len(output_times)
			outtimes = ptr2(*output_times[:])
			enrichment = clib.enrich(byref(self.__run), byref(self.__model), 
				self._name.encode("latin-1"), times, 
				c_long(len(eval_times)), outtimes, c_double(output_times[-1]))

			# Save the yield settings 
			self.__save_yields() 

			# Save the settings 
			self.__save_attributes() 

		else:
			# Can still return an output object if the user wants to capture it 
			enrichment = 0

		if enrichment == 1: 
			# Couldn't open output files
			message = "Couldn't open files under directory: %s\n" % (self._name)
			raise IOError(message)
		elif enrichment == 2:
			# Something went wrong in setting up the DTD 
			message = "Unrecognized SNe Ia delay time distribution: %s" % (
				self._ria)
			raise ValueError(message)
		elif enrichment == 0:
			# Everything went fine 
			if capture:
				return _du.output(self._name[:-5])
			else:
				pass # done
		else:
			# Something went wrong
			message = "Unknown return parameter: %g\n" % (enrichment)
			message += "Please open an issue to submit a bug report at "
			message += "<http://github.com/giganano/VICE.git>."
			raise SystemError(message)

	def __output_times_check(self, output_times):
		"""
		Ensures that the output times have only numerical values above zero. 
		"""

		"""
		First pull a copy to allow compatibility w/NumPy arrays and Pandas 
		DataFrames. 
		"""
		if "numpy" in sys.modules and isinstance(output_times, _np.ndarray):
			output_times = output_times.tolist()
		elif "pandas" in sys.modules and isinstance(output_times, 
			_pd.DataFrame): 
			output_times = [i[0] for i in output_times.values.tolist()]
		else:
			try: 
				output_times = list(output_times)
			except:
				message = "Argument 'output_times' must be an array-like object."
				raise TypeError(message)

		"""
		Sort the output times from least to greatest. The user need not do 
		this themselves. 
		"""
		output_times = sorted(output_times)
		if not all(list(map(lambda x: isinstance(x, numbers.Number), 
			output_times))):
			# Make sure they're all numbers 
			message = "All output times must be numerical values. "
			message += "Non-numerical value detected."
			raise TypeError(message)
		elif not all(list(map(lambda x: x >= 0, output_times))):
			# Make sure they're all non-negative 
			message = "All output times must be non-negative. "
			raise ValueError(message)
		else:
			if output_times[-1] > 15:
				"""
				For reasons relating to the SNe Ia DTD numerical 
				implementation, VICE does not simulate histories longer than 
				15 Gyr. Warn the user that this will likely cause a 
				segmentation fault in the integration. 
				"""
				message = "VICE only determines SNe Ia rate out to 15 Gyr, "
				message += "and therefore does not support integrations over "
				message += "this long of timescales. This integrations will "
				message += "either have numerical errors or produce a "
				message += "segmentation fault at late times."

				warnings.warn(message, UserWarning)
			else:
				pass
			# Return the sorted list 
			return self.__refine_output_times(output_times)
			# return output_times

	def __refine_output_times(self, output_times): 
		"""
		Removes any elements of the user's specified output_times array that 
		are smaller than the timestep size minus 1.e-5. 
		"""
		arr = len(output_times) * [0.] # It will only get smaller 

		n = 0
		for i in range(1, len(output_times)): 
			# If the difference is near or larger than dt 
			if output_times[i] - arr[n] - self._dt >= -1.e-5: 
				arr[n + 1] = output_times[i]
				n += 1
			else:
				# If not, move to the next output time 
				continue 

		return arr[:(n + 1)]

	def __outfile_check(self, overwrite):
		"""
		Determines if any of the output files exist and proceeds according to 
		the user specified overwrite preference.
		"""

		# The names of the output files 
		outfiles = ["%s/%s" % (self._name, 
			i) for i in ["history.out", "mdf.out", "ccsne_yields.config", 
				"sneia_yields.config"]]
		if os.path.exists(self._name):
			# If the output path exists, but the user specified overwrite 
			if overwrite:
				return True
			else:
				"""
				If they didn't specify overwrite, see if either of the output 
				files will overwrite anything. 
				"""
				if any(list(map(os.path.exists, outfiles))):
					# If they do, ask if they'd like to overwrite 
					question = "At least one of the output files already "
					question += "exists. If you continue with the integration, "
					question += "then their contents will be lost.\n"
					question += "Output directory: %s\n" % (self._name)
					question += "Overwrite? (y | n) "
					answer = raw_input(question)

					# Be emphatic about it 
					while answer.lower() not in ["yes", "y", "no", "n"]:
						question = "Please enter either 'y' or 'n': "
						answer = raw_input(question)
					if answer.lower() in ["y", "yes"]:
						# They said overwrite 
						return True
					else:
						# They said don't overwrite 
						return False
				else:
					# Neither output file will overwrite ---> proceed 
					return True
		else:
			# The output directory doesn't even exist ---> proceed 
			return True


	@staticmethod
	def __args(func):
		"""
		Returns True if the function passed to it takes more than one parameter 
		or any keyword/variable/default arguments.
		"""
		if sys.version_info[0] == 2:
			# Python 2.x argspec function 
			args = inspect.getargspec(func)
		elif sys.version_info[0] == 3:
			# Python 3.x argspec function 
			args = inspect.getfullargspec(func)
		else:
			# This should be caught at import anyway 
			_version_error() 

		# Return True only if the function takes exactly one parameter 
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

	def __set_ria(self):
		"""
		Sets a customized SNe Ia DTD 
		"""

		# Pull an array of time in self._dt steps from 0 to 15
		times = __times(15, self._dt)
		ria = len(times) * [0.]
		for i in list(range(len(ria))):
			"""
			Map the specified function across those times and take into account 
			the intrinsic delay from SNe Ia 
			"""
			if times[i] > self._delay:
				if times[i] <= 13.8:
					ria[i] = self._ria(times[i])
				else:
					"""
					Set the DTD to zero after 13.8 Gyr. This is a physically 
					motivated decision ---> thermonuclear detonations of a 
					white dwarf should be largely finished after this much 
					time. 
					"""
					ria[i] = 0
				if (m.isnan(ria[i]) or m.isinf(ria[i]) or ria[i] < 0): 
					# If it ever evaluted to a nan or inf 
					message = "Custom SNe Ia DTD evaluated to negative, nan, "
					message += "or inf for at least one timestep. "
					raise ArithmeticError(message)
				else:
					continue
			else:
				continue

		# Normalize the array 
		norm = sum(ria)
		for i in list(range(len(ria))):
			ria[i] /= norm
		if any(list(map(lambda x: x < 0, ria))):
			# If it ever evaluated to a negative value 
			message = "Custom SNe Ia DTD evaluated to negative value for at "
			message += "least one timestep."
			raise ArithmeticError(message)
		else:
			# Embed it in the C struct 
			ptr = c_double * len(ria)
			self.__model.ria = ptr(*ria[:])

	def __set_zin(self, eval_times):
		"""
		Passes the inflow metallicity information to C.
		"""

		# Initialize a pointer and allocate memory 
		dummy = len(eval_times) * [0.] 
		ptr = c_double * len(dummy) 
		clib.malloc_Zin(self.__run, byref(self.__model)) 

		# If it's just a number, fill the whole array for each element 
		if isinstance(self._zin, float): 
			for i in list(range(len(self._elements))): 
				dummy = len(eval_times) * [self._zin] 
				clib.setup_Zin(byref(self.__model), ptr(*dummy[:]), 
					len(eval_times), i)

		# If it's a function, map it across the eval times for each element 
		elif callable(self._zin) and not isinstance(self._zin, 
			_du._customizable_yield_table): 
			# Case insensitive dataframes in VICE are callable too 
			for i in list(range(len(self._elements))): 
				for j in list(range(len(eval_times))): 
					# Make sure there's no infs or nans along the way
					if (m.isnan(self._zin(eval_times[j])) or 
						m.isinf(self._zin(eval_times[j])) or 
						self._zin(eval_times[j]) < 0): 
						message = "Inflow metallicity evaluated to negative, " 
						message += "nan, or inf for at least one timestep. "
						raise ArithmeticError(message) 
					else:
						dummy[j] = self._zin(eval_times[j]) 
				# If it gets here, everything went fine ---> pass to C 
				clib.setup_Zin(byref(self.__model), ptr(*dummy[:]), 
					len(eval_times), i) 

		# If there's a separate specification for each element
		elif isinstance(self._zin, _du._customizable_yield_table): 
			for i in list(range(len(self._elements))): 
				sym = self._elements[i].lower() 
				if isinstance(self._zin[sym], float): 
					# If the user specified a number for that element 
					dummy = len(eval_times) * [self._zin[sym]]
					clib.setup_Zin(byref(self.__model), ptr(*dummy[:]), 
						len(eval_times), i) 
				elif callable(self._zin[sym]): 
					# If they specified a function for that element 
					for j in list(range(len(eval_times))): 
						# Check for infs and nans along the way 
						if (m.isnan(self._zin[sym](eval_times[j])) or 
							m.isinf(self._zin[sym](eval_times[j])) or 
							self._zin[sym](eval_times[j]) < 0): 
							message = "Inflow metallicity evaluated to "
							message += "negative, nan, or inf for at least "
							message += "one timestep." 
							raise ArithmeticError(message) 
						else:
							dummy[j] = self._zin[sym](eval_times[j]) 
					# If it gets here, everything went fine ---> pass to C 
					clib.setup_Zin(byref(self.__model), ptr(*dummy[:]), 
						len(eval_times), i) 
				else: 
					"""
					Include this as a failsafe ---> should be caught in the 
					zin.setter function anyway
					"""
					raise SystemError("This shouldn't be raised.") 

		else: 
			"""
			Include this as a failsafe ---> should be caught in the 
			zin.setter function anyway
			"""
			raise SystemError("This shouldn't be raised.") 


	def __save_yields(self): 
		"""
		Saves the .config yield files to the output directory. 
		"""

		# Snap a shot of the current yield settings 
		ccsne_yields = len(self._elements) * [None]
		sneia_yields = len(self._elements) * [None]
		for i in range(len(self._elements)): 
			ccsne_yields[i] = _yields.ccsne_yields[self._elements[i]]
			sneia_yields[i] = _yields.sneia_yields[self._elements[i]]

		# Turn them back into dictionaries
		ccsne_yields = dict(zip(self._elements, ccsne_yields))
		sneia_yields = dict(zip(self._elements, sneia_yields))

		# See which lements have functional yields 
		encoded = tuple(filter(lambda x: callable(ccsne_yields[x.lower()]), 
			self._elements))
		if len(encoded) > 0: 
			# If the user has dill, everything will be encoded just fine 
			if "dill" in sys.modules: 
				pass
			else: 
				# Elements will be saved with yield = None
				message = "Encoding functional yields from core-collapse " 
				message += "supernovae along with VICE output requires " 
				message += "the package 'dill' (installable via pip). "
				message += "Yields for the following elements will not be " 
				message += "saved: "
				for i in encoded: 
					message += "%s " % (i)
					ccsne_yields[i.lower()] = None
				# Warn the user and set the yields to None

				warnings.warn(message, UserWarning)
		else:
			pass

		# Pickle the dataframes 
		pickle.dump(ccsne_yields, open("%s/ccsne_yields.config" % (self._name), 
			"wb"))
		pickle.dump(sneia_yields, open("%s/sneia_yields.config" % (self._name), 
			"wb"))

	def __save_attributes(self):
		"""
		Saves the .config file to the output directory containing all of the 
		attributes. 
		"""

		params = {
			"agb_model":			self.agb_model,  
			"bins": 				self.bins, 
			"delay": 				self.delay, 
			"dt": 					self.dt, 
			"ria": 					self.ria, 
			"elements": 			self.elements, 
			"enhancement": 			self.enhancement, 
			"eta": 					self.eta, 
			"func": 				self.func, 
			"imf": 					self.imf, 
			"m_lower": 				self.m_lower, 
			"m_upper": 				self.m_upper, 
			"Mg0":					self.Mg0, 
			"MgSchmidt": 			self.MgSchmidt, 
			"mode": 				self.mode, 
			"name": 				self.name, 
			"recycling": 			self.recycling, 
			"schmidt": 				self.schmidt, 
			"schmidt_index": 		self.schmidt_index, 
			"smoothing": 			self.smoothing, 
			"tau_ia": 				self.tau_ia, 
			"tau_star": 			self.tau_star, 
			"z_solar": 				self.z_solar, 
			"zin": 					self.zin
		}

		if "dill" in sys.modules: 
			# User has dill, pickling functional attributes will go fine 
			pickle.dump(params, open("%s/params.config" % (self._name), "wb")) 
		else: 
			# User doesn't have dill, functional attributes need to be 
			# switched to None before pickling 
			functional = []
			for i in params: 
				if callable(params[i]): 
					params[i] = None 
					functional.append(i)
				else:
					continue 

			# Check for callable functions in the infall metallicity 
			if isinstance(self.zin, dict): 
				# cast a copy of it 
				params["zin"] = dict(self.zin)
				for i in self.zin: 
					if callable(self.zin[i]): 
						params["zin"][i] = None 
						functional.append("zin(%s)" % (i))
					else:
						continue 
			else:
				pass

			message = "Saving functional attributes within VICE output " 
			message += "requires dill (installable via pip). The following "
			message += "functional attributes will not be saved with this " 
			message += "output: "
			for i in functional: 
				message += "%s " % (i) 
			warnings.warn(message, UserWarning)

			pickle.dump(params, open("%s/params.config" % (self._name), "wb"))

	def __nsns_warning(self): 
		"""
		Determines which, if any, of the tracked elements are enriched via the 
		r-process. In this case, VICE raises a warning that these elements will 
		be under-abundant in the simulation. 
		"""
		rprocess = list(filter(lambda x: "NSNS" in _yields.sources[x], 
			self._elements))
		# If anything survived the filter, it comes from the r-process 
		if len(rprocess) > 0: 
			message = "The following elements tracked by this simulation are " 
			message += "believed to be enriched by the r-process: "
			for i in rprocess: 
				message += "%s " % (i) 
			message += "\n"
			message += "In its current version, VICE is not designed to model "
			message += "enrichment via the r-process. These elements will " 
			message += "likely be under-abundant in the output." 
			warnings.warn(message, ScienceWarning) 
		else:
			pass

	def __solar_z_warning(self): 
		"""
		Determines if VICE is about to simulate the enrichment of 
		an element whose solar Z calibration off of Asplund et al. (2009) is 
		not well understood. Raises a warning that the trends should be 
		interpreted as having arbitrary normalization in these cases. 
		""" 
		poorly_calibrated = tuple(["as", "se", "br", "cd", "sb", "te", "i", 
			"cs", "ta", "re", "pt", "hg", "bi"])
		test = list(filter(lambda x: x.lower() in poorly_calibrated, 
			self._elements)) 
		if len(test) > 0: 
			message = "The following elements do not have a well understood " 
			message += "solar abundance: " 
			for i in test: 
				message += "%s " % (i) 
			message += "\n" 
			message += "For this reason, the [X/H] abundances relative to the " 
			message += "sun and all [X/Y] abundance ratios involving these " 
			message += "elements should be interpreted as having an arbitrary "
			message += "normalization." 
			warnings.warn(message, ScienceWarning)
		else:
			pass



#-------------- TYPEDEF STRUCT OBJECTS FOR WRAPPING C-ROUTINES --------------# 
class __model_struct(Structure):

	"""
	The wrapping of the model struct defined in specs.h.

	User access of this class is strongly discouraged.

	See the specs.h file for details on each field. 
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

	See the specs.h file for details on each field. 
	"""

	_fields_ = [
		("symbol", c_char_p), 
		("ccsne_yield", POINTER(c_double)), 
		("sneia_yield", c_double), 
		("agb_grid", POINTER(POINTER(c_double))), 
		("agb_m", POINTER(c_double)), 
		("agb_z", POINTER(c_double)), 
		("num_agb_m", c_long), 
		("num_agb_z", c_long),
		("m_tot", c_double), 
		("solar", c_double)
	]


class __integration_struct(Structure):

	"""
	The wrapping of the integration struct defined in specs.h.

	User access of this class is strongly discouraged.

	See the specs.h file for details on each field. 
	"""

	_fields_ = [
		("out1", c_void_p), 
		("out2", c_void_p), 
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





#--------- A REPLACEMENT TO NUMPY.LINSPACE FOR ANACONDA INDEPENDENCE ---------# 
def __times(stop, dt):
	"""
	Returns the evaluation times given a stopping time and a timestep size
	"""
	arr = (long(stop / dt) + 2) * [0.]
	for i in list(range(len(arr))):
		arr[i] = i * dt
	return arr




