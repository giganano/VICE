# cython: language_level = 3, boundscheck = False 
"""
This file wraps the C subroutines for reading AGB yield grids 
""" 

# Python imports 
from __future__ import absolute_import 
from ..._globals import _DIRECTORY_ 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ..._globals import _VERSION_ERROR_ 
from ...core._builtin_dataframes import atomic_number 
from ...core import _pyutils 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 

# C imports 
from libc.stdlib cimport malloc, free 
from ...core._objects cimport AGB_YIELD_GRID, ELEMENT 
from ...core cimport _agb 
from ...core cimport _cutils 
from ...core cimport _element 
from ...core cimport _io 

_RECOGNIZED_STUDIES_ = tuple(["cristallo11", "karakas10"]) 

#-------------------------- AGB_YIELD_GRID FUNCTION --------------------------# 
def yield_grid(element, study = "cristallo11"):
	"""
	Obtain the stellar mass-metallicity grid of fractional nucleosynthetic 
	yields from asymptotic giant branch (AGB) stars. VICE includes yields 
	from Cristallo et al. (2011), ApJS, 197, 17 and Karakas (2010), MNRAS, 403, 
	1413, allowing users the choice of which to adopt in their simulations. 

	Signature: vice.yields.agb.grid(element, study = "cristallo11") 

	Parameters
	==========
	element :: str [case-insensitive] 
		The symbol of the element to obtain the yield grid for. 
	study :: str [case-insensitive] [default :: "cristallo11"]
		A keyword denoting which AGB yield study to pull the yield table from. 
		Keywords and their Associated Studies: 
		--------------------------------------
		"cristallo11" :: Cristallo et al. (2011), ApJS, 197, 17 
		"karakas10" :: Karakas (2010), MNRAS, 403, 1413 

	Returns
	=======
	grid :: tuple (2-D)
		The yield grid itself; elements are tuples of fractional 
		nucleosynthetic yields at constant stellar mass, but varying 
		metallicity. It should be indexed with the rule: 
		arr[mass_index][z_index]
	masses :: tuple 
		The masses in terms of the sun that the yield grid is sampled on. 
	z :: tuple 
		The metallicities by mass Z on that the yield grid is sampled on. 

	Raises
	====== 
	ValueError :: 
		::	The study or the element are not built into VICE 
	LookupError :: 
		:: 	study == "karakas10" and the atomic number of the element is 
			greater than or equal to 29. The Karakas (2010), MNRAS, 403, 1413 
			study did not report yields from AGB stars for elements heavier 
			than nickel. 
	IOError :: [Occurs only if VICE's file structure has been tampered with] 
		:: 	The parameters passed to this function are allowed but the data 
			file is not found. 

	Example
	=======
	>>> y, m, z = vice.agb_yield_grid("sr") 
	>>> m 
	    (1.3, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0) 
	>>> z 
	    (0.0001, 0.0003, 0.001, 0.002, 0.003, 0.006, 0.008, 0.01, 0.014, 0.02) 
	>>> # the fractional yield from 1.3 Msun stars at Z = 0.001 
	>>> y[0][2] 
	    2.32254e-09

	References 
	========== 
	Cristallo et al. (2011), ApJS, 197, 17 
	Karakas (2010), MNRAS, 403, 1413 
	""" 
	# Type checking  
	if not isinstance(element, strcomp): 
		raise TypeError("First argument must be of type string. Got: %s" % (
			type(element))) 
	elif not isinstance(study, strcomp): 
		raise TypeError("""Keyword arg 'study' must be of type string. \
Got: %s""" % (study)) 
	else: 
		pass 

	# Study keywords to their full citations 
	studies = {
		"cristallo11": 			"Cristallo et al. (2011), ApJ, 197, 17", 
		"karakas10": 			"Karakas (2010), MNRAS, 403, 1413" 
	} 

	# Value checking 
	if study.lower() not in _RECOGNIZED_STUDIES_: 
		raise ValueError("Unrecognized study: %s" % (study)) 
	elif element.lower() not in _RECOGNIZED_ELEMENTS_: 
		raise ValueError("Unrecognized element: %s" % (element)) 
	else: 
		pass 

	if study.lower() == "karakas10" and atomic_number[element.lower()] > 28: 
		raise LookupError("""The %s study did not report yields for elements \
heavier than nickel (atomic number 28).""" % (studies["karakas10"])) 
	else: 
		pass 

	# full path to the file containing the yield grid 
	filename = find_yield_file(element, study) 

	if not os.path.exists(filename): 
		"""
		File nt found ---> unless VICE was tampered with, this shouldn't 
		happen. 
		""" 
		raise IOError("Yield file not found. Please re-install VICE.") 
	else: 
		pass 

	cdef ELEMENT *e = _element.element_initialize() 
	if _io.import_agb_grid(e, filename.encode("latin-1")): 
		free(e) 
		raise SystemError("Internal Error: couldn't read yield file.") 
	else: 
		try: 
			# copy over the yields, masses, and metallicities 
			yields = e[0].agb_grid[0].n_m * [None] 
			for i in range(e[0].agb_grid[0].n_m): 
				yields[i] = e[0].agb_grid[0].n_z * [0.0] 
				for j in range(e[0].agb_grid[0].n_z): 
					yields[i][j] = e[0].agb_grid[0].grid[i][j] 
			masses = [e[0].agb_grid[0].m[i] for i in range(
				e[0].agb_grid[0].n_m)] 
			metallicities = [e[0].agb_grid[0].z[i] for i in range(
				e[0].agb_grid[0].n_z)] 
		finally: 
			free(e[0].agb_grid[0].m) 
			free(e[0].agb_grid[0].z) 
			free(e[0].agb_grid[0].grid) 
			free(e) 

		return [tuple(i) for i in [[tuple(j) for j in yields], masses, 
			metallicities]] 

def find_yield_file(element, study): 
	""" 
	Determines the full path to the file containing the mass-metallicity 
	yield grid for a given element and study. 

	Parameters 
	========== 
	element :: str [case-insensitive] 
		The symbol for the element whose file is to be found 
	study :: str [case-insensitive] 
		The keyword for the study to lookup 

	Returns 
	======= 
	path :: str 
		The path to the yield file 

	Raises 
	====== 
	TypeError :: 
		:: element is not of type str 
		:: study is not of type str 
	ValueError :: 
		:: element is not recognized by VICE 
		:: study is not recognized by VICE 
	""" 
	if not isinstance(element, strcomp): 
		raise TypeError("Element must be of type str. Got: %s" % (
			type(element)))
	elif not isinstance(study, strcomp): 
		raise TypeError("Study must be of type str. Got: %s" % (
			type(study))) 
	elif element.lower() not in _RECOGNIZED_ELEMENTS_: 
		raise ValueError("Unrecognized element: %s" % (element)) 
	elif study.lower() not in _RECOGNIZED_STUDIES_: 
		raise ValueError("Unrecognized study: %s" % (study)) 
	else: 
		return "%syields/agb/%s/%s.dat" % (_DIRECTORY_, study.lower(), 
			element.lower()) 





