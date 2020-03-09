# cython: language_level = 3, boundscheck = False 
""" 
This file implements the single_stellar_population function. 
""" 

from __future__ import absolute_import 
from ...version import version as _VERSION_ 
from ..._globals import _RECOGNIZED_IMFS_ 
from ..._globals import _VERSION_ERROR_ 
from ...yields.agb._grid_reader import find_yield_file as find_agb_yield_file 
from ...yields import agb 
from ...yields import ccsne 
from ...yields import sneia 
from . import _ssp_utils 
from .. import _pyutils 
import math as m 
import warnings 
import numbers 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from libc.stdlib cimport malloc, free 
from libc.stdio cimport printf 
from .._cutils cimport map_pyfunc_over_array 
# from .._cutils cimport setup_ccsne_yield 
# from .._cutils cimport setup_sneia_yield 
# from .._cutils cimport setup_agb_yield 
from .._cutils cimport callback_1arg_from_pyfunc 
from .._cutils cimport callback_2arg_from_pyfunc 
from .._cutils cimport copy_2Dpylist 
from .._cutils cimport copy_pylist 
from .._cutils cimport set_string 
from .._cutils cimport setup_imf 
from .._cutils cimport binspace 
from ..singlezone._element cimport ELEMENT 
from ..singlezone._ssp cimport SSP 
from ..singlezone cimport _agb 
from ..singlezone cimport _element 
from ..singlezone cimport _io 
from ..singlezone cimport _sneia 
from ..singlezone cimport _ssp 

def single_stellar_population(element, mstar = 1e6, Z = 0.014, time = 10, 
	dt = 0.01, m_upper = 100, m_lower = 0.08, postMS = 0.1, IMF = "kroupa", 
	RIa = "plaw", delay = 0.15, agb_model = None): 
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
		postMS = 0.1, 
		IMF = "kroupa", 
		RIa = "plaw", 
		delay = 0.15, 
		agb_model = None 
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
	postMS :: real number [default :: 0.1] 
		The ratio of a star's post main sequence lifetime to its main sequence 
		lifetime 
	IMF :: str [case-insensitive] or <function> [default :: "kroupa"]
		The stellar initial mass function (IMF) to assume. Strings denote 
		built-in IMFs, which must be either "kroupa" (1) or "salpeter" (2). 
		Functions must accept only one numerical parameter and will be 
		interpreted as a custom, arbitrary stellar IMF. 
	RIa :: str [case-insensitive] or <function> [default :: "plaw"] 
		The delay-time distribution for type Ia supernovae to adopt. VICE will 
		automatically normalize any function that is passed. Alternatively, 
		VICE has built-in distributions: "plaw" (power-law, \\propto t^-1.1) 
		and "exp" (exponential, \\propto e^(-t/1.5 Gyr)). 
	delay :: real number [default :: 0.15] 
		The minimum delay time following the formation of a single stellar 
		population before the onset of type Ia supernovae in Gyr. 
	agb_model :: str [case-insensitive] [default :: None] [DEPRECATED] 
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
	TypeError :: 
		::	RIa is not of type str or <function> 
		::	IMF is not of type str or <function> 
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
		:: 	postMS < 0 or > 1 
		::	built-in IMF is not recognized 
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
		"mstar": 				mstar, 
		"Z": 					Z, 
		"time": 				time, 
		"dt": 					dt, 
		"m_upper": 				m_upper, 
		"m_lower": 				m_lower, 
		"postMS": 				postMS, 
		"RIa": 					RIa, 
		"delay": 				delay, 
		"agb_model": 			agb_model, 
		"RIA_MAX_EVAL_TIME": 	_sneia.RIA_MAX_EVAL_TIME 
	} 
	_ssp_utils._ssp_type_checks(element, **kwargs) 
	_ssp_utils._ssp_value_checks(element, **kwargs) 

	# Necessary C structs for calling _ssp.single_population_enrichment
	cdef SSP *ssp = _ssp.ssp_initialize() 
	cdef ELEMENT *e = _element.element_initialize() 
	# set_string(ssp[0].imf, IMF.lower()) 
	ssp[0].postMS = postMS 
	ssp[0].imf[0].m_upper = m_upper 
	ssp[0].imf[0].m_lower = m_lower 

	# Setup the yields 
	# e[0].sneia_yields[0].yield_ = copy_pylist(map_sneia_yield(element.lower())) 
	# e[0].ccsne_yields[0].yield_ = copy_pylist(map_ccsne_yield(element.lower())) 

	if callable(ccsne.settings[element]): 
		ccfunc = ccsne.settings[element] 
	else: 
		def ccfunc(z): 
			return ccsne.settings[element] 
	e[0].ccsne_yields[0].custom_yield = callback_1arg_from_pyfunc(ccfunc) 

	if callable(sneia.settings[element]): 
		iafunc = sneia.settings[element] 
	else: 
		def iafunc(z): 
			return sneia.settings[element] 
	e[0].sneia_yields[0].custom_yield = callback_1arg_from_pyfunc(iafunc) 

	# e[0].ccsne_yields[0].custom_yield = setup_ccsne_yield(element.lower()) 
	# e[0].sneia_yields[0].custom_yield = setup_sneia_yield(element.lower()) 

	# Take into account deprecation of the keyword arg "agb_model" 
	def builtin_agb_grid(model): 
		agbfile = find_agb_yield_file(element, model) 
		if os.path.exists(agbfile): 
			if _io.import_agb_grid(e, agbfile.encode("latin-1")): 
				raise IOError("Failed to read AGB yield file.") 
			else: 
				pass 
		else: 
			raise IOError("AGB yield file not found. Please re-install VICE.")  
	if agb_model is None: 
		# take into account deprecation of the keyword arg 'agb_model' 
		if callable(agb.settings[element.lower()]): 
			# masses = [_ssp.main_sequence_turnoff_mass(i, 
			# 	postMS) for i in _pyutils.range_(0, time + 10 * dt, dt)] 
			# metallicities = _pyutils.range_(
			# 	_agb.AGB_Z_GRID_MIN, 
			# 	_agb.AGB_Z_GRID_MAX, 
			# 	_agb.AGB_Z_GRID_STEPSIZE 
			# ) 
			# yield_grid = map_agb_yield(element.lower(), masses) 
			# e[0].agb_grid[0].n_m = len(masses) 
			# e[0].agb_grid[0].n_z = len(metallicities)  
			# e[0].agb_grid[0].grid = copy_2Dpylist(yield_grid) 
			# e[0].agb_grid[0].m = copy_pylist(masses) 
			# e[0].agb_grid[0].z = copy_pylist(metallicities) 
			# e[0].agb_grid[0].custom_yield = setup_agb_yield(element.lower()) 
			e[0].agb_grid[0].custom_yield = callback_2arg_from_pyfunc(
				agb.settings[element]
			) 
		else: 
			builtin_agb_grid(agb.settings[element.lower()]) 
	else: 
		msg = """\
Setting AGB star yield model via keyword argument to this function is \
deprecated in this version of VICE (%s). Instead, modify the yield settings \
for the desired element via vice.yields.agb.settings. Function of stellar \
masses and metallicity by mass (respectively) are also supported. 

Elemental yields in the current simulation will be set to the table of %s \
with linear interpolation between masses and metallicities on the grid. 

This feature will be removed in a future release of VICE. 
""" % (_VERSION_, _ssp_utils._AGB_STUDIES_[agb_model])  
		warnings.warn(msg, DeprecationWarning) 
		builtin_agb_grid(agb_model) 
		

	# Map RIa across time 
	if RIa == "exp": 
		# built-in exponential delay-time distribution 
		e[0].sneia_yields[0].RIa = map_pyfunc_over_array(
			lambda t: 0 if t < delay else m.exp(-t / 1.5), 
			_pyutils.range_(0, _sneia.RIA_MAX_EVAL_TIME, dt)) 
	elif RIa == "plaw": 
		# power-law delay-time distribution 
		e[0].sneia_yields[0].RIa = map_pyfunc_over_array(
			lambda t: 0 if t < delay else (t + 1.e-12)**(
				-1 * _sneia.PLAW_DTD_INDEX), 
			_pyutils.range_(0, _sneia.RIA_MAX_EVAL_TIME, dt)) 
	elif callable(RIa): 
		# custom functional delay-time distribution 
		arr = list(map(lambda t: 0 if t < delay else RIa(t), 
			_pyutils.range_(0, _sneia.RIA_MAX_EVAL_TIME, dt))) 
		_pyutils.numeric_check(arr, ArithmeticError, 
			"Custom RIa evaluated to non-numerical value") 
		e[0].sneia_yields[0].RIa = copy_pylist(arr) 
	else: 
		# failsafe ---> should already be caught 
		raise SystemError("Internal Error") 
	_sneia.normalize_RIa(e, _sneia.RIA_MAX_EVAL_TIME / dt + 1) 

	# Call the C routines 
	setup_imf(ssp[0].imf, IMF) 
	cdef double *evaltimes = binspace(0, time + 10 * dt, 
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


######## DEPRECATED IN DEVELOPMENT REPO AFTER RELEASE OF VERSION 1.0.0 ########
	# Import the element's AGB yield grid 
	# agbfile = find_agb_yield_file(element, agb_model) 
	# if os.path.exists(agbfile): 
	# 	if _io.import_agb_grid(e, agbfile.encode("latin-1")): 
	# 		raise IOError("Failed to read AGB yield file.") 
	# 	else: 
	# 		pass 
	# else: 
	# 	raise IOError("AGB yield file not found. Please re-install VICE.") 

	# # e[0].sneia_yields[0].yield_ = sneia.settings[element.lower()] 
	# if isinstance(sneia.settings[element.lower()], numbers.Number): 
	# 	# constant ia yield -> fill the yield grid w/that value 
	# 	length = int((_sneia.IA_YIELD_GRID_MAX - _sneia.IA_YIELD_GRID_MIN) / 
	# 		_sneia.IA_YIELD_STEP) + 1 
	# 	e[0].sneia_yields[0].yield_ = copy_pylist(
	# 		length * [sneia.settings[element.lower()]]) 
	# elif callable(sneia.settings[element.lower()]): 
	# 	# functional ia yield -> map it across the yield grid 
	# 	_pyutils.args(sneia.settings[element.lower()], 
	# 		"Functional yield must take only one numerical parameter") 
	# 	arr = list(map(sneia.settings[element.lower()], _pyutils.range_(
	# 		_sneia.IA_YIELD_GRID_MIN, 
	# 		_sneia.IA_YIELD_GRID_MAX, 
	# 		_sneia.IA_YIELD_STEP 
	# 	))) 
	# 	_pyutils.numeric_check(arr, ArithmeticError, 
	# 		"Functional yield mapped to non-numerical value") 
	# 	e[0].sneia_yields[0].yield_ = copy_pylist(arr) 
	# else: 
	# 	# failsafe ---> should already be caught 
	# 	raise SystemError("Internal Error") 

	# if isinstance(ccsne.settings[element.lower()], numbers.Number): 
	# 	# constant core-collapse yield -> fill the yield grid w/that value  
	# 	length = int((_ccsne.CC_YIELD_GRID_MAX - 
	# 		_ccsne.CC_YIELD_GRID_MIN) / _ccsne.CC_YIELD_STEP) + 1 
	# 	e[0].ccsne_yields[0].yield_ = copy_pylist(
	# 		length * [ccsne.settings[element.lower()]])  
	# elif callable(ccsne.settings[element.lower()]): 
	# 	# functional core-collapse yield -> map it across the yield grid 
	# 	_pyutils.args(ccsne.settings[element.lower()], 
	# 		"Functional yield must take only one numerical parameter") 
	# 	arr = list(map(ccsne.settings[element.lower()], _pyutils.range_(
	# 		_ccsne.CC_YIELD_GRID_MIN, 
	# 		_ccsne.CC_YIELD_GRID_MAX, 
	# 		_ccsne.CC_YIELD_STEP
	# 	))) 
	# 	_pyutils.numeric_check(arr, ArithmeticError, 
	# 		"Functional yield mapped to non-numerical value") 
	# 	e[0].ccsne_yields[0].yield_ = copy_pylist(arr) 
	# else: 
	# 	# failsafe ---> should already be caught 
	# 	raise SystemError("Internal Error") 

