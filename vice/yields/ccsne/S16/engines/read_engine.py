r""" 
This file implements the function which reads an explodability engine from its 
file. 
""" 

from __future__ import absolute_import 
from ....._globals import _VERSION_ERROR_ 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 


def read(filename): 
	r""" 
	Reads in a file containing explodability engine data. 

	Parameters 
	----------
	filename : str 
		The name of the file to read in. 

	Returns 
	-------
	masses : list 
		The masses on which the explodability engine is sampled. 
	freq : list 
		The frequency with which stars of a given mass explode. 

	Raises
	------
	* IOError 
		- The file is not found. 
	""" 
	if isinstance(filename, strcomp): 
		if os.path.exists(filename): 
			masses = [] 
			freq = [] 
			with open(filename, 'r') as f: 
				f.readline() 
				line = f.readline() 
				while line != "": 
					line = [float(i) for i in line.split()] 
					masses.append(line[0]) 
					freq.append(line[1]) 
					line = f.readline() 
				f.close() 
			return [masses, freq] 
		else: 
			raise IOError("File not found: %s" % (filename)) 
	else: 
		raise TypeError("Must be of type str. Got: %s" % (type(filename))) 

