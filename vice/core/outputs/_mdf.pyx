# cython: language_level = 3, boundscheck = False 
""" 
This file implements the history function, which returns a fromfile object 
from a singlezone output. 
""" 

from __future__ import absolute_import 
from . import _output_utils 
from ..dataframe._fromfile cimport fromfile as fromfile_obj 


def mdf(name): 
	"""
	Read in the normalized stellar metallicity distribution functions at the 
	final timestep of the simulation. 

	Signature: vice.mdf(name) 

	Parameters 
	========== 
	name :: str 
		The name of the simulation to read output from, with or without the 
		'.vice' extension. 

	Returns 
	=======
	zdist :: VICE dataframe 
		A VICE dataframe containing the bin edges and the values of the 
		normalized stellar metallicity distribution in each [X/H] abundance 
		and [X/Y] abundance ratio. 

	Raises 
	====== 
	IOError :: [Occurs only if the output has been tampered with] 
		:: The output file is not found. 
		:: The output file is not formatted correctly. 
		:: Other VICE output files are missing from the output. 

	Notes 
	===== 
	For an output under a given name, this file will be stored under 
	name.vice/mdf.out, and it is a simple ascii text file with a comment header 
	detailing each column. By storing the output in this manner, user's may 
	analyze the results of VICE simulations in languages other than python. 

	VICE normalizes stellar metallicity distribution functions such that the 
	area under the user-specified binspace is equal to 1. Because of this, they 
	should be interpreted as probability densities. See section 6 of VICE's 
	science documentation at https://github.com/giganano/VICE/tree/master/docs 
	for further details. 

	If any [X/H] abundances or [X/Y] abundance ratios determined by VICE never 
	pass within the user's specified binspace, then the associated MDF will be 
	NaN at all values. 

	Because the user-specified bins that the stellar MDF is sorted into may 
	not be symmetric, if the simulation tracks the abundance ratios of stars in 
	[X/Y], the returned dataframe will not determine the distribution in the 
	inverse abundance ratio [Y/X] automatically. 

	Example 
	======= 
	>>> zdist = vice.mdf("example") 
	>>> zdist.keys() 
	    [“dn/d[sr/h],”,
	    “dn/d[sr/fe],”
	    “bin_edge_left,”
	    “dn/d[o/h],”
	    “dn/d[o/fe],”
	    “dn/d[fe/h],”
	    “bin_edge_right,”
	    “dn/d[o/sr]”]	
	>>> print("dN/d[O/Fe] in the 65th bin: %.2e" % (zdist["dn/d[o/fe]"][65])) 
	    dN/d[O/Fe] in the 65th bin: 1.41e-01 
	>>> [zdist[65]["bin_edge_left"], zdist[65]["bin_edge_right"]] 
	    [2.50e-01, 3.00e-01] 
	""" 
	return c_mdf(name) 



cdef fromfile_obj c_mdf(name): 
	""" 
	Returns a fromfile object for the MDF of a given output. 

	For details and documentation, see docstring of mdf function in this 
	file. 
	""" 
	name = _output_utils._get_name(name) 
	_output_utils._check_singlezone_output(name) 
	with open("%s/mdf.out" % (name), 'r') as f: 
		line = f.readline() 
		keys = [i.lower() for i in line.split()[1:]] 
		f.close() 
	return fromfile_obj(
		filename = "%s/mdf.out" % (name), 
		labels = keys
	)

