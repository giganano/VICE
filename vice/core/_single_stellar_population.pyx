# cython: language_level = 3, boundscheck = False
"""
This file wraps the C subroutines of the single_stellar_population 
function, the main_sequence_mass_fraction function, and the 
cumulative_return_fraction function. 
""" 

from __future__ import absolute_import 

__all__ = ["single_stellar_population", "cumulative_return_fraction", 
	"main_sequence_mass_fraction"] 

# Python functions 
from .._globals import _DIRECTORY_ 
from .._globals import _RECOGNIZED_ELEMENTS_ 
from .._globals import _RECOGNIZED_IMFS_ 
from .._globals import _RECOGNIZED_RIAS_ 
from .._globals import _VERSION_ERROR_ 
from ..core._builtin_dataframes import atomic_number 
from ..yields.agb._grid_reader import find_yield_file as find_agb_yield_file 
from ..yields import agb 
from ..yields import sneia 
from ..yields import ccsne 
from . import _pyutils 
import math as m 
import numbers 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 

# C Functions 
from libc.stdlib cimport malloc, free 
from ._objects cimport SSP, ELEMENT 
from . cimport _agb 
from . cimport _ccsne 
from . cimport _cutils 
from . cimport _element 
from . cimport _io 
from . cimport _sneia 
from . cimport _ssp 

# ------------------- CUMULATIVE RETURN FRACTION FUNCTION ------------------- # 
def cumulative_return_fraction(age, IMF = "kroupa", m_upper = 100, 
	m_lower = 0.08): 
	"""
	Determine the cumulative return fraction for a single stellar population 
	at a given age. This quantity represents the fraction of the stellar 
	population's mass that is returned to the ISM as gas at the birth 
	metallicity of the stars. See section 2.2 of VICE's science documentation 
	at https://github.com/giganano/VICE/tree/master/docs for further details. 

	Signature: vice.cumulative_return_fraction(age, 
		IMF = "kroupa", 
		m_upper = 100, 
		m_lower = 0.08)

	Parameters 
	========== 
	age :: real number 
		The age of the stellar population in Gyr 
	IMF :: string [default :: "kroupa"] [case-insensitive] 
		The stellar initial mass function (IMF) to assume. This must be either 
		"kroupa" (1) or "salpeter" (2). 
	m_upper :: real number [default :: 100] 
		The upper mass limit on star formation in solar masses 
	m_lower :: real number [default :: 0.08] 
		The lower mass limit on star formation in solar masses 

	Returns 
	======= 
	crf :: real number 
		The value of the cumulative return fraction for a stellar population 
		at the specified age under the specified parameters. 

	Raises 
	====== 
	TypeError :: 
		:: age is not a real number 
		:: IMF is not of type string 
		:: m_upper is not a real number 
		:: m_lower is not a real number 
	ValueError :: 
		:: age < 0 
		:: IMF is not recognized 
		:: m_upper <= 0 
		:: m_lower <= 0 
		:: m_lower >= m_upper 

	Notes 
	===== 
	VICE operates under the approximation that stars have a mass-luminosity 
	relationship of L ~ M^4.5, leading to a mass-lifetime relation that is 
	also a power law of t ~ M/L ~ M^-3.5. 

	VICE implements the remnant mass model of Kalirai et al. (2008), assuming 
	that (on average) stars above 8 Msun leave behind remnants of 1.44 Msun, 
	while stars below 8 Musn leave behind remnants of 0.394Msun + 0.109M. 

	Example 
	======= 
	>>> vice.cumulative_return_fraction(1) 
	0.3560160079575864
	>>> vice.cumulative_return_fraction(2) 
	0.38056657042902253
	>>> vice.cumulative_return_fraction(3) 
	0.394760119115021 

	References 
	========== 
	Kalirai et al. (2008), ApJ, 676, 594 
	(1) Kroupa (2001), MNRAS, 231, 322 
	(2) Salpeter (1955), ApJ, 121, 161 
	"""
	# Type and Value checks first 
	if not isinstance(age, numbers.Number): 
		raise TypeError("First argument must be a numerical value. Got: %s" % (
			type(age))) 
	elif age < 0: 
		raise ValueError("First argument must be non-negative.") 
	else: 
		__numeric_checker(m_upper, "m_upper") 
		__numeric_checker(m_lower, "m_lower") 
		__msmf_crf_value_checking(IMF = IMF, m_upper = m_upper, 
			m_lower = m_lower) 

	# necessary for the C subroutines 
	cdef SSP *ssp = _ssp.ssp_initialize() 
	_cutils.set_string(ssp[0].imf, IMF.lower()) 
	ssp[0].m_upper = m_upper 
	ssp[0].m_lower = m_lower 

	try: 
		x = _ssp.CRF(ssp[0], age) 
	finally: 
		# always free the memory 
		_ssp.ssp_free(ssp) 
	return x 


# ------------------ MAIN SEQUENCE MASS FRACTION FUNCTION ------------------ # 
def main_sequence_mass_fraction(age, IMF = "kroupa", m_upper = 100, 
	m_lower = 0.08): 	
	"""
	Determine the main sequence mass fraction for a single stellar population 
	at a given age. This quantity represents the fraction of the stellar 
	population's mass that is still in the form of stars on the main sequence. 
	See section 2.3 of VICE's science documentation at 
	https://github.com/giganano/VICE/tree/master/docs for further details. 

	Signature: vice.main_sequence_mass_fraction(age, 
		IMF = "kroupa", 
		m_upper = 100, 
		m_lower = 0.08)

	Parameters 
	========== 
	age :: real number 
		The age of the stellar population in Gyr 
	IMF :: string [default :: "kroupa"] [case-insensitive] 
		The stellar initial mass function (IMF) to assume. This must be either 
		"kroupa" (1) or "salpeter" (2). 
	m_upper :: real number [default :: 100] 
		The upper mass limit on star formation in solar masses 
	m_lower :: real number [default :: 0.08] 
		The lower mass limit on star formation in solar masses 

	Returns 
	======= 
	msmf :: real number 
		The value of the main sequence mass fraction for a stellar population 
		at the specified age under the specified parameters. 

	Raises 
	====== 
	TypeError :: 
		:: age is not a real number 
		:: IMF is not of type string 
		:: m_upper is not a real number 
		:: m_lower is not a real number 
	ValueError :: 
		:: age < 0 
		:: IMF is not recognized 
		:: m_upper <= 0 
		:: m_lower <= 0 
		:: m_lower >= m_upper 

	Notes 
	===== 
	VICE operates under the approximation that stars have a mass-luminosity 
	relationship of M ~ L^4.5, leading to a mass-lifetime relation that is 
	also a power law of t ~ M/L ~ M^-3.5. 

	Example 
	======= 
	>>> vice.main_sequence_mass_fraction(1) 
	0.5815004968281556
	>>> vice.main_sequence_mass_fraction(2) 
	0.5445877675278488
	>>> vice.main_sequence_mass_fraction(3) 
	0.5219564300200146

	References 
	========== 
	(1) Kroupa (2001), MNRAS, 231, 322 
	(2) Salpeter (1955), ApJ, 121, 161 
	"""
	# Type and value checks first 
	if not isinstance(age, numbers.Number): 
		raise TypeError("First argument must be a numerical value. Got: %s" % (
			type(age))) 
	elif age < 0: 
		raise ValueError("First argument must be non-negative.") 
	else: 
		__numeric_checker(m_upper, "m_upper") 
		__numeric_checker(m_lower, "m_lower") 	
		__msmf_crf_value_checking(IMF = IMF, m_upper = m_upper, 
			m_lower = m_lower) 

	# necessary for C subroutines 
	cdef SSP *ssp = _ssp.ssp_initialize() 
	_cutils.set_string(ssp[0].imf, IMF.lower()) 
	ssp[0].m_upper = m_upper 
	ssp[0].m_lower = m_lower 

	try: 
		x = _ssp.MSMF(ssp[0], age) 
	finally: 
		# always free the memory 
		_ssp.ssp_free(ssp) 
	return x 


def __msmf_crf_value_checking(IMF = "kroupa", m_upper = 100, m_lower = 0.08): 
	if IMF.lower() not in _RECOGNIZED_IMFS_: 
		raise ValueError("Unrecognized IMF: %s" % (IMF)) 
	elif m_upper <= 0: 
		raise ValueError("Keyword arg 'm_upper' must be greater than zero.") 
	elif m_lower <= 0: 
		raise ValueError("Keyword arg 'm_lower' must be greater than zero.") 
	elif m_lower >= m_upper: 
		raise ValueError("Keyword arg 'm_upper' must be larger than 'm_lower'.") 
	else: 
		pass 


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
	# Type and value checks first 
	kwargs = {
		"mstar": 		mstar, 
		"Z": 			Z, 
		"time": 		time, 
		"dt": 			dt, 
		"m_upper": 		m_upper, 
		"m_lower": 		m_lower, 
		"IMF": 			IMF, 
		"RIa": 			RIa, 
		"delay": 		delay, 
		"agb_model": 	agb_model
	} 
	__ssp_type_checking(element, **kwargs) 
	__ssp_value_checking(element, **kwargs) 

	# Necessary C structs for calling _ssp.single_population_enrichment
	cdef SSP *ssp = _ssp.ssp_initialize() 
	cdef ELEMENT *e = _element.element_initialize() 
	_cutils.set_string(ssp[0].imf, IMF.lower()) 
	ssp[0].m_upper = m_upper 
	ssp[0].m_lower = m_lower 

	# Import the element's AGB yield grid 
	agbfile = find_agb_yield_file(element, agb_model) 
	if os.path.exists(agbfile): 
		if _io.import_agb_grid(e, agbfile.encode("latin-1")): 
			raise IOError("Failed to read AGB yield file.") 
		else: 
			pass 
	else: 
		raise IOError("AGB yield file not found. Please re-install VICE.") 

	# Setup the SNe Ia yield
	e[0].sneia_yields[0].yield_ = sneia.settings[element.lower()] 
	if isinstance(ccsne.settings[element.lower()], numbers.Number): 
		# constant core-collapse yield -> fill the yield grid w/that value  
		length = int((_ccsne.CC_YIELD_GRID_MAX - 
			_ccsne.CC_YIELD_GRID_MIN) / _ccsne.CC_YIELD_STEP) + 1 
		e[0].ccsne_yields[0].yield_ = _cutils.copy_pylist(
			length * [ccsne.settings[element.lower()]])  
	elif callable(ccsne.settings[element.lower()]): 
		# functional core-collapse yield -> map it across the yield grid 
		_pyutils.args(ccsne.settings[element.lower()], 
			"Functional yield must take only one numerical parameter") 
		arr = list(map(ccsne.settings[element.lower()], _pyutils.range_(
			_ccsne.CC_YIELD_GRID_MIN, 
			_ccsne.CC_YIELD_GRID_MAX, 
			_ccsne.CC_YIELD_STEP))) 
		_pyutils.numeric_check(arr, ArithmeticError, 
			"Functional yield mapped to non-numerical value") 
		e[0].ccsne_yields[0].yield_ = _cutils.copy_pylist(arr) 
	else: 
		# failsafe ---> should already be caught 
		raise SystemError("Internal Error") 

	# Map RIa across time 
	if RIa == "exp": 
		# built-in exponential delay-time distribution 
		e[0].sneia_yields[0].RIa = _cutils.map_pyfunc_over_array(
			lambda t: 0 if t < delay else m.exp(-t / 1.5), 
			_pyutils.range_(0, _sneia.RIA_MAX_EVAL_TIME, dt)) 
	elif RIa == "plaw": 
		# power-law delay-time distribution 
		e[0].sneia_yields[0].RIa = _cutils.map_pyfunc_over_array(
			lambda t: 0 if t < delay else (t + 1.e-12)**(
				-1 * _sneia.PLAW_DTD_INDEX), 
			_pyutils.range_(0, _sneia.RIA_MAX_EVAL_TIME, dt)) 
	elif callable(RIa): 
		# custom functional delay-time distribution 
		arr = list(map(lambda t: 0 if t < delay else RIa(t), 
			_pyutils.range_(0, _sneia.RIA_MAX_EVAL_TIME, dt))) 
		_pyutils.numeric_check(arr, ArithmeticError, 
			"Custom RIa evaluated to non-numerical value") 
		e[0].sneia_yields[0].RIa = _cutils.copy_pylist(arr) 
	else: 
		# failsafe ---> should already be caught 
		raise SystemError("Internal Error") 
	_sneia.normalize_RIa(e, _sneia.RIA_MAX_EVAL_TIME / dt + 1) 

	# Call the C routines 
	cdef double *evaltimes = _cutils.binspace(0, time + 10 * dt, 
		long((time + 10 * dt) / dt)) 
	cdef double *cresults = _ssp.single_population_enrichment(ssp, e, 
		Z, 
		evaltimes, 
		long(time / dt) + 11l, 
		mstar) 
	if cresults is NULL: 
		raise MemoryError("Internal Error") 
	else: 
		pass 

	try: 
		# pull the data into python 
		pyresults = [cresults[i] for i in range(int(time / dt) + 1)] 
		times = [evaltimes[i] for i in range(int(time / dt) + 1)] 
	finally: 
		# always free the memory 
		_element.element_free(e) 
		_ssp.ssp_free(ssp)
		free(cresults) 
		free(evaltimes) 

	return [pyresults, times] 


def __ssp_type_checking(element, mstar = 1e6, Z = 0.014, time = 10, 
	dt = 0.01, m_upper = 100, m_lower = 0.08, IMF = "kroupa", RIa = "plaw", 
	delay = 0.15, agb_model = "cristallo11"): 
	""" 
	Does type checking for the single_stellar_population function. See 
	docstring for details on each parameter. 
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
		if RIa.lower() not in _RECOGNIZED_RIAS_: 
			raise ValueError("""Unrecognized RIa: %s. Recognized values: \
%s""" % (RIa, _RECOGNIZED_RIAS_)) 
		else: 
			pass 
	elif callable(RIa): 
		_pyutils.args(RIa, """Custom SNe Ia DTD must take only one numerical \
value as an argument.""") 
	else: 
		raise TypeError("""Keyword arg 'RIa' must be either of type string or \
a callable function with only one parameter. Got: %s""" % (type(RIa))) 
	if not isinstance(agb_model, strcomp): 
		raise TypeError("""Keyword argument 'agb_model' must be of type \
string. Got: %s""" % (type(agb_model))) 
	else: 
		pass 

	# Mstar, Z, dt, m_upper, m_lower, and delay must all be numerical values. 
	__numeric_checker(mstar, "mstar") 
	__numeric_checker(Z, "Z") 
	__numeric_checker(time, "time") 
	__numeric_checker(dt, "dt") 
	__numeric_checker(m_upper, "m_upper") 
	__numeric_checker(m_lower, "m_lower") 
	__numeric_checker(delay, "delay") 


def __ssp_value_checking(element, mstar = 1e6, Z = 0.014, time = 10, 
	dt = 0.01, m_upper = 100, m_lower = 0.08, IMF = "kroupa", RIa = "plaw", 
	delay = 0.15, agb_model = "cristallo11"): 
	"""
	Does value checking for the single_stellar_population function. See 
	docstring for details on each parameter. 

	These lines simply check for unphysical values or unrecognized keywords, 
	and raise a ValueError if the conditions are not met. In the case of time, 
	VICE by design does not simulate evolution on timescales longer than 15 
	Gyr. 

	Also of note is that the Karakas et al. (2010) study of AGB star 
	nucleosynthetic yields did not study elements heavier than nickel.  
	""" 
	# Study keywords to their full citations ---> agb_model keywords 
	studies = {
		"cristallo11": 		"Cristallo et al. (2011), ApJS, 197, 17", 
		"karakas10": 		"Karakas et al. (2010), MNRAS, 403, 1413" 
	} 
	
	if element.lower() not in _RECOGNIZED_ELEMENTS_: 
		raise ValueError("Unrecognized element: %s" % (element)) 
	elif mstar <= 0: 
		raise ValueError("Keyword arg 'mstar' must be greater than zero.") 
	elif Z < 0: 
		raise ValueError("Keyword arg 'Z' must be non-negative.") 
	elif time <= 0: 
		raise ValueError("Keyword arg 'time' must be greater than zero.") 
	elif time > _sneia.RIA_MAX_EVAL_TIME: 
		raise ValueError("""By design, VICE does not simulate enrichment on \
timescales longer than %g Gyr.""" % (_sneia.RIA_MAX_EVAL_TIME)) 
	elif dt <= 0: 
		raise ValueError("Keyword arg 'dt' must be greater than zero.") 
	elif m_upper <= 0: 
		raise ValueError("Keyword arg 'm_upper' must be greater than zero.") 
	elif m_lower <= 0: 
		raise ValueError("Keyword arg 'm_lower' must be greater than zero.") 
	elif m_lower >= m_upper: 
		raise ValueError("Keyword arg 'm_upper' must be larger than 'm_lower'.") 
	elif IMF.lower() not in _RECOGNIZED_IMFS_: 
		raise ValueError("Unrecognized IMF: %s" % (IMF)) 
	elif delay < 0: 
		raise ValueError("Keyword arg 'delay' must be non-negative.") 
	elif agb_model.lower() not in studies.keys(): 
		raise ValueError("""Unrecognized AGB yield model: %s. See docstring \
for list of recognized models.""" % (agb_model)) 
	elif (agb_model.lower() == "karakas10" and 
		atomic_number[element.lower()] > 28): 
		raise LookupError("""The %s study did not report yields for elements \
heavier than nickel.""" % (studies["karakas10"])) 
	else: 
		pass 


def __numeric_checker(pyval, name): 
	"""
	Raises a TypeError if pyval is not a numerical value. Takes it's name 
	as a second parameter for the error message. 
	"""
	if not isinstance(pyval, numbers.Number): 
		raise TypeError("""Keyword arg '%s' must be a numerical value. \
Got: %s""" % (name, type(pyval)))
	else: 
		pass 

