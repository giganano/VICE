# cython: language_level = 3, boundscheck = False
"""
This file scripts the mirror functionality of VICE, which takes in output 
objects and returns simulations with the same parameters that ran them. 
""" 

# Python imports 
from __future__ import absolute_import 
from .._globals import _VERSION_ERROR_ 
from ._pysinglezone import singlezone 
from ._pymultizone import multizone 
from ._output import _get_name 
from ._output import _is_multizone 
from ._output import output 
import warnings 
import pickle 
import sys 
import os 
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
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 

#----------------------------- MIRROR FUNCTION -----------------------------# 
def mirror(arg): 
	"""
	Obtain an instance of either vice.singlezone or vice.multizone class 
	given only an instance of the vice.output class or the path to the output. 
	The returned object will have the same parameters as that which produced 
	the output, allowing re-simulation with whatever modifications the user 
	desires. 

	Signature: vice.mirror(arg) 

	Parameters 
	========== 
	arg :: str or vice.output 
		Either the path to the output (type str) or the output object itself 

	Returns 
	======= 
	obj :: 
		If arg is of type vice.output, then the singlezone object which 
		produced the output is returned. If arg is of type str, then obj is 
		either of type vice.singlezone or vice.multizone, depending on which 
		type of simulation produced the output. 

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
	>>> new
	vice.singlezone{
		name -----------> onezonemodel
		func -----------> <function _DEFAULT_FUNC_ at 0x1085a6ae8>
		mode -----------> ifr
		verbose --------> False
		elements -------> ('fe', 'sr', 'o')
		IMF ------------> kroupa
		eta ------------> 2.5
		enhancement ----> 1.0
		Zin ------------> 0.0
		recycling ------> continuous
		delay ----------> 0.15
		RIa ------------> plaw
		Mg0 ------------> 6000000000.0
		smoothing ------> 0.0
		tau_ia ---------> 1.5
		tau_star -------> 2.0
		schmidt --------> False
		schmidt_index --> 0.5
		MgSchmidt ------> 6000000000.0
		dt -------------> 0.01
		m_upper --------> 100.0
		m_lower --------> 0.08
		Z_solar --------> 0.014
		agb_model ------> cristallo11
		bins -----------> [-3, -2.95, -2.9, ... , 0.9, 0.95, 1]
	}
	>>> import numpy as np 
	>>> new.run(np.linspace(0, 10, 1001)) 
	""" 
	if isinstance(arg, strcomp): 
		arg = _get_name(arg) # some forethought on what the user passed 
		if _is_multizone(arg): 
			# Multizone object -> first need the number of zones 
			params = pickle.load(open("%s/params.config" % (arg), "rb")) 
			mz = multizone(n_zones = params["n_zones"])  
			mz.name = params["name"] 
			mz.n_tracers = params["n_tracers"] 
			mz.verbose = params["verbose"] 
			if params["migration.stars"] != None: 
				mz.migration.stars = params["stars"] 
			else: 
				warnings.warn("""\
Re-initializing functional attributes from VICE output objects requires the \
python package dill (installable via pip). The following attributes will not \
reflect the attributes of the simulation that produced this output, and will \
instead be set to the default value: """, UserWarning)
			zone_numbers = pickle.load(open("%s/zone_numbers.config" % (arg), 
				"rb")) 
			for i in zone_numbers.keys(): 
				""" 
				Singlezone objects can be passed directly to the multizone 
				object without causing memory errors. See also 
				zone_array object in _pymultizone.pyx. 
				""" 
				mz.zones[i] = from_path("%s/%s.vice" % (arg, zone_numbers[i])) 
				mz.zones[i].name = zone_numbers[i] 
			for i in range(mz.n_zones): 
				for j in range(mz.n_zones): 
					# copy over the migration matrices 
					mz.migration.gas[i][j] = params["migration.gas"][i][j] 
			return mz 
		else: 
			# assume it's singlezone, hand off to the from_path reader 
			return from_path(arg) 
	elif isinstance(arg, output): 
		# output object, hand off to the from_output reader 
		return from_output(arg) 
	else: 
		raise TypeError("""Argument must be of type str or vice.output. \
Got: %s""" % (type(arg))) 


def from_path(filename): 
	""" 
	Obtain an instance of the vice.singlezone class given the path to an 
	output. The returned singlezone object will have the same parameters as 
	that which produced the output, allowing re-simulation with whatever 
	modifications the user desires. 
	""" 
	# error handling in output.__init__ 
	return from_output(output(filename)) 


def from_output(output_obj): 
	""" 
	Obtain an instance of the vice.singlezone class given an output object 
	containing it. The returned singlezone object will have the same parameters 
	as the output, allowing re-simulation with whatever modifications the 
	user desires. 
	""" 
	if isinstance(output_obj, output): 
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
			raise ImportError("""\
This output has encoded functional attributes, indicating that it was ran on \
a system in which dill is installed (installable via pip). To initialize a \
singlezone object from this output, please install dill.""") 

		if "dill" not in sys.modules: 
			""" 
			Remove functional attributes from the **kwargs passed to the 
			singlezone object, and warn the user. 
			""" 
			copy = {} 
			functional = [] 
			for i in params.keys(): 
				if params[i] == None: 
					functional.append(i) 
				elif isinstance(params[i], dict): 
					""" 
					check for missed functions inside evoluationary_settings 
					attributes 
					""" 
					copy[i] = {} 
					for j in params["elements"]: 
						if params[i][j] == None: 
							functional.append("%s(%s)" % (i, j)) 
							copy[i][j] = 0.0 # default is zero 
						else: 
							copy[i][j] = params[i][j] 
				else: 
					copy[i] = params[i] 

			message = """\
Re-initializing functional attributes from VICE output objects requires the \
python package dill (installable via pip). The following attributes will not \
reflect the attributes of the simulation that produced this output, and will \
instead be set to the default value: """
			for i in functional: 
				message += "%s " % (i) 
			warnings.warn(message, UserWarning) 
			return singlezone(**copy) 

		else: 
			return singlezone(**params) 

	else: 
		raise TypeError("Argument must be of type vice.output. Got: %s" % (
			type(output_obj))) 


