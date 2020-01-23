# cython: language_level = 3, boundscheck = False 
""" 
This file implements the history function, which returns a history object 
from a singlezone output. 
""" 

from __future__ import absolute_import 
from . import _output_utils 
import pickle 
try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 
try: 
	"""
	dill extends the pickle module and allows functional attributes to be 
	encoded. In later version of python 3, dill.dump must be called instead 
	of pickle.dump. All cases can be taken care of by overriding the native 
	pickle module and letting dill masquerade as pickle. 
	"""
	import dill as pickle 
except (ModuleNotFoundError, ImportError): 
	pass 
from ..dataframe._history cimport history as history_obj 


def history(name): 
	"""
	Read in the part of a simulation's output that records the time-evolution 
	of the ISM metallicity. 

	Signature: vice.history(name) 

	Parameters
	==========
	name :: str 
		The name of the output to read the history from, with or without the 
		'.vice' extension. 

	Returns 
	======= 
	hist :: VICE dataframe 
		A VICE history object (a subclass of the VICE dataframe), which 
		contains the time in Gyr, gas and stellar masses in solar masses, star 
		formation and infall rates in Msun/yr, inflow and outflow 
		metallicities for each element, gas-phase mass and metallicities of 
		each element, and every [X/Y] combination of abundance ratios for each 
		output timestep. 

	Raises 
	====== 
	IOError :: [Only occurs if the output has been tampered with]  
		:: The output file is not found. 
		:: The output file is not formatted correctly. 
		:: Other VICE output files are missing from the output 

	Notes 
	===== 
	For an output under a given name, the history file is stored under 
	name.vice/history.out, and it is a simple ascii text file with a comment 
	header detailing each column. By storing the output in this manner, user's 
	may analyze the results of VICE simulations in languages other than 
	python. 

	In addition to the abundance and dynamical evolution information, history 
	objects will also record the effective recycling parameter and the 
	specified mass loading parameter at all times. These ar ethe actual 
	recycling rate divided by the star formation rate and the instantaneous 
	mass loading parameter \\eta that the user has specified regardless of the 
	smoothing time, respectively. 

	In addition to the keys present in history dataframes, users may also 
	index them with 'z' and '[m/h]' [case-insensitive]. This will determine 
	the total metallicity by mass as well as the logarithmic abundance 
	relative to solar. Both are scaled in the following manner: 

	Z = Z_solar * (\\sum_i Z_i / \\sum_i Z_i^solar) 

	This is the scaling of the total metallicity that is encoded into VICE's 
	timestep integrator, which prevents the simulation from behaving as if it 
	has a systematically low metallicity when enrichment is tracked for only 
	a small number of elements. See section 5.4 of VICE's science documentation 
	at https://github.com/giganano/VICE/tree/master/docs for further details. 

	Example 
	=======
	>>> history = vice.history("example") 
	>>> hist.keys() 
	    [“z(fe)”,
	    “mass(fe)”,
	    “[o/fe]”,
	    “z_in(sr)”,
	    “z_in(fe)”,
	    “z(sr)”,
	    “[sr/fe]”,
	    “z_out(o)”,
	    “mgas”,
	    “mass(sr)”,
	    “z_out(sr)”,
	    “time”,
	    “sfr”,
	    “z_out(fe)”,
	    “eta_0”,
	    “[o/sr]”,
	    “z(o)”,
	    “[o/h]”,
	    “ifr”,
	    “z_in(o)”,
	    “ofr”,
	    “[sr/h]”,
	    “[fe/h]”,
	    “r_eff”,
	    “mass(o)”,
	    “mstar”]
	>>> print ("[O/Fe] at end of simulation: %.2e" % (hist["[o/fe]"][-1])) 
	    [O/Fe] at end of simulation: -3.12e-01 
	""" 
	return c_history(name) 



cdef history_obj c_history(name): 
	""" 
	Returns a history object for a given output. 

	For details and documentation, see docstring of history function in this 
	file. 
	""" 
	name = _output_utils._get_name(name) 
	_output_utils._check_singlezone_output(name) 
	try: 
		adopted_solar_z = pickle.load(open("%s/params.config" % (name), 
			"rb"))["Z_solar"] 
	except TypeError: 
		raise SystemError("""\
Error reading encoded parameters stored in output. It appears this output \
was produced in a version of python other than the current.""") 
	return history_obj(
		filename = "%s/history.out" % (name), 
		adopted_solar_z = adopted_solar_z
	) 


