""" 
This file implements the mirror function, which takes in output objects or 
relative paths to outputs and returns simulations with the same parameters 
that ran them. 
""" 

from __future__ import absolute_import 
from .._globals import _RECOGNIZED_ELEMENTS_ 
from .._globals import _VERSION_ERROR_ 
from .singlezone import singlezone 
from .multizone import multizone 
from .outputs._output_utils import _check_singlezone_output 
from .outputs._output_utils import _is_multizone 
from .outputs._output_utils import _get_name 
from .outputs import multioutput 
from .outputs import output 
from . import pickles 
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
		bins -----------> [-3, -2.95, -2.9, ... , 0.9, 0.95, 1]
	}
	>>> import numpy as np 
	>>> new.run(np.linspace(0, 10, 1001)) 
	""" 
	if isinstance(arg, strcomp): 
		# this will send it to from_multizone_output if necessary 
		return from_singlezone_output(arg) 
	elif isinstance(arg, output): 
		return from_singlezone_output(arg) 
	elif isinstance(arg, multioutput): 
		return from_multizone_output(arg) 
	else: 
		raise TypeError("""Expected either a string or an output object. \
Got: %s""" % (type(arg))) 



def from_multizone_output(arg): 
	""" 
	Obtain an instance of the vice.multizone class given either the path to an 
	output or an output itself. 

	Parameters 
	========== 
	arg :: str or vice.multioutput 
		The full or relative path to the output directory. Alternatively, an 
		output object. 

	Returns 
	======= 
	mz :: vice.multizone 
		A multizone object with the same parameters as that which produced 
		the output 

	Raises 
	====== 
	TypeError :: 
		::	arg is neither an output object nor a string 
	IOError :: 
		::	output is not found, or is missing files 
	""" 
	if isinstance(arg, multioutput): 
		# recursion to the algorithm which does it from the path 
		return from_multizone_output(arg.name) 
	elif isinstance(arg, strcomp): 
		dirname = _get_name(arg) 
		if not _is_multizone(dirname): return from_singlezone_output(dirname) 
	else: 
		raise TypeError("""Must be either a string or an output object. \
Got: %s""" % (type(arg))) 

	attrs = pickles.jar.open("%s/attributes" % (dirname)) 
	mz = multizone(n_zones = attrs["n_zones"]) 
	mz.name = attrs["name"] 
	mz.n_tracers = attrs["n_tracers"] 
	mz.simple = attrs["simple"] 
	mz.verbose = attrs["verbose"] 
	for i in range(mz.n_zones): 
		mz.zones[i] = from_singlezone_output("%s/%s.vice" % (dirname, 
			attrs["zones"][i])) 
		mz.zones[i].name = attrs["zones"][i] 
	
	stars = pickles.jar.open("%s/migration" % (dirname))["stars"] 
	if stars is None: 
		warnings.warn("""\
Attribute not encoded with output: migration.stars. Assuming default value, \
which may not reflect the value of this attribute at the time the simulation \
was ran.""", UserWarning) 
	else: 
		mz.migration.stars = stars 

	for i in range(mz.n_zones): 
		attrs = pickles.jar.open("%s/migration/gas%d" % (dirname, i)) 
		for j in range(mz.n_zones): 
			if attrs[str(j)] is None: 
				warnings.warn("""\
Attribute not encoded with output: migration.gas[%d][%d]. Assuming default \
value, which may not reflect the value of this attribute at the time the \
simulation was ran.""" % (i, j), UserWarning) 
			else: 
				mz.migration.gas[i][j] = attrs[str(j)]  

	return mz 


def from_singlezone_output(arg): 
	""" 
	Obtain an instance of the vice.singlezone class given either the path to 
	an output or an output itself. 

	Parameters 
	========== 
	arg :: str or vice.output 
		The full or relative path to the output directory. Alternatively, an 
		output object. 

	Returns 
	======= 
	sz :: vice.singlezone 
		A singlezone object with the same parameters as that which produced 
		the output 

	Raises 
	====== 
	TypeError :: 
		::	arg is neither an output object nor a string 
	IOError :: 
		::	output is not found, or is missing files 
	""" 
	if isinstance(arg, output): 
		# recursion to the algorithm which does it from the path 
		return from_singlezone_output(arg.name) 
	if isinstance(arg, strcomp): 
		# make sure the output looks okay 
		dirname = _get_name(arg) 
		if _is_multizone(dirname): return from_multizone_output(dirname) 
		_check_singlezone_output(dirname) 
	else: 
		raise TypeError("""Must be either a string or an output object. \
Got: %s""" % (type(arg)))  

	attrs = pickles.jar.open("%s/attributes" % (dirname)) 
	copy = {} # copy the attributes one by one, checking for lost values 
	for i in attrs.keys(): 
		if i.startswith("entrainment") or i == "agb_model": 
			"""
			take care of these two at the end -> agb_model is None by default 
			due to deprecation, so don't raise a misleading UserWarning. 
			""" 
			continue 
		elif attrs[i] is None: 
			warnings.warn("""\
Attribute not encoded with output: %s. Assuming default value, which may not \
reflect the value of this attribute at the time the simulation was ran.""" % (
				i), UserWarning) 
		elif isinstance(attrs[i], dict): 
			# check for None values in dataframe attributes 
			attr_copy = {} 
			for j in attrs[i].keys(): 
				if attrs[i][j] is None: 
					warnings.warn("""\
Attribute not encoded with output: %s["%s"]. Assuming default value, which \
may not reflect the value of this attribute at the time the simulation was \
ran.""" % (i, j), UserWarning) 
				else: 
					attr_copy[j] = attrs[i][j] 
			copy[i] = attr_copy 
		else: 
			copy[i] = attrs[i] 
	copy["agb_model"] = attrs["agb_model"] 
	sz = singlezone(**copy) 
	for i in sz.elements: 
		sz.entrainment.agb[i] = attrs["entrainment.agb"][i] 
		sz.entrainment.ccsne[i] = attrs["entrainment.ccsne"][i] 
		sz.entrainment.sneia[i] = attrs["entrainment.sneia"][i] 
	return sz 

