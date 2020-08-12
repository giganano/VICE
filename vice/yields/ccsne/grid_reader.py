
from __future__ import absolute_import 
__all__ = ["table"] 
from ...core.dataframe._ccsn_yield_table import ccsn_yield_table 
from ...core.dataframe._builtin_dataframes import stable_isotopes 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ..._globals import _VERSION_ERROR_ 
from ..._globals import ScienceWarning 
from ._errors import _RECOGNIZED_STUDIES_ 
from ._errors import find_yield_file
from ._errors import numeric_check 
from ._errors import string_check 
from ._errors import _ROTATION_ 
from ._errors import _MOVERH_ 
from ._errors import _NAMES_ 
import warnings 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 


def table(element, study = "LC18", MoverH = 0, rotation = 0, wind = True, 
	isotopic = False): 
	
	r""" 
	Look up the mass yield of a given element as a function of stellar mass 
	as reported by a given study. 

	**Signature**: vice.yields.ccsne.table(element, study = "LC18", MoverH = 0, 
	rotation = 0, wind = True, isotopic = False) 

	Parameters 
	----------
	element : ``str`` [case-insensitive] 
		The symbol of the element to look up the yield table for. 
	study : ``str`` [case-insensitive] [default : "LC18"] 
		A keyword denoting which study to pull the table from 

		Keywords and their Associated Studies: 

			- "LC18": Limongi & Chieffi (2018) [1]_ 
			- "CL13": Chieffi & Limongi (2013) [2]_ 
			- "NKT13": Nomoto, Kobayashi & Tominaga (2013) [3]_ 
			- "CL04": Chieffi & Limongi (2004) [4]_ 
			- "WW95": Woosley & Weaver (1995) [5]_ 
			- "S16/W18": Sukhbold et al. (2016) [6]_ (W18 explosion engine) 

	MoverH : real number [default : 0] 
		The total metallicity [M/H] of the exploding stars. There are only a 
		handful of metallicities recognized by each study. 

		Keywords and their Associated Metallicities: 

			- "LC18": [M/H] = -3, -2, -1, 0 
			- "CL13": [M/H] = 0 
			- "NKT13": [M/H] = -inf, -1.15, -0.54, -0.24, 0.15, 0.55 
			- "CL04": [M/H] = -inf, -4, -2, -1, -0.37, 0.15 
			- "WW95": [M/H] = -inf, -4, -2, -1, 0 
			- "S16/W18": [M/H] = 0 

	rotation : real number [default : 0] 
		The rotational velocity of the exploding stars in km/s. There are only 
		a handful of rotational velocities recognized by each study. 

		Keywords and their Associated Rotational Velocities: 

			- "LC18": v = 0, 150, 300 
			- "CL13": v = 0, 300 
			- "NKT13": v = 0 
			- "CL04": v = 0 
			- "WW95": v = 0 
			- "S16/W18": v = 0 

	wind : bool [default : ``True``] 
		If True, the stellar wind contribution to the yield will be included 
		in the reported table. If False, the table will include only the 
		supernova explosion yields. 

		.. note:: Wind and explosive yields are only separated for the 
			Limongi & Chieffi (2018) and Sukhbold et al. (2016) studies. Wind 
			yields are not separable from explosive yields for other studies 
			supported by this function. 

	isotopic : ``bool`` [default : ``False``] 
		If ``True``, the full-breakdown of isotopic mass yields is returned. 
		If ``False``, only the total mass yield of the given element is 
		returned. 

	Returns 
	-------
	yields : ``ccsn_yield_table`` [VICE ``dataframe`` derived class] 
		A dataframe designed to hold a CCSN yield table. It can be indexed via 
		stellar mass in :math:`M_\odot` or the isotopes of the requested 
		element (if ``isotopic == True``). 

	Raises 
	------
	* ValueError 
		- 	The element is not built into VICE 
		- 	The study is not built into VICE 
	* LookupError 
		- 	The study did not report yields for the requested element 
		- 	The study did not report yields at the specified metallicity 
		- 	The study did not report yields at the specified rotational 
			velocity. 
	* ScienceWarning 
		- 	``wind = False`` and ``study`` is anything other than 
			LC18 or S16. These are the only studies for which wind yields were 
			reported separate from explosive yields. 

	Notes 
	-----
	.. note:: The nucleosynthetic yield tables built into VICE do not include 
		any treatment of radioactive isotopes. The yield tables returned from 
		this function will not include what the specified study reported for 
		radioactive isotopes. In the case of elements with a significant 
		nucleosynthetic contribution from radioactive decay products, the 
		values returned from this function should be interpreted as lower 
		bounds rather than estimates of the true yield. 

	Example Code 
	------------
	>>> import vice 
	>>> vice.yields.ccsne.table('o') 
	vice.dataframe{
		13.0 -----------> 0.247071034
		15.0 -----------> 0.585730308
		20.0 -----------> 1.256452301
		25.0 -----------> 2.4764558329999997
		30.0 -----------> 0.073968147
		40.0 -----------> 0.087475695
		60.0 -----------> 0.149385561
		80.0 -----------> 0.24224373600000002
		120.0 ----------> 0.368598602
	} 
	>>> vice.yields.ccsne.table('o', isotopic = True) 
	vice.dataframe{
		13 -------------> {'o16': 0.24337, 'o17': 5.5634e-05, 'o18': 0.0036454}
		15 -------------> {'o16': 0.58234, 'o17': 5.5608e-05, 'o18': 0.0033347}
		20 -------------> {'o16': 1.2501, 'o17': 4.6201e-05, 'o18': 0.0063061}
		25 -------------> {'o16': 2.4724, 'o17': 4.7633e-05, 'o18': 0.0040082}
		30 -------------> {'o16': 0.073782, 'o17': 4.0707e-05, 'o18': 0.00014544}
		40 -------------> {'o16': 0.087253, 'o17': 4.1705e-05, 'o18': 0.00018099}
		60 -------------> {'o16': 0.1491, 'o17': 5.3011e-05, 'o18': 0.00023255}
		80 -------------> {'o16': 0.24192, 'o17': 6.1316e-05, 'o18': 0.00026242}
		120 ------------> {'o16': 0.36819, 'o17': 7.9192e-05, 'o18': 0.00032941}
	} 

	.. [1] Limongi & Chieffi (2018), ApJS, 237, 13 
	.. [2] Chieffi & Limongi (2013), ApJ, 764, 21 
	.. [3] Nomoto, Kobayashi & Tominaga (2013), ARA&A, 51, 457 
	.. [4] Chieffi & Limongi (2004), ApJ, 608, 405 
	.. [5] Woosley & Weaver (1995), ApJ, 101, 181 
	.. [6] Sukhbold et al. (2016), ApJ, 821, 38 
	""" 

	if not isinstance(element, strcomp): 
		raise TypeError("Element must be of type str. Got: %s" % (
			type(element))) 
	elif element.lower() not in _RECOGNIZED_ELEMENTS_: 
		raise ValueError("Unrecognized element: %s" % (element)) 
	else: 
		pass 

	# Type check keyword args 
	string_check(study, "study") 
	numeric_check(MoverH, "MoverH") 
	numeric_check(rotation, "rotation") 
	try: 
		isotopic = bool(isotopic) 
	except: 
		raise TypeError("""Keyword 'isotopic' must be interpretable as a \
boolean. Got: %s""" % (type(isotopic))) 

	# value check keyword args 
	if study.upper() not in _RECOGNIZED_STUDIES_: 
		raise ValueError("Unrecognized study: %s" % (study)) 
	elif MoverH not in _MOVERH_[study.upper()]: 
		raise LookupError("The %s study does not have yields for [M/H] = %g" % (
			_NAMES_[study.upper()], MoverH)) 
	elif rotation not in _ROTATION_[study.upper()]: 
		raise LookupError("""The %s study does not have yields for v = %g \
km/s and [M/H] = %g""" % (rotation, MoverH)) 
	else: 
		filename = find_yield_file(study, MoverH, rotation, "explosive", 
			element) 

	# Find and read the file 
	if not os.path.exists(filename): 
		raise LookupError("""The %s study did not report yields for the \
element %s. If adopting these yields for simulation, it is likely that this \
yield can be approximated as zero at this metallicity. Users may exercise \
their own discretion by modifying their CCSN yield settings directly.""" % (
			_NAMES_[study.upper()], element)) 
	else: 
		grid = read_grid(filename) 

	if wind: 
		wind_grid = read_grid(find_yield_file(study, MoverH, rotation, "wind", 
			element)) 
		for i in range(len(grid)): 
			for j in range(1, len(grid[i])): 
				grid[i][j] += wind_grid[i][j] 
	elif study.upper() not in ["LC18", "S16/W18"]: 
		warnings.warn("""The %s study did not separate the yields from the \
wind and the explosion, publishing only the total yields from both. For this \
reason, this function cannot separate the wind yields from this table.""" % (
			_NAMES_[study.upper()]), ScienceWarning) 
	else: pass 

	# Format them as total or isotopic mass yields, and return a yield table 
	masses = tuple([i[0] for i in grid]) 
	isotopic_yields = (len(grid[0]) - 1) * [None] 
	for i in range(1, len(grid[0])): 
		isotopic_yields[i - 1] = tuple([row[i] for row in grid]) 

	if isotopic: 
		return ccsn_yield_table(masses, tuple(isotopic_yields), 
			isotopes = ["%s%d" % (element.lower(), 
				i) for i in stable_isotopes[element]]) 
	else: 
		mass_yields = len(masses) * [0.] 
		for i in range(len(mass_yields)): 
			mass_yields[i] = sum([j[i] for j in isotopic_yields])  
		return ccsn_yield_table(masses, mass_yields, isotopes = None) 


def read_grid(filename): 
	r""" 
	Read in the contents of a yield grid given the filename. 

	Parameters 
	----------
	filename: str 
		The path to the file to read. 

	Returns 
	-------
	yields : list 
		The contents of the yield file as a 2-D list 
	""" 
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
	return contents 

