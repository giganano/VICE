# cython: language_level = 3, boundscheck = False
"""
This file scripts the mirror functionality of VICE, which takes in output 
objects and returns simulations with the same parameters that ran them. 
""" 

# Python imports 
from __future__ import absolute_import 
from ._pysinglezone import singlezone 
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


#----------------------------- MIRROR FUNCTION -----------------------------# 
def mirror(output_obj): 
	"""
	Obtain an instance of the vice.singlezone class given only an instance of 
	the vice.output class. The returned singlezone object will have the same 
	parameters as that which produced the output, allowing re-simulation with 
	whatever modifications the user desires. 

	Signature: vice.mirror(output_obj) 

	Parameters 
	========== 
	output_obj :: vice.output 
		Any vice.output object. 

	Returns 
	======= 
	sz :: vice.singlezone 
		A vice.singlezone object with the same attributes as that which 
		produced the given output. 

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
	>>> new.settings() 
	    Current Settings:
	    =================
	    tau_ia ---------> 1.5
	    recycling ------> continuous
	    Z_solar --------> 0.014
	    enhancement ----> 1.0
	    agb_model ------> cristallo11
	    RIa ------------> plaw
	    delay ----------> 0.15
	    IMF ------------> kroupa
	    smoothing ------> 0.0
	    schmidt_index --> 0.5
	    eta ------------> 2.5
	    Zin ------------> 0.0
	    schmidt --------> False
	    elements -------> (u’fe’, u’sr’, u’o’)
	    MgSchmidt ------> 6000000000.0
	    func -----------> <function _DEFAULT_FUNC at 0x1109e06e0> 
	    dt -------------> 0.01
	    tau_star -------> 2.0
	    name -----------> onezonemodel
	    m_lower --------> 0.08
	    m_upper --------> 100.0
	    Mg0 ------------> 6000000000.0
	    mode -----------> ifr
	    bins -----------> [-3, -2.95, -2.9, ... , 0.9, 0.95, 1]
	>>> import numpy as np 
	>>> new.run(np.linspace(0, 10, 1001)) 
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


