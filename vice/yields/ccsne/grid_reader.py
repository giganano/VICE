
from __future__ import absolute_import 
__all__ = ["table"] 
from ...core.dataframe._ccsn_yield_table import ccsn_yield_table 
from ...core.dataframe._builtin_dataframes import stable_isotopes 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ..._globals import _VERSION_ERROR_ 
from .errors import _RECOGNIZED_STUDIES_ 
from .errors import find_yield_file
from .errors import numeric_check 
from .errors import string_check 
from .errors import _ROTATION_ 
from .errors import _MOVERH_ 
from .errors import _NAMES_ 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 


def table(element, study = "LC18", MoverH = 0, rotation = 0, isotopic = False): 
	""" 
	Look up the mass yield of a given element as a function of stellar mass 
	as reported by a given study. 

	Signature: vice.yields.ccsne.table(
		element, 
		study = "LC18", 
		MoverH = 0, 
		rotation = 0, 
		isotopic = False 
	) 

	Parameters 
	========== 
	element :: str [case-insensitive] 
		The symbol of the element to look up the yield table for 
	study :: str [case-insensitive] [default :: "LC18"] 
		A keyword denoting which study to look up the table from 
		Keywords and their Associated Studies 
		------------------------------------- 
		"LC18"	:: Limongi & Chieffi (2018), ApJS, 237, 13
		"CL13"	:: Chieffi & Limongi (2013), ApJ, 764, 21 
		"NKT13"	:: Nomoto, Kobayashi & Tominaga (2013), ARA&A, 51, 457
		"CL04"	:: Chieffi & Limongi (2004), ApJ, 608, 405 
		"WW95"	:: Woosley & Weaver (1995) ApJ, 101, 181 
	MoverH :: real number [default :: 0] 
		The total metallicity [M/H] of the exploding stars. There are only a 
		handful of metallicities recognized by each study, and VICE will raise 
		a LookupError if this value is not one of them. 
		Keywords and their Associated Metallicities 
		------------------------------------------- 
		"LC18"	:: [M/H] = -3, -2, -1, 0 
		"CL13"	:: [M/H] = 0 
		"NKT13"	:: [M/H] = -inf, -1.15, -0.54, -0.24, 0.15, 0.55 
		"CL04"	:: [M/H] = -inf, -4, -2, -1, -0.37, 0.15 
		"WW95"	:: [M/H] = -inf, -4, -2, -1, 0
	rotation :: real number [default :: 0] 
		The rotational velocity of the exploding stars in km/s. There are only 
		a handful of rotational velocities recognized by each study, and VICE 
		will raise a LookupError if this value is not one of them. 
		Keywords and their Associated Rotational Velocities 
		--------------------------------------------------- 
		"LC18"	:: v = 0, 150, 300 
		"CL13"	:: v = 0, 300 
		"NKT13"	:: v = 0 
		"CL04"	:: v = 0 
		"WW95"	:: v = 0 
	isotopic :: bool [default :: False] 
		If True, the full-breakdown of isotopic mass yields is returned. If 
		False, only the total mass yield of the given element is returned. 

	Returns 
	======= 
	yields :: dataframe 
		A VICE dataframe designed to hold a CCSN yield table. It can be 
		indexed via stellar mass or (if isotopic = True) the isotopes of the 
		requested element 

	Raises 
	====== 
	ValueError :: 
		::	The element is not built into VICE 
		::	The study is not built into VICE 
	LookupError ::
		::	The study did not report yields for the requested element 
		::	The study did not report yields at the specified metallicity 
		::	The study did not report yields at the specified rotational 
			velocity 
	ScienceWarning :: 
		::	Study is either "CL04" or "CL13" and the atomic number of the 
			element is between 24 and 28 (inclusive). VICE warns against 
			adopting these yields for iron peak elements. 
	""" 
	if not isinstance(element, strcomp): 
		raise TypeError("Element must be of type str. Got: %s" % (
			type(element))) 
	elif element.lower() not in _RECOGNIZED_ELEMENTS_: 
		raise ValueError("Unrecognized element: %s" % (element)) 
	else: 
		pass 

	string_check(study, "study")  
	numeric_check(MoverH, "MoverH")  
	numeric_check(rotation, "rotation")  
	try: 
		isotopic = bool(isotopic) 
	except: 
		raise TypeError("""Keyword 'isotopic' must be interpretable as a \
boolean. Got: %s""" % (type(isotopic))) 

	if study.upper() not in _RECOGNIZED_STUDIES_: 
		raise ValueError("Unrecognized study: %s" % (study)) 
	elif MoverH not in _MOVERH_[study.upper()]: 
		raise LookupError("The %s study does not have yields for [M/H] = %g" % (
			_NAMES_[study.upper()], MoverH)) 
	elif rotation not in _ROTATION_[study.upper()]: 
		raise LookupError("""The %s study does not have yields for v = %g \
km/s and [M/H] = %g""" % (rotation, MoverH)) 
	else: 
		filename = find_yield_file(study, MoverH, rotation, element) 

	if not os.path.exists(filename): 
		raise LookupError("""The %s study did not report yields for the \
element %s. If adopting these yields for simulation, it is likely that this \
yield can be approximated as zero at this metallicity. Users may exercise \
their own discretion by modifying their CCSN yield settings directly.""" % (
			_NAMES_[study.upper()], element)) 
	else: 
		with open(filename, 'r') as f: 
			contents = [] 
			line = f.readline() 
			while line[0] == '#': 
				line = f.readline() 
			line = f.readline() 
			while line != "": 
				contents.append([float(i) for i in line.split()])  
				line = f.readline() 
			f.close() 

	masses = tuple([i[0] for i in contents]) 
	isotopic_yields = (len(contents[0]) - 1) * [None] 
	for i in range(1, len(contents[0])): 
		isotopic_yields[i - 1] = tuple([row[i] for row in contents]) 

	if isotopic: 
		return ccsn_yield_table(masses, tuple(isotopic_yields), 
			isotopes = ["%s%d" % (element.lower(), 
				i) for i in stable_isotopes[element]]) 
	else: 
		mass_yields = len(masses) * [0.] 
		for i in range(len(mass_yields)): 
			mass_yields[i] = sum([j[i] for j in isotopic_yields])  
		return ccsn_yield_table(masses, mass_yields, isotopes = None) 

