r""" 
This file implements the repair_function function. 
""" 

from __future__ import absolute_import 
from ..._globals import _VERSION_ERROR_ 
from ...core.outputs import output 
from ...core import pickles 
from .repfunc import repfunc 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 


def repair_function(out, key): 
	r""" 
	"Repair" a function which was not able to be pickled with a VICE output. 

	.. versionadded:: 1.X.0 

	Parameters 
	----------
	out : str or output 
		The full or relative path to a VICE output (the ".vice" extension is 
		not necessary). Alternatively, the corresponding output object can be 
		passed. 
	key : str [case-insensitive] 
		A string denoting the function to repair from the output. This must be 
		one of the following: 

		* "sfr" : the star formation rate in :math:`M_\odot yr^{-1}` 
		  as a function of time in Gyr. 
		* "ifr" : the infall rate rate in :math:`M_\odot yr^{-1}` 
		  as a function of time in Gyr. 
		* "mgas" : the amount of interstellar gas in :math:`M_\odot` as a 
		  function of time in Gyr. 
		* "eta" : the outflow mass loading factor (unitless) as a function of 
		  time in Gyr. 
		* "z_in(x)" : the inflow metallicity of an element :math:`x` as a 
		  function of time in Gyr. 
		* "tau_star" : the star formation efficiency timescale in Gyr as a 
		  function of time in Gyr. 

		These are all of the functions which can be approximated from the 
		output. 

	Returns 
	-------
	func : repfunc 
		A callable object accepting time in Gyr as the parameter, storing the 
		value of the given function at all times as reported by the output. It 
		will automatically interpolate linearly in time to approximate the 
		value of the function at all other times. 

	Raises 
	------
	* ValueError 
		- key is not from the allowed set of values (see above) 
	* ScienceWarning 
		- key = "tau_star" and the simulation was ran with the attribute 
		  ``schmidt = True`` 

	Example Code 
	------------
	>>> sz = vice.singlezone(name = "example") 
	>>> sz.func = vice.toolkit.repair_function("oldmodel", "ifr") 
	>>> sz.tau_star = vice.toolkit.repair_function("oldmodel", "tau_star") 
	>>> sz.run([0.01 * i for i in range(1001)]) 
	""" 
	if isinstance(out, strcomp): 
		# Let the output object do the file I/O and use simple recursion 
		return repair_function(output(out), key) 
	elif isinstance(out, output): 
		if isinstance(key, strcomp): 
			""" 
			Each possible option has to be considered individually, because 
			some of them require special warnings to be raised or a specific 
			calculation. 
			""" 
			if key.lower() in ["sfr", "ifr", "mgas"]: 
				# no special consideration or warnings 
				return repfunc(out.history["time"], out.history[key]) 
			elif key.lower() == "eta": 
				return repfunc(out.history["time"], out.history["eta_0"]) 
			elif '(' in key and key.lower().split('(')[0] == "z_in": 
				# This should be an infall metallicity 
				return repfunc(out.history["time"], out.history[key]) 
			elif key.lower() == "tau_star": 
				if pickles.pickled_object.from_pickle(
					"%s.vice/attributes/schmidt.obj" % (out.name)): 
					warnings.warn("""\
This simulation was ran with the attribute 'schmidt' = True. With this \
repaired function, its parameters are best reproduced by switching this \
parameter to False.""", ScienceWarning) 
				else: pass 
				tstar = list(map(lambda x, y: 1.e-9 * x / y, 
					out.history["mgas"], out.history["sfr"])) 
				return repfunc(out.history["time"], tstar) 
			else: 
				raise ValueError("""Unrecognized key. Must be one of: 'sfr', \
'ifr', 'mgas', 'eta', 'tau_star', or 'z_in(<element>)'. Got: %s""" % (key)) 
		else: 
			raise TypeError("Key must be of type str. Got: %s" % (type(key))) 
	else: 
		raise TypeError("Out must be of type str or output. Got: %s" % (
			type(out))) 




