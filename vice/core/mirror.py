""" 
This file implements the mirror function, which takes in output objects or 
relative paths to outputs and returns simulations with the same parameters 
that ran them. 

The implementation of this function moved to vice.singlezone.from_output and 
vice.multizone.from_output in version 1.1.0. To maintain backward compatibility, 
the call signature is remained intact. The call signature will be deprecated 
in version >= 2.0.0, and thus the necessary warning is raised. 
""" 

from __future__ import absolute_import 
from .._globals import VisibleDeprecationWarning 
from .singlezone import singlezone 
import warnings 


def mirror(arg): 
	"""
	[DEPRECATED] 

	Obtain an instance of either vice.singlezone or vice.multizone class 
	given only an instance of the vice.output class or the path to the output. 
	The returned object will have the same parameters as that which produced 
	the output, allowing re-simulation with whatever modifications the user 
	desires. 

	Signature: vice.mirror(arg) 

	Deprecation Notes 
	================= 
	This function is deprecated in versions >= 1.1.0 and will be removed in a 
	future relase of VICE. Users should instead call either 
	vice.singlezone.from_output or vice.multizone.from_output to achieve the 
	same functionality. 

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

	Deprecation Notes 
	================= 
	This function is deprecated in versions >= 1.1.0 and will be removed in a 
	future relase of VICE. Users should instead call either 
	vice.singlezone.from_output or vice.multizone.from_output to achieve the 
	same functionality. 

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

	""" 
	Developer's Notes 
	================= 
	The implementation of this function in versions >= 1.1.0 moved to the 
	vice.singlezone.from_output and vice.multizone.from_output class methods. 

	The signature of vice.mirror, however, is kept intact to maintain 
	backwards compatibility. 

	Either vice.singlezone.from_output and vice.multizone.from_output will 
	suffice - they are designed to recognize output from the opposite class and 
	return the correct version. The error handling can be left to them as well. 
	""" 
	warnings.warn("""\
The vice.mirror function is deprecated in versions >= 1.1.0 and will be \
removed in a future relase of VICE. Users should instead call either \
vice.singlezone.from_output or vice.multizone.from_output to achieve the same \
functionality.""", VisibleDeprecationWarning) 
	return singlezone.singlezone.from_output(arg) 

