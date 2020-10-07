r""" 
Utility functions for running a given simulation suite. 

Contents 
--------
generate_output_tree : <function> 
	Create the directory tree to store the outputs in. 
""" 

import os 


def generate_output_tree(name): 
	r""" 
	Generates a directory tree in which to store the outputs for a given 
	simulation suite, the root being placed in the current working directory. 

	Parameters 
	----------
	name : str 
		The name of the simulation suite. 
	""" 
	if isinstance(name, str): 
		if not os.path.exists("outputs"): os.system("mkdir outputs") 
		os.system("mkdir outputs/%s" % (name)) 
		# Each SFE timescale prescription 
		for i in ["2Gyr", "1Gyr", "2Gyr_timedep", "1Gyr_timedep"]: 
			os.system("mkdir outputs/%s/%s" % (name, i)) 
			# Each migration model 
			for j in ["linear", "diffusion", "sudden", "post-process"]: 
				os.system("mkdir outputs/%s/%s/%s" % (name, i, j)) 
				# Each evolutionary history within this directory 
	else: 
		raise TypeError("Name must be of type str. Got: %s" % (type(name))) 

