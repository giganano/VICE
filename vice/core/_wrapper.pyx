# cython: language_level=3, boundscheck=False
"""
This file wraps the C subroutines of the single_stellar_population function 
and the singlezone class. Most of the scientific utility of VICE that the user 
interacts with is scripted in this file. 
"""

# Python Functions
from __future__ import (print_function, division, unicode_literals, 
	absolute_import)
from . import _data_utils as _du
from .._globals import _RECOGNIZED_ELEMENTS_
from .._globals import _RECOGNIZED_IMFS_
from .._globals import _VERSION_ERROR_
from .._globals import ScienceWarning
from .._globals import _DEFAULT_FUNC_ 
from .._globals import _DEFAULT_BINS_
from .._globals import _DIRECTORY_
from ._dataframes import atomic_number 
from ._dataframes import solar_z 
from ._dataframes import sources 
from ..yields import ccsne 
from ..yields import sneia 
import math as m
import warnings
import numbers
import inspect
import pickle
import sys
import os
try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 
try:
	# NumPy compatible but not NumPy dependent
	import numpy as _np
except (ImportError, ModuleNotFoundError):
	pass
try:
	# Pandas compatible but not Pandas dependent
	import pandas as _pd
except (ImportError, ModuleNotFoundError):
	pass
try: 
	"""
	dill extends the pickle module and allows functional attributes to be 
	encoded. In later version of python 3, dill.dump must be called instead 
	of pickle.dump. All cases can be taken care of by overriding the native 
	pickle module and letting dill masquerade as pickle. 
	"""
	import dill as pickle 
except (ImportError, ModuleNotFoundError): 
	pass

# C Functions
from ctypes import *
clib = pydll.LoadLibrary("%ssrc/enrichment.so" % (_DIRECTORY_))

__all__ = ["singlezone", "single_stellar_population", "mirror"] 
__all__ = [str(i) for i in __all__] # appease python 2 strings  

if sys.version_info[0] == 2: 
	strcomp = basestring
elif sys.version_info[0] == 3:
	strcomp = str
else:
	_VERSION_ERROR_()



#------------------------------ MIRROR FUNCTION ------------------------------# 
def mirror(output_obj): 
	"""
	Obtain an instance of the vice.singlezone class given only an instance of 
	the vice.output class. The returned singlezone object will have the same 
	parameters as that which produced the output, allowing re-simulation with 
	whatever modifications the user desires. 

	Signature: vice.mirror(output_obj) 

	Parameters 
	========== 
	output_obj :: vice.output 
		Any vice.output object. 

	Returns 
	======= 
	sz :: vice.singlezone 
		A vice.singlezone object with the same attributes as that which 
		produced the given output. 

	Raises 
	====== 
	ImportError :: 
		:: 	The output has encoded functional attributes and the user does not 
			have dill installed 
	UserWarning :: 
		::	The output was produced with functional attributes, but was ran on 
			a system without dill, and they have thus been lost. 

	Notes 
	===== 
	VICE stores attributes of singlezone objects in a pickle within the output 
	directory. Encoding functions along with the rest of the attributes 
	requires the package dill, an extension to pickle which makes this 
	possible. If dill is not installed, these attributes will not be encoded 
	with the output. 

	It is recommended that users install dill in order to make use of these 
	features. It is installable via 'pip install dill'. 

	Example 
	======= 
	>>> out = vice.output("example") 
	>>> new = vice.mirror(out) 
	>>> new.settings() 
	    Current Settings:
	    =================
	    tau_ia ---------> 1.5
	    recycling ------> continuous
	    Z_solar --------> 0.014
	    enhancement ----> 1.0
	    agb_model ------> cristallo11
	    RIa ------------> plaw
	    delay ----------> 0.15
	    IMF ------------> kroupa
	    smoothing ------> 0.0
	    schmidt_index --> 0.5
	    eta ------------> 2.5
	    Zin ------------> 0.0
	    schmidt --------> False
	    elements -------> (u’fe’, u’sr’, u’o’)
	    MgSchmidt ------> 6000000000.0
	    func -----------> <function _DEFAULT_FUNC at 0x1109e06e0> 
	    dt -------------> 0.01
	    tau_star -------> 2.0
	    name -----------> onezonemodel
	    m_lower --------> 0.08
	    m_upper --------> 100.0
	    Mg0 ------------> 6000000000.0
	    mode -----------> ifr
	    bins -----------> [-3, -2.95, -2.9, ... , 0.9, 0.95, 1]
	>>> import numpy as np 
	>>> new.run(np.linspace(0, 10, 1001)) 
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
			"""
			Functional attributes, when stored in a dictionary, come out of a 
			pickle encoded. This means that functional attributes stored in 
			the singlezone.zin attribute will need to be re-wrapped. 
			Fortunately, if they made it through an integrator once and passed 
			the argspec checks, it can be safely assumed that they will again. 
			"""
			if isinstance(params["Zin"], _du.dataframe): 
				for i in params["elements"]: 
					if callable(params["Zin"][i.lower()]): 
						params["Zin"][i.lower()] = __pyfunc_generator(
							params["Zin"][i.lower()]) 
					else:
						continue 
				params["Zin"] = params["Zin"].todict()
			else: 
				pass 

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

			if isinstance(params["Zin"], dict): 
				# check for callable functions in the zin object 
				for i in params["elements"]: 
					if params["Zin"][i.lower()] == None:  
						functional.append("Zin(%s)" % (i))
						copy["Zin"][i.lower()] = 0 
					else:
						copy["Zin"][i.lower()] = params["Zin"][i.lower()] 
				# Cast it back to a list for the integrator 
				copy["Zin"] = [copy["Zin"][i.lower()] for i in copy["elements"]]

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


def __pyfunc_generator(func): 
	"""
	Generates python function which wraps a compiled function in order to 
	unwrap output objects. 

	In a future version of VICE, this may be incorporated into all functional 
	attributes to allow more flexibility. 

	Parameters 
	==========
	func :: <function> 
		The compiled function 

	Returns 
	======= 
	A python function which wraps the compiled function 
	"""
	def pyfunc(t): 
		return func(t) 

	return pyfunc 


#--------------- SINGLE STELLAR POPULATION ENRICHMENT FUNCTION ---------------# 
def single_stellar_population(element, mstar = 1e6, Z = 0.014, time = 10, 
	dt = 0.01, m_upper = 100, m_lower = 0.08, IMF = "kroupa", RIa = "plaw", 
	delay = 0.15, agb_model = "cristallo11"):
	"""
	Simulate the nucleosynthesis of a given element from a single star cluster 
	of given mass and metallicity. This does not take into account galactic 
	evolution - whether or not it is depleted from inflows or ejected in winds 
	is not considered. Only the mass of the given element produced by the star 
	cluster is determined. See section 2.4 of VICE's science documentation at 
	https://github.com/giganano/VICE/tree/master/docs for further details. 

	Signature: vice.single_stellar_population(
		element, 
		mstar = 1.0e+06, 
		Z = 0.014, 
		time = 10, 
		dt = 0.01, 
		m_upper = 100, 
		m_lower = 0.08, 
		IMF = "kroupa", 
		RIa = "plaw", 
		delay = 0.15, 
		agb_model = "cristallo11"
	)

	Parameters 
	========== 
	element :: str [case-insensitive] 
		The symbol of the element to simulate the enrichment for 
	mstar :: real number [default :: 1.0e+06] 
		The birth mass of the star cluster in solar masses. 
	Z :: real number [default :: 0.014] 
		The metallicity by mass of the stars in the cluster. 
		(i.e. Z = mass of metals / total mass) 
	time :: real number [default :: 10] 
		The amount of time in Gyr to run the simulation for 
	dt :: real number [default :: 0.01]
		The size of each timestep in Gyr 
	m_upper :: real number [default :: 100] 
		The upper mass limit on star formation in solar masses. 
	m_lower :: real number [default :: 0.08] 
		The lower mass limit on star formation in solar masses. 
	IMF :: str [case-insensitive] [default :: "kroupa"]
		The stellar initial mass function (IMF) to assume. This must be either 
		"kroupa" (1) or "salpeter" (2). 
	RIa :: str [case-insensitive] or <function> [default :: "plaw"] 
		The delay-time distribution for type Ia supernovae to adopt. VICE will 
		automatically normalize any function that is passed. Alternatively, 
		VICE has built-in distributions: "plaw" (power-law, \\propto t^-1.1) 
		and "exp" (exponential, \\propto e^(-t/1.5 Gyr)). 
	delay :: real number [default :: 0.15] 
		The minimum delay time following the formation of a single stellar 
		population before the onset of type Ia supernovae in Gyr. 
	agb_model :: str [case-insensitive] [default :: "cristallo11"] 
		A keyword denoting which table of nucleosynthetic yields from AGB stars 
		to adopt. 
		Recognized Keywords and their Associated Studies 
		------------------------------------------------
		"cristallo11" :: Cristallo et al. (2011), ApJS, 197, 17 
		"karakas10" :: Karakas (2010), MNRAS, 403, 1413 

	Returns 
	=======
	mass :: list 
		The net mass of the element in solar masses produced by the star 
		cluster at each timestep. 
	times :: list 
		The times in Gyr corresponding to each mass yield. 

	Raises 
	====== 
	ValueError :: 
		::	The element is not built into VICE. 
		::	mstar < 0 
		::	Z < 0 
		::	time < 0 or time > 15 [VICE does not simulate enrichment on 
			timescales longer than the age of the universe] 
		::	dt < 0 
		:: 	m_upper < 0 
		::	m_lower < 0 
		::	m_lower > m_upper 
		::	The IMF is not built into VICE 
		::	delay < 0 
		::	agb_model is not built into VICE 
	LookupError :: 
		::	agb_model == "karakas10" and the atomic number of the element is 
			larger than 29. The Karakas (2010), MNRAS, 403, 1413 study did not 
			report yields for elements heavier than nickel. 
	ArithmeticError :: 
		::	A functional RIa evaluated to a negative value, inf, or NaN at any 
			given timestep. 
	IOError :: [Only occurs if VICE's file structure has been tampered with] 
		::	The AGB yield file is not found. 

	Example 
	======= 
	>>> mass, times = vice.single_stellar_population("sr", Z = 0.008) 
	>>> mass[-1] 
	    0.04808964406448721
	>>> mass, times = vice.single_stellar_population("fe") 
	>>> mass[-1] 
	    2679.816051685778

	References 
	========== 
	Cristallo et al. (2011), ApJS, 197, 17
	(1) Kroupa (2001), MNRAS, 322, 231 
	Karakas (2010), MNRAS, 403, 1413
	(2) Salpeter (1955) ApJ, 121, 161 
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
	if element.lower() not in _RECOGNIZED_ELEMENTS_:
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
	elif IMF.lower() not in _RECOGNIZED_IMFS_:
		raise ValueError("Unrecognized IMF: %s" % (IMF))
	elif delay < 0:
		message = "Keyword arg 'delay' must be non-negative."
		raise ValueError(message)
	elif agb_model.lower() not in studies:
		message = "Unrecognized AGB yield model: %s" % (agb_model)
		message = "See docstring for list of recognized models." 
		raise ValueError(message)
	elif (agb_model.lower() == "karakas10" and 
		atomic_number[element.lower()] > 28):
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
	agbfile = "%syields/agb/%s/%s.dat" % (_DIRECTORY_, 
		agb_model.lower(), element.lower())
	if os.path.exists(agbfile):
		clib.read_agb_grid(byref(r), agbfile.encode("latin-1"), 0)
	else:
		message = "The associated AGB star yield file was not found. "
		message += "Please re-install VICE."
		raise IOError(message)

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
			if isinstance(RIa, strcomp):
				if RIa.lower() == "plaw":
					ria[i] = (ria_times[i] + 1.e-12)**(-1.1)
				elif RIa.lower() == "exp":
					ria[i] = m.exp( -ria_times[i] / 1.5) 
				else:
					raise SystemError("This shouldn't be raised.") 
			elif callable(RIa):
				ria[i] = RIa(ria_times[i]) 
			else:
				raise SystemError("This shouldn't be raised.") 
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
	ccyield = singlezone()._singlezone__setup_ccsne_yield(element)
	ptr = c_double * len(ccyield) 
	clib.fill_cc_yield_grid(byref(r), 0, ptr(*ccyield[:]))

	# Setting the SNe Ia yield is a lot easier with the current version of VICE 
	clib.set_sneia_yield(byref(r), 0, 
		c_double(sneia.settings[element.lower()]))
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
	Runs simulations of chemical enrichment under the single-zone approximation 
	for user-specified parameters. The organizational structure of this class 
	is very simple; every attribute encodes information on a relevant galaxy 
	evolution parameter. 

	Signature: vice.singlezone.__init__(name = "onezonemodel", 
		func = "_DEFAULT_FULC_", 
		mode = "ifr", 
		elements = ("fe", "sr", "o"), 
		IMF = "kroupa", 
		eta = 2.5, 
		ehancement = 1, 
		zin = 0, 
		recycling = "continuous", 
		bins = _DEFAULT_FUNC_, 
		delay = 0.15, 
		RIa = "plaw", 
		Mg0 = 6.0e+09, 
		smoothing = 0.0, 
		tau_ia = 1.5, 
		tau_star = 2.0, 
		dt = 0.01, 
		schmidt = False, 
		schmidt_index = 0.5, 
		MgSchmidt = 6.0e+09, 
		m_upper = 100, 
		m_lower = 0.08, 
		Z_solar = 0.014, 
		agb_model = "cristallo11" 
	)

	Attributes 
	========== 
	name :: str [default :: "onezonemodel"] 
		The name of the simulation. 
	func :: <function> 
		A function of time describing some evolutionary parameter of the 
		galaxy. Interpretation set by the attribute "mode". 
	mode :: str [default :: "ifr"] 
		The interpretation of the attribute "func". Either "ifr" for infall 
		rate, "sfr" for star formation rate, or "gas" for the gas supply. 
	elements :: array-like [default :: ("fe", "sr", "o")] 
		An array-like object of strings denoting the symbols of the elements to 
		track the enrichment for 
	IMF :: str [default :: "kroupa"] 
		A string denoting which stellar initial mass function to adopt. This 
		must be either "kroupa" (1) or "salpeter" (2). 
	eta :: real number [default :: 2.5] 
		The mass-loading parameter - ratio of outflow to star formation rates. 
		This relationship gets more complicated when the attribute smoothing is 
		nonzero. See docstring for further details. 
	enhancement :: real number or <function> [default :: 1] 
		The ratio of outflow to ISM metallicities. If a callable function is 
		passed, it will be interpreted as taking time in Gyr as a parameter. 
	zin :: real number, <function>, or dict [default :: 0] 
		The infall metallicity. See docstring for further details. 
	recycling :: str or real number [default :: "continuous"] 
		Either the string "continuous" or a real number between 0 and 1 
		denoting the treatment of recycling from previous generations of stars. 
	bins :: array-like [default :: [-3.0, -2.95, -2.9, ... , 0.9, 0.95, 1.0]] 
		The binspace within which to sort the normalized stellar metallicity 
		distribution function in each [X/H] abundance and [X/Y] abundance 
		ratio measurement. 
	delay :: real number [default :: 0.15] 
		The minimum delay time in Gyr before the onset of type Ia supernovae 
		associated with a single stellar population 
	RIa :: str or <function> [default :: "plaw"] 
		The delay-time distribution (DTD) to adopt. See docstring for further 
		details. 
	Mg0 :: real number [default :: 6.0e+09] 
		The initial gas supply of the galaxy in solar masses. Only relevant 
		when the simulation is ran in infall mode (i.e. mode == "ifr") 
	smoothing :: real number [default :: 0] 
		The smoothing timescale in Gyr. See docstring for further details. 
	tau_ia :: real number [default :: 1.5] 
		The e-folding timescale of type Ia supernovae in Gyr when ria == "exp". 
	tau_star :: real number or <function> [default :: 2.0] 
		The star formation rate per unit gas mass in the galaxy in Gyr. This 
		can either be a number which will be treated as a constant, or a 
		function of time in Gyr. This becomes the normalization of the star 
		formation efficiency when the attribute schmidt == True. 
	dt :: real number [default :: 0.01] 
		The timestep size in Gyr. 
	schmidt :: bool [default :: False] 
		A boolean switch describing whether or not to implement star formation 
		efficiency dependent on the gas-supply (3; 4). 
	MgSchmidt :: real number [default :: 6.0e+09] 
		The normalization of the gas-supply when attribute schmidt == True. 
	m_upper :: real number [default :: 100] 
		The upper mass limit on star formation in solar masses 
	m_lower :: real number [default :: 0.08] 
		The lower mass limit on star formation in solar masses 
	Z_solar :: real number [default :: 0.014] 
		The adopted solar metallicity by mass. 
	agb_model :: str [default :: "cristallo11"] 
		A keyword denoting which AGB yield grid to adopt. Must be either 
		"cristallo11" (5) or "karakas10" (6). 

	Functions 
	========= 
	run :: 			Run the simulation 
	settings :: 	Print the current settings 

	See also 	[https://github.com/giganano/VICE/tree/master/docs]
	========
	Sections 3 - 6 of science documentation 
	Notes on functional attributes and numerical delta functions in User's 
		guide 

	References 
	========== 
	(5) Cristallo et al. (2011), ApJS, 197, 17 
	(6) Karakas (2010), MNRAS, 403, 1413 
	(1) Kroupa (2001), MNRAS, 322, 231 
	(4) Leroy et al. (2008), AJ, 136, 2782 
	(2) Salpeter (1955), ApJ, 121, 161 
	(3) Schmidt (1959), ApJ, 129, 243 
	"""

	def __init__(self, 
		name = "onezonemodel", 
		func = _DEFAULT_FUNC_, 
		mode = "ifr", 
		elements = ("fe", "sr", "o"), 
		IMF = "kroupa", 
		eta = 2.5, 
		enhancement = 1, 
		Zin = 0, 
		recycling = "continuous", 
		bins = _DEFAULT_BINS_,
		delay = 0.15, 
		RIa = "plaw", 
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
		Z_solar = 0.014, 
		agb_model = "cristallo11"):

		# wrap the C strcuts 
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
		self.IMF = IMF
		self.eta = eta
		self.enhancement = enhancement
		self.Zin = Zin
		self.recycling = recycling
		self.bins = bins
		self.delay = delay
		self.RIa = RIa
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
		self.Z_solar = Z_solar
		self.agb_model = agb_model 

	def __enter__(self): 
		return self 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		return exc_value == None 

	def __del__(self): 
		del self._name 
		del self._func 
		del self._mode 
		del self._elements 
		del self._imf
		del self._eta 
		del self._enhancement 
		del self._zin 
		del self._recycling 
		del self._delay 
		del self._ria 
		del self._Mg0 
		del self._smoothing 
		del self._tau_ia 
		del self._tau_star 
		del self._schmidt 
		del self._schmidt_index 
		del self._MgSchmidt 
		del self._dt 
		del self._m_upper 
		del self._m_lower 
		del self._z_solar 
		del self._agb_model
		del self.__model
		del self.__run

	@property
	def name(self):
		"""
		Type :: str 
		Default :: "onezonemodel" 

		The name of the simulation. The output will be stored in a directory 
		under this name with the extension ".vice". This can also be of the 
		form /path/to/directory/name and the output will be stored there. 

		Notes 
		===== 
		The user need not interact with any of the output files; the output 
		object is designed to read in all of the results automatically. 

		Most of the relevant physical information stored in VICE 
		outputs are in the history.out and mdf.out output files. They are 
		simple ascii text files, allowing users to open them in languages other 
		than python if they so choose. The other output files store the yield 
		settings at the time of simulation and the integrator parameters which 
		produced it. 

		By forcing a ``.vice'' extension on the output file, users can run 
		'<command> *.vice' in a linux terminal to run commands over 
		all vice outputs in a given directory. 		
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

	@name.deleter 
	def name(self): 
		del self._name 

	@property
	def func(self):
		"""
		Type :: <function> 
		Default :: _DEFAULT_FUNC_ 

		A callable python function of time which returns a real number. 
		This must take only one parameter, which will be interpreted as time 
		in Gyr. The value returned by this function will represent either the 
		gas infall history in Msun/yr, the star formation history in Msun/yr, 
		or the gas supply in Msun. 

		The default function returns the value of 9.1 always. With a default 
		mode of "ifr", if these attributes are not changed, the simulation 
		will run with an infall rate of 9.1 Msun/yr at all times. 

		Notes 
		===== 
		Encoding this functional attribute into VICE outputs requires the 
		package 'dill', an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of this parameter. 
		It is recommended that VICE users install dill if they have not already 
		so that they can make use of this feature; this can be done via 
		'pip install dill'. 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 3 of science documentation 
		Notes on functional attributes and numerical delta functions in user's 
			guide 
		Attribute mode 
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
				message = "Attribute 'func' must be a callable function  "
				message += "that takes only one parameter with no variable, "
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

	@func.deleter 
	def func(self): 
		del self._func 

	@property
	def mode(self):
		"""
		Type :: str [case-insensitive] 
		Default :: "ifr" 

		The interpretation of the attribute 'func'. 

		mode = "ifr" 
		------------ 
		The values returned from the attribute func represents the rate of 
		gas infall into the galaxy in Msun/yr. 

		mode = "sfr" 
		------------ 
		The values returned from the attribute func represent the star 
		formation rate in Msun/yr. 

		mode = "gas" 
		------------ 
		The values returned from the attribute func represent the mass of the 
		ISM gas in Msun. 

		Notes 
		===== 
		The attribute func will always be interpreted as taking 
		time in Gyr as a parameter. However, infall and star formation 
		rates will be interpreted as having units of Msun/yr according to 
		convention. 

		See Also 
		======== 
		Section 3.1 of science documentation 
		Attribute func 
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

	@mode.deleter 
	def mode(self): 
		del self._mode 

	@property
	def elements(self):
		"""
		Type :: tuple [elements of type str [case-insensitive]] 
		Default :: ("fe", "sr", "o") 

		The symbols for the elements to track the enrichment for. The more 
		elements that are tracked, the more precisely calibrated is the ISM 
		metallicity at each timestep, but the longer the simulation will take. 

		In its current state, VICE recognizes all 76 astrophysically produced 
		elements between carbon ("c") and bismuth ("bi") 

		Notes
		=====
		The order in which the elements appear in this tuple will dictate the 
		ratios that are quoted in the output stellar metallicity distribution 
		function. That is, if element X appears before element Y, then VICE 
		will determine the MDF in dN/d[Y/X]. 

		See Also 
		======== 
		Section 6 of science documentation 
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
			if i.lower() not in _RECOGNIZED_ELEMENTS_: 
				message = "Unrecognized element: %s" % (i)
				raise ValueError(message)
			else:
				continue

		# Store the copy in the attribute ---> make it a tuple so it's immutable 
		self._elements = tuple(copy[:]) 

	@elements.deleter
	def elements(self): 
		del self._elements 

	@property
	def IMF(self):
		"""
		Type :: str [case-insensitive] 
		Default :: "kroupa" 

		The assumed stellar initial mass function (IMF). This must be either 
		"kroupa" (1) or "salpeter" (2). These IMFs have the following form: 

		"kroupa" 
		-------- 
		dN/dM ~ M^-a 
			a = 2.3 [M > 0.5 Msun] 
			a = 1.3 [0.08 Msun <= M <= 0.5 Msun] 
			a = 0.3 [M < 0.08 Msun] 

		"salpeter" 
		----------
		dN/dM ~ M^-2.35 

		Notes 
		===== 
		A future update to VICE will likely include functionality for a wider 
		sample of IMFs. 

		See Also 
		======== 
		The IMF is relevant in many sections of VICE's science documentation. 

		References
		========== 
		(1) Kroupa (2001), MNRAS, 322, 231 
		(2) Salpeter (1955), ApJ, 121, 161 
		"""
		return self._imf

	@IMF.setter
	def IMF(self, value):
		if isinstance(value, strcomp): 
			# Make sure it's recognized 
			if value.lower() in _RECOGNIZED_IMFS_:
				# Save the copy  
				self._imf = value.lower() 
				self.__model.imf = value.lower().encode("latin-1") 
			else:
				raise ValueError("Unrecognized IMF: %s" % (value))
		else: 
			# If it's not a string it's a TypeError
			message = "Attribute 'IMF' must be of type string. Got: %s" % (
				type(value))
			raise TypeError(message) 

	@IMF.deleter 
	def IMF(self): 
		del self._imf 

	@property
	def eta(self):
		"""
		Type :: real number or <function> 
		Default :: 2.5 

		The mass loading parameter: the ratio of the outflow rate to the star 
		formation rate. 

		Notes 
		===== 
		If the smoothing timescale is nonzero, this relationship is more 
		complicated. See associated docstring for further details. 

		If type <function> 
		------------------ 
		Encoding this functional attribute into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of this parameter. 
		It is recommended that VICE users install dill if they have not already 
		in order to make use of this feature; this can be done via 
		'pip install dill'. 
		
		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 3.2 of science documentation  
		Attribute smoothing 
		Notes on function attributes and numerical delta functions in User's 
			guide 
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
				message += "parameter."
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
				message += "chemical equilibrium (Dalcanton 2007, ApJ, 658, " 
				message += "941." 
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

	@eta.deleter 
	def eta(self): 
		del self._eta 

	@property
	def enhancement(self):
		"""
		Type :: real number or <function> 
		Default :: 1.0 

		The ratio of the outflow to ISM metallicities. This can also be a 
		callable function of time in Gyr. 

		Notes
		===== 
		This multiplicative factor will apply to all elements tracked by the 
		simulation. 

		If type <function> 
		------------------ 
		Encoding this functional attribute into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of this parameter. 
		It is recommended that VICE users install dill if they have not already 
		so that they can make use of this feature; this can be done via 
		'pip install dill'. 

		See Also 
		========
		Sections 3.2 and 4.1 of science documentation 
		Attribute eta 
		Attribute smoothing 
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
				message += "only one parameter."
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

	@enhancement.deleter 
	def enhancement(self): 
		del self._enhancement 

	@property
	def Zin(self):
		"""
		Type :: real number, <function>, or vice.dataframe 
		Default :: 0.0 

		The metallicity of gas inflow. If this is a number or function, it will 
		apply to all elements tracked by the simulation. A python dictionary 
		or VICE dataframe can also be passed, allowing real numbers and 
		functions to be assigned to each individual element. 

		Notes 
		===== 
		The easiest way to switch this attribute to a dataframe is by passing 
		an empty python dictionary (i.e. '{}'). 

		If type <function> 
		------------------ 
		Encoding this functional attribute into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of this parameter. 
		It is recommended that VICE users install dill if they have not already 
		so that they can make use of this feature; this can be done via 
		'pip install dill'. 

		Example 
		======= 
		>>> sz = vice.singlezone(name = "example") 
		>>> sz.Zin = {} 
		>>> sz.Zin
		    vice.dataframe{
		        sr -------------> 0.0 
		        fe -------------> 0.0 
		        o --------------> 0.0 
		    }
		>>> sz.Zin["fe"] = vice.solar_z["fe"] 
		>>> sz.Zin["o"] = lambda t: vice.solar_z["o"] * (t / 10.0) 
		>>> sz.Zin
		    vice.dataframe{
		        sr -------------> 0.0 
		        fe -------------> 0.00129 
		        o --------------> <function <lambda> at 0x115591aa0> 
		    }
		"""
		return self._zin

	@Zin.setter
	def Zin(self, value):
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
				message += "parameter."
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
					if i.lower() in _RECOGNIZED_ELEMENTS_: 
						message = "Element not tracked by current " 
						message += "settings: %s" % (i) 
						raise ValueError(message)
					else:
						message = "Unrecognized element: %s" % (i) 
					raise ValueError(message) 
				# Check to see if they secified a value for this element 
				elif i.lower() in copy.keys(): 
					frame[i.lower()] = copy[i.lower()] 
				# If there's no frame yet, default to zero 
				elif not hasattr(self, "Zin"): 
					frame[i.lower()] = 0.0
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
						message += "exactly one parameter." 
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

	@Zin.deleter 
	def Zin(self): 
		del self._zin 

	@property
	def recycling(self):
		"""
		Type :: real number or str [case-insensitive] 
		Default :: "continuous" 

		The cumulative return fraction r. This is the mass fraction of a 
		single stellar population returned to the ISM as gas at the birth 
		metallicity of the stars. 

		If this attribute is a string, it must be "continuous" 
		[case-insensitive]. In this case VICE will treat recycling from each 
		episode of star formation individually via a treatment of the stellar 
		initial mass function and the remnant mass model of Kalirai et al. 
		(2008). 

		If this attribute is a real number, it must be a value between 0 and 1. 
		VICE will implement instantaneous recycling in this case, and this 
		parameter will represent the fraction of a single stellar population's 
		mass that is returned instantaneously the ISM. 

		Notes 
		===== 
		It is recommended that user's adopt r = 0.4 (0.2) if they desire 
		instantaneous recycling with a Kroupa (1) (Salpeter (2)) IMF, based 
		on the analytical model of Weinberg, Andrews & Freudenburg (2017). 

		See Also 	[https://github.com/giganano/VICE/tree/master/docs]
		======== 
		Section 3.3 of science documentation 

		Example 
		======= 
		>>> sz = vice.singlezone(name = "example") 
		>>> sz.recycling = 0.4 
		>>> sz.imf = "salpeter" 
		>>> sz.recycling = 0.2 

		References 
		========== 
		Kalirai et al (2008), ApJ, 676, 594 
		(1) Kroupa (2001), MNRAS, 322, 231 
		(2) Salpeter (1955), ApJ, 131, 161 
		Weinberg, Andrews & Freudenburg (2017), ApJ, 837, 183 
		"""
		return self._recycling

	@recycling.setter
	def recycling(self, value):
		if isinstance(value, numbers.Number):
			# The cumulative return fraction is by definition between 0 and 1 ... 
			if 0 <= value <= 1: 
				self.__recycling_warnings(value) 
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

	@recycling.deleter 
	def recycling(self): 
		del self._recycling 

	def __recycling_warnings(self, value): 
		"""
		Raises a ScienceWarning if the instananeous recycling parameter is 
		significantly different from that derived in WAF17. 
		"""
		if isinstance(value, numbers.Number) and 0 <= value <= 1: 
			"""
			Check for > 10% deviations from WAF17. 
			"""	
			if self._imf == "kroupa": 
				if value <= 0.36 or value >= 0.44: 
					message = "Weinberg, Andrews & Freudenburg (2017), ApJ, "
					message += "837, 183 recommend an instantaneous recycling " 
					message += "parameter of r = 0.4 for a Kroupa IMF. Got "
					message += "value with a >10%  discrepancy from this "
					message += "value: %g" % (value) 
					warnings.warn(message, ScienceWarning) 
				else: 
					pass 
			elif self._imf == "salpeter": 
				if value <= 0.18 or value >= 0.22: 
					message = "Weinberg, Andrews & Freudenburg (2017), ApJ, "
					message += "837, 183 recommend an instantaneous recycling " 
					message += "parameter of r = 0.2 for a Salpeter IMF. Got "
					message += "value with a >10%  discrepancy from this "
					message += "value: %g" % (value) 
					warnings.warn(message, ScienceWarning) 
				else: 
					pass 
			else: 
				# failsafe 
				raise SystemError("This should be raised.")  

	@property
	def bins(self):
		"""
		Type :: array-like [elements are real numbers] 
		Default :: [-3, -2.95, -2.9, ... , 0.9, 0.95, 1.0] 

		The bins in each [X/H] abundance and [X/Y] abundance ratio to sort the 
		normalized stellar metallicity distribution function into. By default, 
		VICE sorts everything into 0.05-dex width bins between [X/H] and 
		[X/Y] = -3 and +1. 

		Notes 
		===== 
		This attribute is compatible with the NumPy array and Pandas DataFrame, 
		but is not dependent on either package. 

		See Also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 6 of science documentation 
		"""
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

	@bins.deleter 
	def bins(self): 
		del self.__model.bins 
		del self.__model.num_bins 

	@property
	def delay(self):
		"""
		Type :: real number 
		Default :: 0.15 

		The minimum delay time in Gyr for the onset of type Ia supernovae 
		associated with a single stellar population. The default parameter 
		is adopted from Weinberg, Andrews & Freudenburg (2017).  

		See Also 	[https://github.com/giganano/VICE/tree/master/docs]
		======== 
		Attribute ria 
		Section 4.3 of science documentation 

		References 
		========== 
		Weinberg, Andrews & Freudenburg (2017), ApJ, 837, 183 
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

	@delay.deleter 
	def delay(self): 
		del self._delay 

	@property
	def RIa(self):
		"""
		Type :: <function> or str [case-insensitive] 
		Default :: "plaw" 

		The delay-time distribution (DTD) for type Ia supernovae to adopt. If 
		type str, VICE will use built-in DTDs: 
			"exp"
			----- 
			RIa ~ e^-t  [e-folding timescale set by attribute tau_ia] 

			"plaw"
			------
			RIa ~ t^-1.1 

		Alternatively, the user may pass their own function of time in Gyr, 
		and the normalization of the custom DTD will be taken care of 
		automatically. 

		If type <function> 
		------------------ 
		Encoding this functional attribute into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of this parameter. 
		It is recommended that VICE users install dill if they have not already 
		so that they can make use of this feature; this can be done via 
		'pip install dill'. 

		See also [https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 4.3 of science documentation 
		Note on functional attributes and numerical delta functions in user's 
			guide 
		"""
		return self._ria

	@RIa.setter
	def RIa(self, value):
		if callable(value):
			"""
			Allow functionality for user-specified delay-time distributions. 
			As usual, the specified function must take only one parameter, 
			which will be interpreted as time in Gyr. 
			"""
			if self.__args(value):
				message = "When callable, attribute 'RIa' must take only "
				message += "one parameter."
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

	@RIa.deleter 
	def RIa(self): 
		del self._ria 

	@property
	def Mg0(self):
		"""
		Type :: real number 
		Default :: 6.0e+09 

		The mass of the ISM gas at time t = 0 in solar masses. 

		Notes 
		===== 
		This parameter only matters when the simulation is in infall mode (i.e. 
		mode = "ifr"). In gas mode, func(0) specifies the initial gas supply, 
		and in star formation mode, it is func(0) * tau_star(0) (modulo the 
		prefactors imposed by gas-dependent star formation efficiency, if 
		applicable). 
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

	@Mg0.deleter 
	def Mg0(self): 
		del self._Mg0 

	@property
	def smoothing(self):
		"""
		Type :: real number 
		Default :: 0.0 

		The smoothing time in Gyr to adopt. This is the timescale on which the 
		star formation rate is time-averaged before determining the outflow 
		rate via the mass loading parameter (attribute eta). For an outflow 
		rate (OFR) and star formation rate (SFR) with smoothing time s: 

		OFR = eta * <SFR>_s

		The traditional relationship of OFR = eta * SFR is recovered when the 
		user specifies a smoothing time that is smaller than the timestep size.  

		Notes 
		===== 
		While this parameter time-averages the star formation rate, it does 
		NOT time-average the mass-loading parameter. 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 3.2 of science documentation 
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

	@smoothing.deleter 
	def smoothing(self): 
		del self._smoothing 

	@property
	def tau_ia(self):
		"""
		Type :: real number 
		Default :: 1.5 

		The e-folding timescale in Gyr of an exponentially decaying delay-time 
		distribution for type Ia supernovae. 

		Notes 
		===== 
		Because this is an e-folding timescale, it only matters when the 
		attribute ria = "exp". 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 4.3 of science documentation 
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

	@tau_ia.deleter 
	def tau_ia(self): 
		del self._tau_ia 

	@property
	def tau_star(self):
		"""
		Type :: real number or <function> 
		Default :: 2.0 

		The star formation rate per unit gas supply in Gyr (Mgas / SFR). In 
		observational journal articles, this is sometimes referred to as the 
		"depletion time". This parameter is how the gas supply and star 
		formation rate are determined off of one another at each timestep. 

		Notes 
		===== 
		When attribute schmidt = True, this is interpreted as the prefactor 
		on gas-dependent star formation efficiency. 

		If type <function> 
		------------------ 
		Encoding this functional attribute into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of this parameter. 
		It is recommended that VICE users install dill if they have not already 
		so that they can make use of this feature; this can be done via 
		'pip install dill'. 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 3.1 of science documentation 
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

	@tau_star.deleter 
	def tau_star(self): 
		del self._tau_star 

	@property
	def dt(self):
		"""
		Type :: real number 
		Default :: 0.01 

		The timestep size in Gyr to use in the integration.

		Notes 
		===== 
		For fine timesteps with a given ending time in the simulation, this 
		affects the total integration time with a dt^-2 dependence. 
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

	@dt.deleter 
	def dt(self): 
		del self._dt 

	@property
	def schmidt(self):
		"""
		Type :: bool 
		Default :: False 

		A boolean describing whether or not to use an implementation of 
		gas-dependent star formation efficiency (i.e. the Kennicutt-Schmidt 
		Law: Schmidt (1959); Leroy et al. (2008)). At each timestep, the 
		attributes tau_star, MgSchmidt, and schmidt_index determine the 
		star formation efficiency at that timestep via: 

		SFE = tau_star(t)^-1 (Mgas / MgSchmidt)^schmidt_index 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 3.1 of science documentation 

		References 
		========== 
		Schmidt (1959), ApJ, 129, 243 
		Leroy et al. (2008), AJ, 136, 2782 
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

	@schmidt.deleter 
	def schmidt(self): 
		del self._schmidt 

	@property
	def schmidt_index(self):
		"""
		Type :: real number 
		Default :: 0.5 

		The power-law index on gas-dependent star formation efficiency.

		See also 	[https://github.com/giganano/VICE/tree/master/docs]
		======== 
		Section 3.1 of science documentation
		Attribute schmidt 
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

	@schmidt_index.deleter 
	def schmidt_index(self): 
		del self._schmidt_index 

	@property
	def MgSchmidt(self):
		"""
		Type :: real number 
		Default :: 6.0e+09 

		The normalization of the gas supply when star formation efficiency is 
		dependent on the gas supply. 

		Notes 
		===== 
		In practice, this quantity should be comparable to a typical gas supply 
		of the simulated galaxy so that the actual star formation efficiency at 
		a given timestep is near the user-specified value. 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 3.1 of science documentation 
		Attribute schmidt 
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

	@MgSchmidt.deleter 
	def MgSchmidt(self): 
		del self._MgSchmidt 

	@property
	def m_upper(self):
		"""
		Type :: real number 
		Default :: 100 

		The upper mass limit on star formation in solar masses. 
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

	@m_upper.deleter 
	def m_upper(self): 
		del self._m_upper 

	@property
	def m_lower(self):
		"""
		Type :: real number 
		Default :: 0.08 

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

	@m_lower.deleter 
	def m_lower(self): 
		del self._m_lower 

	@property
	def Z_solar(self):
		"""
		Type :: real number 
		Default :: 0.014 (Asplund et al. 2009) 

		The metallicity by mass of the sun. This is used in calibrating the 
		total metallicity of the ISM, which is necessary when there are only a 
		few elements tracked by the simulation. 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 5.4 of science documentation 

		References 
		========== 
		Asplund et al. (2009), ARA&A, 47, 481 
		""" 
		return self._z_solar

	@Z_solar.setter
	def Z_solar(self, value):
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

	@Z_solar.deleter 
	def Z_solar(self): 
		del self._z_solar 

	@property
	def agb_model(self):
		"""
		Type :: str [case-insensitive] 
		Default :: "cristallo11"

		A keyword denoting which stellar mass-metallicity grid of fractional 
		nucleosynthetic yields from asymptotic giant branch stars to adopt 
		in the simulation. 

		Recognized Keywords and their Associated Studies 
		------------------------------------------------ 
		cristallo11:		Cristallo et al. (2011), ApJS, 197, 17
		karakas10:			Karakas (2010), MNRAS, 403, 1413

		Notes 
		===== 
		If the Karakas (2010) set of yields are adopted and any elements 
		tracked by the simulation are heavier than nickel, a LookupError will 
		be raised. The Karakas (2010) study did not report yields for elements 
		heavier than nickel. 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Sections 4.4 and 5.3 of science documentation 
		"""
		return self._agb_model

	@agb_model.setter
	def agb_model(self, value):
		# The recognized AGB yield studies 
		recognized = ["cristallo11", "karakas10"] 
		if any(list(map(lambda x: atomic_number[x] > 28, 
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

	@agb_model.deleter 
	def agb_model(self): 
		del self._agb_model 

	def settings(self):
		"""
		Prints the current parameters of the simulation to the screen. 
		"""
		frame = {}
		frame["name"] = self._name[:-5]
		frame["func"] = self._func
		frame["mode"] = self._mode 
		frame["IMF"] = self._imf 
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
		frame["RIa"] = self._ria
		frame["Mg0"] = self._Mg0
		frame["smoothing"] = self._smoothing
		frame["tau_ia"] = self._tau_ia 
		frame["tau_star"] = self._tau_star 
		frame["dt"] = self._dt 
		frame["schmidt"] = self._schmidt 
		frame["schmidt_index"] = self._schmidt_index 
		frame["MgSchmidt"] = self._MgSchmidt 
		frame["Zin"] = self._zin
		frame["m_upper"] = self._m_upper 
		frame["m_lower"] = self._m_lower 
		frame["Z_solar"] = self._z_solar
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
		Run's the built-in timestep integration routines over the parameters 
		built into the attributes of this class. Whether or not the user sets 
		capture = True, the output files will be produced and can be read into 
		an output object at any time. 

		Signature: vice.singlezone.run(output_times, capture = False, 
			overwrite = False) 

		Parameters 
		========== 
		output_times :: array-like [elements are real numbers] 
			The times in Gyr at which VICE should record output from the 
			simulation. These need not be sorted in any way; VICE will take 
			care of that automatically. 
		capture :: bool [default :: False] 
			A boolean describing whether or not to return an output object 
			from the results of the simulation. 
		overwrite :: bool [default :: False] 
			A boolean describing whether or not to force overwrite any existing 
			files under the same name as this simulation's output files. 

		Returns 
		======= 
		out :: output [only returned if capture = True] 
			An output object produced from this simulation's output. 

		Raises 
		====== 
		TypeError :: 
			::	Any functional attribute evaluates to a non-numerical value 
				at any timestep 
		ValueError :: 
			::	Any element of output_times is negative 
			:: 	An inflow metallicity evaluates to a negative value 
		ArithmeticError :: 
			::	An inflow metallicity evaluates to NaN or inf 
			::	Any functional attribute evaluates to NaN or inf at any 
				timestep 
		UserWarning :: 
			::	Any yield settings or class attributes are callable 
				functions and the user does not have dill installed 
		ScienceWarning :: 
			::	Any element tracked by the simulation is enriched in 
				significant part by the r-process 
			::	Any element tracked by the simulation has a weakly constrained 
				solar abundance measurement 

		Notes
		=====
		Encoding functional attributes into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of any functional 
		attributes stored in this class. It is recommended that VICE users 
		install dill if they have not already so that they can make use of this 
		feature; this can be done via 'pip install dill'. 

		When overwrite = False, and there are files under the same name as the 
		output produced, this acts as a halting function. VICE will wait for 
		the user's approval to overwrite existing files in this case. If 
		user's are running multiple simulations and need their integrations 
		not to stall, they must specify overwrite = True. 

		Example 
		======= 
		>>> import numpy as np 
		>>> sz = vice.singlezone(name = "example") 
		>>> outtimes = np.linspace(0, 10, 1001) 
		>>> sz.run(outtimes) 
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
		solars = [solar_z[i] for i in self._elements]
		solars = ptr(*solars[:])
		clib.setup_elements(byref(self.__run), syms, solars)

		"""
		Setup each element's AGB yield grid, SNe Ia yield, and CCSNe yield. 
		This for-loop pulls all of the user's presets. 
		"""
		for i in list(range(len(self._elements))):
			# AGB yield grids are stored in files 
			agbfile = ("%syields/agb/%s/%s.dat" % (_DIRECTORY_, 
				self._agb_model.lower(), 
				self._elements[i].lower())).encode("latin-1")
			clib.read_agb_grid(byref(self.__run), agbfile, i)
			
			"""
			Under the current version of VICE, SNe Ia yields can only be 
			numbers. 
			"""
			sneia_yield = sneia.settings[self._elements[i]]
			clib.set_sneia_yield(byref(self.__run), i, c_double(sneia_yield))
			
			# CCSNe yields, however, can be functions of metallicity Z 
			ccyield = self.__setup_ccsne_yield(self._elements[i])
			ptr = c_double * len(ccyield)
			clib.fill_cc_yield_grid(byref(self.__run), i, ptr(*ccyield[:]))

		"""
		Construct the array of times at which the integration will evaluate, 
		and map the specified function across those times. In the case of 
		sfr or ifr mode, it is specified in Msun yr^-1 and it must be 
		converted to Msun Gyr^-1 (hence the factor of 1e9). 
		"""
		eval_times = __times(output_times[-1] + 10 * self._dt, self._dt)
		ptr = c_double * len(eval_times)
		if self._mode == "gas": 
			spec = list(map(self._func, eval_times)) 
		else:
			spec = list(map(lambda t: 1.e9 * self._func(t), eval_times)) 
		self.__numeric_check(spec, "func")  
		self.__run.spec = ptr(*spec[:]) 

		# Map the mass loading factor across eval_times
		if callable(self._eta):
			eta = list(map(self._eta, eval_times)) 
			self.__numeric_check(eta, "eta") 
		else:
			eta = len(eval_times) * [self._eta]
		# Map the enhancement factor across eval_times 
		if callable(self._enhancement):
			enhancement = list(map(self._enhancement, eval_times)) 
			self.__numeric_check(enhancement, "enhancement") 
		else:
			enhancement = len(eval_times) * [self._enhancement]
		# Map the SFE timescale across eval_times
		if callable(self._tau_star):
			tau_star = list(map(self._tau_star, eval_times)) 
			self.__numeric_check(tau_star, "tau_star") 
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
			output_times = sorted(output_times)
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


	def __setup_ccsne_yield(self, element): 
		"""
		Allow CCSNe yields to be functions of metallicity Z
		"""
		ccyield = ccsne.settings[element]
		if callable(ccyield): 
			if self.__args(ccyield): 
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
				arr = list(map(ccyield, z_arr)) 

				# Check for Type- and ValueErrors in the mapped function 
				if not all(list(map(lambda x: isinstance(x, numbers.Number), 
					arr))): 
					message = "Yield as a function of metallicity mapped "
					message += "to non-numerical value." 
					raise ArithmeticError(message) 
				elif any(list(map(lambda x: m.isnan(x) or m.isinf(x), arr))): 
					message = "Yield as a function of metallicity mapped to " 
					message += "NaN or inf for at least one metallicity." 
					raise ArithmeticError(message) 
				else:
					# Allow all numerical values, even negative values
					return arr
		elif isinstance(ccyield, numbers.Number): 
			# Allow all values, even negative values 
			return len(__times(0.5 + 1.e-5, 1.e-5)) * [ccyield]
		else:
			# Otherwise it's a TypeError 
			message = "IMF-integrated yield from core collapse supernovae "
			message += "must be either a numerical value or a function "
			message += "of metallicity."
			raise TypeError(message)


	def __outfile_check(self, overwrite):
		"""
		Determines if any of the output files exist and proceeds according to 
		the user specified overwrite preference.
		"""

		# The names of the output files 
		outfiles = ["%s/%s" % (self._name, 
			i) for i in ["history.out", "mdf.out", "ccsne_yields.config", 
				"sneia_yields.config", "params.config"]]
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

		All functional attributes in this software take a numerical value as 
		the only parameter, so this is done with a simple try statement that 
		passes the value of 1. This allows pre-compiled code to run. 
		"""
		x = False
		try: 
			foo = func(1) 
		except TypeError: 
			x = True 
		return x

	@staticmethod
	def __numeric_check(arr, name): 
		"""
		Determines if a given array has all numerical valus in it and raises a 
		TypeError if it doesn't. 

		Parameters 
		========== 
		arr :: array-like 
			The array to check 
		name :: string 
			The name of the object (for raising the TypeError). 
		"""
		if not all(list(map(lambda x: isinstance(x, numbers.Number), arr))): 
			message = "Functional attribute %s evaluated to non-numerical " % (
				name)
			message += "value." 
			raise TypeError(message) 
		elif any(list(map(lambda x: m.isinf(x) or m.isnan(x), arr))): 
			message = "Functional attribute %s evaluated to inf or NaN." % (
				name) 
			raise ArithmeticError(message) 
		else: 
			pass

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
						m.isinf(self._zin(eval_times[j]))): 
						message = "Inflow metallicity evaluated to NaN or inf " 
						message += "for at least one timestep." 
						raise ArithmeticError(message) 
					elif self._zin(eval_times[j]) < 0: 
						message = "Inflow metallicity evaluated to negative " 
						message += "value for at least one timestep." 
						raise ValueError(message)
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
							m.isinf(self._zin[sym](eval_times[j]))): 
							message = "Inflow metallicity evaluated to NaN or " 
							message += "inf for at least one timestep." 
							raise ArithmeticError(message) 
						elif self._zin[sym](eval_times[j]) < 0: 
							message = "Inflow metallicity evaluated to " 
							message += "negative value for at least one " 
							message += "timestep." 
							raise ValueError(message)
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
			ccsne_yields[i] = ccsne.settings[self._elements[i]]
			sneia_yields[i] = sneia.settings[self._elements[i]]

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
			"RIa": 					self.RIa, 
			"elements": 			self.elements, 
			"enhancement": 			self.enhancement, 
			"eta": 					self.eta, 
			"func": 				self.func, 
			"IMF": 					self.IMF, 
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
			"Z_solar": 				self.Z_solar, 
			"Zin": 					self.Zin
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
			if isinstance(self.Zin, dict): 
				# cast a copy of it 
				params["zin"] = dict(self.Zin)
				for i in self.Zin: 
					if callable(self.Zin[i]): 
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
		rprocess = list(filter(lambda x: "NSNS" in sources[x], 
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




