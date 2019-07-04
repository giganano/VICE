# cython: language_level=3, boundscheck=False
"""
This file handles file I/O of the built in AGB grids either for use in 
integrations or returning to the user 
"""

from __future__ import absolute_import
import inspect
import sys
import os
from ..._globals import _DIRECTORY_
from ..._globals import _RECOGNIZED_ELEMENTS_
from ..._globals import _VERSION_ERROR_
from ...core._dataframes import atomic_number 
PATH = "%syields/agb/" % (_DIRECTORY_)
if sys.version_info[0] == 3:
	from builtins import str
else:
	pass
	
if sys.version_info[0] == 2: 
	strcomp = basestring 
elif sys.version_info[0] == 3: 
	strcomp = str
else:
	_VERSION_ERROR_()



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
	Obtain the stellar mass-metallicity grid of fractional nucleosynthetic 
	yields from asymptotic giant branch (AGB) stars. VICE includes yields 
	from Cristallo et al. (2011), ApJS, 197, 17 and Karakas (2010), MNRAS, 403, 
	1413, allowing users the choice of which to adopt in their simulations. 

	Signature: vice.yields.agb.grid(element, study = "cristallo11") 

	Parameters
	==========
	element :: str [case-insensitive] 
		The symbol of the element to obtain the yield grid for. 
	study :: str [case-insensitive] [default :: "cristallo11"]
		A keyword denoting which AGB yield study to pull the yield table from. 
		Keywords and their Associated Studies: 
		--------------------------------------
		"cristallo11" :: Cristallo et al. (2011), ApJS, 197, 17 
		"karakas10" :: Karakas (2010), MNRAS, 403, 1413 

	Returns
	=======
	grid :: tuple (2-D)
		The yield grid itself; elements are tuples of fractional 
		nucleosynthetic yields at constant stellar mass, but varying 
		metallicity. It should be indexed with the rule: 
		arr[mass_index][z_index]
	masses :: tuple 
		The masses in terms of the sun that the yield grid is sampled on. 
	z :: tuple 
		The metallicities by mass Z on that the yield grid is sampled on. 

	Raises
	====== 
	ValueError :: 
		::	The study or the element are not built into VICE 
	LookupError :: 
		:: 	study == "karakas10" and the atomic number of the element is 
			greater than or equal to 29. The Karakas (2010), MNRAS, 403, 1413 
			study did not report yields from AGB stars for elements heavier 
			than nickel. 
	IOError :: [Occurs only if VICE's file structure has been tampered with] 
		:: 	The parameters passed to this function are allowed but the data 
			file is not found. 

	Example
	=======
	>>> y, m, z = vice.agb_yield_grid("sr") 
	>>> m 
	    (1.3, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0) 
	>>> z 
	    (0.0001, 0.0003, 0.001, 0.002, 0.003, 0.006, 0.008, 0.01, 0.014, 0.02) 
	>>> # the fractional yield from 1.3 Msun stars at Z = 0.001 
	>>> y[0][2] 
	    2.32254e-09

	References 
	========== 
	Cristallo et al. (2011), ApJS, 197, 17 
	Karakas (2010), MNRAS, 403, 1413 
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
	if element.lower() not in _RECOGNIZED_ELEMENTS_: 
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
		return [tuple([tuple(i) for i in y]), tuple(sorted(m)), tuple(sorted(z))]
	else:
		"""
		File not found ---> unless VICE was tampered with, this shouldn't 
		happen 
		"""
		message = "Yield file not found. Please re-install VICE."
		raise IOError(message) 

