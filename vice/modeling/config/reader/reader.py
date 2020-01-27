""" 
This file implements the core reader function for config files in fitting 
observed data with VICE singlezone and multizone objects. 
""" 

from __future__ import absolute_import 
from ...._globals import _VERSION_ERROR_ 
from .fit import read_fit 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 

def read(filename): 
	""" 
	Reads the config file the user 
	""" 
	functions = {
		"fit": 		read_fit 
	}
	if isinstance(filename, strcomp): 
		with open(filename, 'r') as f: 
			line = f.readline() 
			while line != "": 
				if line.strip() == "" or line.strip()[0] == '#': 
					line = f.readline() 
					continue 
				else: 
					line = line.lower().strip().replace(" ", "").split(':') 
					if len(line) == 0: 
						continue 
					elif line[0] == "begin": 
						parameters = functions[line[1]](f) 
						f.close() 
						return parameters 
					else: 
						raise ValueError("""Config block must begin with the \
string 'begin' (case-insensitive).""") 
			f.close() 
	else: 
		raise TypeError("Argument must be of type str. Got: %s" % (
			type(filename)))	

