# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from . import _output_utils 
from ..pickles import pickled_object 
import os 
try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 
from ..dataframe._tracers cimport tracers as tracers_obj 


def tracers(name): 
	""" 
	Read in the part of a simulation's output that records the stellar 
	population tracer particles. 

	Signature: vice.tracers(name) 

	Parameters 
	========== 
	name :: str 
		The name of the output to read the stars from, with or without the 
		'.vice' extension. 

	Returns 
	======= 
	trace :: VICE dataframe 
		A VICE tracers object (a subclass of the VICE dataframe), which contains 
		the formation time and ages of star particles in Gyr, their original and 
		final zone numbers, and abundances. 

	Raises 
	====== 
	IOError :: [Only if the output has been tampered with] 
		::	The output files are not found 
		::	The output file is not formatted correctly 
		::	Other VICE output files are missing from the output 

	Notes 
	===== 
	For an output under a given name, the tracers file is stored under 
	name.vice/tracers.out, and is a simple ascii text file with a comment 
	header detailing each column. By storing the output in this manner, users 
	may analyze the results of VICE simulations in languages other than python. 

	Example 
	======= 
	>>> trace = vice.tracers("example") 
	>>> trace[100] 
	vice.dataframe{
		formation_time -> 0.5
		zone_origin ----> 0.0
		zone_final -----> 0.0
		mass -----------> 145745200.0
		z(fe) ----------> 0.0001267402
		z(sr) ----------> 2.264365e-09
		z(o) -----------> 0.0009258085
		[fe/h] ---------> -1.0076753221792103
		[sr/h] ---------> -1.3208319082438733
		[o/h] ----------> -0.7908748649989111
		[sr/fe] --------> -0.313156586064663
		[o/fe] ---------> 0.21680045718029917
		[o/sr] ---------> 0.5299570432449622
		z --------------> 0.0021020847164471383
		[m/h] ----------> -0.8234778210630218
		age ------------> 9.5
	} 
	""" 
	return c_tracers(name) 


cdef tracers_obj c_tracers(name): 
	""" 
	Returns a tracers object for a given output. 

	For details and documentation, see docstring of tracers function in this 
	file. 
	""" 
	name = _output_utils._get_name(name) 
	if _output_utils._is_multizone(name): 
		zone0 = list(filter(lambda x: x.endswith(".vice"), os.listdir(name)))[0] 
		adopted_solar_z = pickled_object.from_pickle(
			"%s/%s/attributes/Z_solar.obj" % (name, zone0) 
		) 
		return tracers_obj(filename = "%s/tracers.out" % (name), 
			adopted_solar_z = adopted_solar_z
		) 
	else: 
		raise IOError("Not a multizone output: %s" % (name)) 

