"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 

This file handles file I/O of the built in AGB grids either for use in 
integrations or returning to the user 
"""

from __future__ import absolute_import
import inspect
import sys
import os
from ...core._globals import _DIRECTORY
from ...core._globals import _RECOGNIZED_ELEMENTS
from ...core._globals import _version_error
from ...core._yields import atomic_number 
PATH = "%sdata/_agb_yields/" % (_DIRECTORY)
if sys.version_info[0] == 3:
	from builtins import str
else:
	pass
	
if sys.version_info[0] == 2: 
	strcomp = basestring 
elif sys.version_info[0] == 3: 
	strcomp = str
else:
	_version_error()



#--------------------------- AGB YIELD GRID READER ---------------------------# 
def read_grid(filename):
	"""
	Reads in the yield grid given the filename
	"""
	grid = []
	with open(filename, 'r') as f: # Open the file 
		line = f.readline()
		while line != "":
			grid.append([float(i) for i in line.split()]) # attach each float 
			line = f.readline() # read the next line 
		f.close()		# close the file and return 
	return grid 




#-------------------------- AGB_YIELD_GRID FUNCTION --------------------------# 
def yield_grid(element, study = "cristallo11"):
	"""
	Returns the mass-metallicity yield grid for the element.

	Args:
	=====
	element:				An elemental symbol (case-insensitive)

	Kwargs:
	=======
	study = "Cristallo11":	A keyword denoting the AGB star yield study to use

	Returns:
	========
	A 3-element array
		returned[0]:		The 2D grid itself, which can be accessed by giving 
					indexing in the following manner:
					yield = returned[mass_index][z_index]
		returned[1]:		The masses on the grid sorted least to greatest
		returned[2]:		The metallicities on the grid sorted least to greatest

	Studies and their Keywords:
	===========================
	cristallo11:		Cristallo et al. (2011), ApJS, 197, 17
	karakas10:		Karakas et al. (2010), MNRAS, 403, 1413
	"""

	# Type check errors
	if not isinstance(element, strcomp): 
		message = "First argument must be of type string." 
		raise TypeError(message) 
	else:
		pass 
	if not isinstance(study, strcomp): 
		message = "Keyword Arg 'study' must be of type string." 
		raise TypeError(message) 
	else:
		pass

	# Study keywords to their full citations
	studies = {
		"cristallo11":		"Cristallo et al. (2011), ApJS, 197, 17", 
		"karakas10":		"Karakas (2010), MNRAS, 403, 1413"
	}

	# Value error checks
	if study.lower() not in studies: 
		message = "Unrecognized study: %s" % (study)
		raise ValueError(message)
	else:
		pass
	if element.lower() not in _RECOGNIZED_ELEMENTS: 
		message = "Unrecognized element: %s" % (element)
		raise ValueError(message)
	else:
		pass

	# The Karakas (2010) study didn't look at anything heavier than nickel 
	if study.lower() == "karakas10" and atomic_number[element.lower()] > 28:
		message = "The %s study did not report yields for elements " % (
			studies["karakas10"])
		message += "heavier than nickel."
		raise LookupError(message)
	else:
		pass

	# The full path to the file containing the yield grid 
	filename = "%s%s/%s.dat" % (PATH, study.lower(), element.lower())
	if os.path.exists(filename):
		grid = read_grid("%s%s/%s.dat" % (PATH, study.lower(), element.lower()))
		# Pull off the masses and metallicities on the grid 
		m = list(set([i[0] for i in grid]))
		z = list(set([i[1] for i in grid]))
		y = len(m) * [None]
		# Stitch together the yields into a new 2-D python list 
		for i in range(len(m)):
			arr = len(z) * [0.]
			for j in range(len(z)):
				# y[i][j] = grid[len(m) * i + j][2]
				arr[j] = grid[len(z) * i + j][2]
			y[i] = arr
		# return the grid 
		return [y, sorted(m), sorted(z)]
	else:
		"""
		File not found ---> unless VICE was tampered with, this shouldn't 
		happen 
		"""
		message = "Yield file not found. Please re-install VICE."
		raise IOError(message) 

