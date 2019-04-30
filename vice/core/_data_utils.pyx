"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 

This file handles the VICE dataframe and the outputs of the singlezone class. 
"""

# Python Functions 
from __future__ import division, unicode_literals, absolute_import 
from ._globals import _DIRECTORY_
from ._globals import _VERSION_ERROR_
from ._globals import ScienceWarning
import math as m 
import warnings 
import inspect 
import numbers 
import pickle 
import sys 
import os 
try: 
	# NumPy compatible but not NumPy dependent 
	import numpy as np 
except ImportError: 
	pass 
try: 
	# Pandas compatible but not Pandas dependent 
	import pandas as pd 
except ImportError: 
	pass 
try: 
	# dill for function encoding 
	import dill 
except ImportError: 
	pass 

# C Functions 
from ctypes import * 
from libc.stdlib cimport malloc, free 
clib = pydll.LoadLibrary("%ssrc/enrichment.so" % (_DIRECTORY_)) 

"""
<--------------- C routine comment headers not duplicated here --------------->

Conventionally these would be declared in a .pxd file and imported, but this 
is simpler when there are only four of them. 
"""
cdef extern from "../src/io.h":
	double **read_output(char *file)
	long num_lines(char *file)
	int file_dimension(char *file, int hlength)
	int header_length(char *file) 

if sys.version_info[0] == 2: 
	strcomp = basestring
elif sys.version_info[0] == 3: 
	strcomp = str 
else: 
	_VERSION_ERROR_() 

__all__ = ["mdf", "history", "output", "dataframe"] 
__all__ = [str(i) for i in __all__] # appease python 2 strings 



#------------- STELLAR METALLICITY DISTRIBUTION FUNCTION READER -------------#
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
	name = __get_name(name) # format the name off of the user's specification 
	__check_output(name) # make sure the files are there 

	data = __read_output("%s/mdf.out" % (name)) # read in the results 

	# pull the columns, stitch it into a dataframe, return, and call it a day 
	data = list(map(lambda x: [row[x] for row in data], range(len(data[0])))) 
	with open("%s/mdf.out" % (name), 'r') as f: 
		line = f.readline() 
		keys = [i.lower() for i in line.split()[1:]] 
		f.close() 
	return dataframe(dict(zip(keys, data))) 



#------------------------------ HISTORY READER ------------------------------#
def history(name): 
	"""
	Read in the part of a simulation's output that records the time-evolution 
	of the ISM metallicity. 

	Signature: vice.history(name) 

	Parameters
	==========
	name :: str 
		The name of the output to read the history from, with or without the 
		'.vice' extension. 

	Returns 
	======= 
	hist :: VICE dataframe 
		A VICE history object (a subclass of the VICE dataframe), which 
		contains the time in Gyr, gas and stellar masses in solar masses, star 
		formation and infall rates in Msun/yr, inflow and outflow 
		metallicities for each element, gas-phase mass and metallicities of 
		each element, and every [X/Y] combination of abundance ratios for each 
		output timestep. 

	Raises 
	====== 
	IOError :: [Only occurs if the output has been tampered with]  
		:: The output file is not found. 
		:: The output file is not formatted correctly. 
		:: Other VICE output files are missing from the output 

	Notes 
	===== 
	For an output under a given name, the history file is stored under 
	name.vice/history.out, and it is a simple ascii text file with a comment 
	header detailing each column. By storing the output in this manner, user's 
	may analyze the results of VICE simulations in languages other than 
	python. 

	In addition to the abundance and dynamical evolution information, history 
	objects will also record the effective recycling parameter and the 
	specified mass loading parameter at all times. These ar ethe actual 
	recycling rate divided by the star formation rate and the instantaneous 
	mass loading parameter \\eta that the user has specified regardless of the 
	smoothing time, respectively. 

	In addition to the keys present in history dataframes, users may also 
	index them with 'z' and '[m/h]' [case-insensitive]. This will determine 
	the total metallicity by mass as well as the logarithmic abundance 
	relative to solar. Both are scaled in the following manner: 

	Z = Z_solar * (\\sum_i Z_i / \\sum_i Z_i^solar) 

	This is the scaling of the total metallicity that is encoded into VICE's 
	timestep integrator, which prevents the simulation from behaving as if it 
	has a systematically low metallicity when enrichment is tracked for only 
	a small number of elements. See section 5.4 of VICE's science documentation 
	at https://github.com/giganano/VICE/tree/master/docs for further details. 

	Example 
	=======
	>>> history = vice.history("example") 
	>>> hist.keys() 
	    [“z(fe)”,
	    “mass(fe)”,
	    “[o/fe]”,
	    “z_in(sr)”,
	    “z_in(fe)”,
	    “z(sr)”,
	    “[sr/fe]”,
	    “z_out(o)”,
	    “mgas”,
	    “mass(sr)”,
	    “z_out(sr)”,
	    “time”,
	    “sfr”,
	    “z_out(fe)”,
	    “eta_0”,
	    “[o/sr]”,
	    “z(o)”,
	    “[o/h]”,
	    “ifr”,
	    “z_in(o)”,
	    “ofr”,
	    “[sr/h]”,
	    “[fe/h]”,
	    “r_eff”,
	    “mass(o)”,
	    “mstar”]
	>>> print ("[O/Fe] at end of simulation: %.2e" % (hist["[o/fe]"][-1])) 
	    [O/Fe] at end of simulation: -3.12e-01 
	"""
	name = __get_name(name) # format the name off of the user's specification 
	__check_output(name) # make sure the files are there 

	data = __read_output("%s/history.out" % (name)) # read in the results 

	# pull the columns, stitch it into a dataframe, return, call it a day 
	data = list(map(lambda x: [row[x] for row in data], range(len(data[0]))))
	keys = __history_keys("%s/history.out" % (name)) 
	return _history(dict(zip(keys, data)), 
		pickle.load(open("%s/params.config" % (name), "rb"))["z_solar"])




#-------------- PRIVATE SUBROUTINES OF HISTORY AND MDF READERS --------------#
def __get_name(name): 
	"""
	Gets the name of a VICE output given the user-specified name. 
	"""
	if isinstance(name, strcomp): # if it's a string 
		while name[-1] == '/': # remove the slash on the end of the directory 
			name = name[:-1] 
		if name[-5:].lower() != ".vice": 
			# If the extension is not on the end 
			return "%s.vice" % (name)
		else: 
			# If the extension is there, but maybe with case errors 
			return "%s.vice" % (name[:-5]) 
	else: 
		# If the name of an output isn't a string, it's a TypeError 
		raise TypeError("Parameter must be of type string. Got: %s" % (
			type(name)))

def __check_output(name): 
	"""
	Checks a VICE output to make sure all of the output files are there. 
	"""
	if not os.path.exists(name): # outputs not even there 
		raise IOError("VICE output not found: %s" % (name)) 
	elif not all(list(map(lambda x: x in os.listdir(name), 
		["history.out", "mdf.out", "ccsne_yields.config", "params.config", 
			"sneia_yields.config"]))): 
		# certain files aren't there 
		raise IOError("VICE output missing files: %s" % (name)) 
	else:
		# all good, proceed 
		pass 

def __read_output(filename): 
	"""
	Reads in results from VICE output and returns a 2-D python list table  
	"""
	filename = filename.encode("latin-1") # make it binary 
	cdef long flen = num_lines(filename) # file length 
	cdef int hlen = header_length(filename) # header length 
	cdef int dim = file_dimension(filename, hlen) # dimension 
	cdef double **contents = read_output(filename) # data 
	if contents == NULL: # C-routines return NULL if the file wasn't found 
		"""
		C file I/O routines return NULL if the file wasn't found. This should 
		be caught here, but this is included as a failsafe. 
		"""
		raise IOError("File not found: %s" % (filename)) 
	else: 
		# save the contents in Python 
		copy = [[contents[i][j] for j in range(dim)] for i in range(flen - hlen)] 
		free(contents) # Free the memory allocated by C 
		return copy

def __history_keys(filename): 
	"""
	Gets the column labels of output from the history file of a VICE output. 
	"""
	if os.path.exists(filename): 
		with open(filename, 'r') as f: # open the file 
			line = f.readline() # read the first line 
			while line[0] == '#' and line[:17] != "# COLUMN NUMBERS:": 
				# Find the column labels 
				line = f.readline() 
			if line[0] == '#': 
				labels = []
				while line[0] == '#': # simply append each label 
					line = f.readline().split()
					labels.append(line[2].lower()) 
				f.close() # close the file and return the labels
				return tuple(labels[:-1]) 
			else:
				# bad formatting
				f.close() 
				message = "Output history file appears to not be formatted "
				message += "correctly: %s" % (filename)
				raise IOError(message)
	else:
		message = "Output history file not found: %s" % (filename) 
		raise IOError(message) 

def __load_elements(filename): 
	"""
	Gets the elements tracked by a single-zone simulation from the history 
	file of its VICE output.  
	"""
	elements = [] 
	for i in __history_keys(filename): 
		if "mass(" in i: 
			# Find the elements based on those with columns "mass(x)" 
			elements.append("%s" % (i.split('(')[1][:-1].lower())) 
		else:
			continue 
	# return the strings for each element
	return tuple(elements[:]) 	





#------------------------------ OUTPUT OBJECT ------------------------------# 
class output(object): 

	"""
	Reads in the output from the singlezone class and allows the user to access 
	it easily via VICE dataframes. The results are read in automatically. 

	Signature: vice.output.__init__(name)

	Attributes 
	==========
	name :: str 
		The name of the .vice directory containing the output of a singlezone 
		object. 
	elements :: tuple 
		The symbols of the elements whose enrichment was tracked by the 
		simulation. 
	history :: VICE dataframe 
		The abundances at all output times as well as the time-evolution of 
		the galaxy, such as the star formation rate, gas mass, and star 
		formation efficiency. 
	mdf :: VICE dataframe 
		The normalized stellar metallicity distribution function at the final 
		timestep of the simulation. 
	ccsne_yields :: VICE dataframe 
		The yield settings from core-collapse supernovae at the time the 
		simulation was ran. 
	sneia_yields :: VICE dataframe 
		The yield settings from type Ia supernovae at the time the simulation 
		was ran. 

	Functions 
	=========
	show :: 		Show a plot of a given quantity stored in the output 

	Notes 
	===== 
	Reinstancing functional attributes from VICE outputs requires the package 
	dill, an extension to pickle in the python standard library. It is 
	recommended that VICE users install dill if they have not already so that 
	they can make use of this feature; this can be done via 'pip install dill'. 

	VICE outputs are stored in directories with a '.vice' extension following 
	the name of the simulation assigned to the singlezone object that produced 
	it. Because the history and mdf outputs are stored in pure ascii text, this 
	allows users to open them in languages other than python while retaining 
	the ability to run <command> *.vice in a linux terminal to run operations 
	on all VICE outputs in a given directory. 

	See also 
	======== 
	vice.history 
	vice.mdf 
	"""
	def __init__(self, name): 
		"""
		Parameters
		==========
		name :: str 
			The name of the .vice directory containing the output. This can 
			also be the full path to the output directory. The '.vice' 
			extension need not be included. 
		"""
		self.name = name # Call the setter function 

		self._history = history(self.name) 
		self._mdf = mdf(self.name) 
		self._elements = __load_elements("%s.vice/history.out" % (self.name)) 

		# Read in the yield settings 
		self.__load_ccsne_yields() 
		self.__load_sneia_yields() 

	@property
	def name(self): 
		"""
		Type :: str 

		The name of the ".vice" directory containing the output of a 
		singlezone object. The ".vice" extension need not be specified with 
		the name. 
		"""
		return self._name[:-5]

	@name.setter
	def name(self, value): 
		if isinstance(value, strcomp): 
			self._name = value 
			while self._name[-1] == '/': 
				# Remove the '/' at the end of a directory name 
				self._name = self._name[:-1]
				# Recognize the forced ".vice" extension
			if self._name[-5:].lower() == ".vice": 
				self._name = "%s.vice" % (self._name[:-5]) 
			else:
				self._name = "%s.vice" % (self._name)
		else: 
			# If it's not a string it's a TypeError 
			message = "Attribute name must be of type string. Got: %s" % (
				type(value)) 
			raise TypeError(message) 

	@property
	def elements(self):
		""" 
		Type :: tuple 

		The symbols for the elements whose enrichment was modeled to produce 
		the output file. 
		"""
		return self._elements

	@property
	def history(self):
		"""
		Type :: dataframe 

		The dataframe read in via vice.history(name). 

		See Also
		======== 
		Function vice.history
		"""
		return self._history

	@property
	def mdf(self):
		"""
		Type :: dataframe 

		The dataframe read in via vice.mdf(name). 

		See Also 
		======== 
		Function vice.mdf 
		"""
		return self._mdf

	@property
	def ccsne_yields(self): 
		"""
		Type :: dataframe 

		A dataframe encoding the settings for nucleosynthetic yields from 
		core collapse supernovae at the time the simulation was ran. 

		See Also 
		======== 
		vice.yields.ccsne.settings 
		"""
		return self._ccsne_yields 

	@property
	def sneia_yields(self): 
		"""
		Type :: dataframe 

		A dataframe encoding the settings for nucleosynthetic yields from 
		type Ia supernovae at the time the simulation was ran. 

		See Also 
		======== 
		vice.yields.sneia.settings 
		"""
		return self._sneia_yields 

	def show(self, key): 
		""" 
		Show a plot of the given quantity referenced by a keyword argument. 

		Signature: vice.output.show(key) 

		Parameters 
		========== 
		key :: str [case-insensitive] 
			The keyword argument. If this is a quantity stored in the history 
			attribute, it will be plotted against time by default. Conversely, 
			if it is stored in the mdf attribute, it will show the 
			corresponding stellar metallicity distribution function. 

			Users can also specify an argument of the format key1-key2 where 
			key1 and key2 are elements of the history output. It will then 
			plot key1 against key2 and show it to the user. 

		Raises 
		====== 
		KeyError :: 
			::	Key is not found in either history or mdf attributes 
		ImportError :: 
			::	matplotlib version >= 2 is not found in the user's system. 

		Notes 
		===== 
		This function is NOT intended to generate publication quality plots for 
		users. It is included purely as a convenience function for users to be 
		able to read in and immediately inspect the results of their simulations 
		in a plot with only a few lines of code. 

		Example 
		======= 
		>>> out = vice.output("example") 
		>>> out.show("dn/d[o/fe]") 
		>>> out.show("sfr") 
		>>> out.show("[o/fe]-[fe/h]") 
		"""
		try: 
			import matplotlib as mpl
			# Version check on matplotlib
			if int(mpl.__version__.split('.')[0]) < 2: 
				message = "The current implementation of VICE's show function " 
				message += "requires matplotlib version >= 2." 
				ImportError(message) 
			else:
				pass 

			# Set the rcParams 
			import matplotlib.pyplot as plt 
			mpl.rcParams["errorbar.capsize"] = 5
			mpl.rcParams["axes.linewidth"] = 2
			mpl.rcParams["xtick.major.size"] = 16
			mpl.rcParams["xtick.major.width"] = 2 
			mpl.rcParams["xtick.minor.size"] = 8 
			mpl.rcParams["xtick.minor.width"] = 1 
			mpl.rcParams["ytick.major.size"] = 16
			mpl.rcParams["ytick.major.width"] = 2 
			mpl.rcParams["ytick.minor.size"] = 8 
			mpl.rcParams["ytick.minor.width"] = 1 
			mpl.rcParams["axes.labelsize"] = 30
			mpl.rcParams["xtick.labelsize"] = 25
			mpl.rcParams["ytick.labelsize"] = 25
			mpl.rcParams["legend.fontsize"] = 25
			mpl.rcParams["xtick.direction"] = "in"
			mpl.rcParams["ytick.direction"] = "in"
			mpl.rcParams["ytick.right"] = True
			mpl.rcParams["xtick.top"] = True
			mpl.rcParams["xtick.minor.visible"] = True
			mpl.rcParams["ytick.minor.visible"] = True
		except ImportError: 
			# Matplotlib not found 
			message = "Error: could not import python package matplotlib. "
			message += "Please install matplotlib and/or anaconda and "
			message += "try again."
			raise ImportError(message)

		if not isinstance(key, strcomp):
			message = "Argument must be of type str. Got: %s" % (type(key)) 
			raise TypeError(message)
		else:
			pass 

		# dark background, make a figure and axes 
		plt.style.use("dark_background") 
		fig = plt.figure() 
		ax = fig.add_subplot(111, facecolor = "black") 

		if '-' in key:  # if they've specified a the x-y axes 
			y_key = key.split('-')[0]
			x_key = key.split('-')[1]
			xlabel = x_key
			ylabel = y_key
		elif key[:4].lower() == "dn/d": # if it's an MDF 
			y_key = key.lower() 
			x_key = "mdf" 
			xlabel = key[4:]
			ylabel = key
		else: # default to showing against time 
			y_key = key
			x_key = "time"
			xlabel = "time [Gyr]"
			ylabel = key

		# Find the x-values based on the history and mdf keys 
		if x_key.lower() in self._history.keys(): 
			x = self._history[x_key.lower()]
		elif self.__flip_key_history(x_key) in self._history.keys(): 
			x = [-1 * i for i in self._history[x_key.lower()]] 
		elif x_key == "mdf": 
			x = list(map(lambda x, y: (x + y) / 2., self._mdf["bin_edge_left"], 
				self._mdf["bin_edge_right"])) 
		else: 
			try: 
				# One last shot in the dark before throwing a KeyError 
				x = self._history[x_key.lower()] 
			except KeyError:
				plt.clf() 
				del mpl
				del plt 
				raise KeyError("Unrecognized dataframe key: %s" % (x_key))

		# Find the y-values based on the history and mdf keys 
		if y_key.lower() in self._history.keys(): 
			y = self._history[y_key.lower()] 
		elif self.__flip_key_history(y_key) in self._history.keys(): 
			y = self._history[y_key.lower()] 
		elif y_key.lower() in self._mdf.keys(): 
			y = self._mdf[y_key.lower()] 
		elif self.__flip_key_mdf(y_key) in self._mdf.keys(): 
			x = [-1 * i for i in x] 
			y = self._mdf[self.__flip_key_mdf(y_key).lower()] 
		else: 
			try: 
				# One last shot in the dark before throwing a KeyError 
				y = self._history[y_key.lower()]
			except KeyError:
				plt.clf() 
				del mpl
				del plt 
				raise KeyError("Unrecognized dataframe key: %s" % (y_key)) 

		if x_key == "mdf": # Show MDFs in log-scale 
			ax.set_yscale("log") 
		else:
			pass 

		# set the axis labels and plot 
		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		ax.plot(x, y, c = 'w') 

		# Widen the axes if they're too narrow 
		if (ax.get_ylim()[1] - ax.get_ylim()[0]) < 0.5: 
			mean = sum(ax.get_ylim()) / 2. 
			ax.set_ylim([mean - 0.25, mean + 0.25]) 
		else:
			pass 

		# Show the plot, then call it a day when the user closes it 
		plt.tight_layout() 
		plt.show() 
		del mpl
		del plt 

	@staticmethod
	def __flip_key_history(key): 
		"""
		Returns [Y/X] if the user passes [X/Y], else it just spits the 
		key right back at them 
		"""
		try: 
			element1 = key.split('/')[0][1:]
			element2 = key.split('/')[1][:-1] 
			return "[%s/%s]" % (element2.lower(), element1.lower()) 
		except IndexError: 
			return key

	def __flip_key_mdf(self, key): 
		"""
		Does the same thing as __flip_key_history, but for MDF keys 
		"""
		if key[:4].lower() == "dn/d": 
			try: 
				return "dn/d%s" % (self.__flip_key_history(key[4:])) 
			except IndexError:
				return key 
		else:
			return key 

	def __load_sneia_yields(self): 
		"""
		Reads in the SNe Ia yield settings from the output 

		No functional attributes here ---> not supported by current version 
		of VICE. 
		"""	
		if os.path.exists("%s/sneia_yields.config" % (self._name)): 
			# Cast them as a dataframe 
			self._sneia_yields = _noncustomizable_dataframe(
				pickle.load(open("%s/sneia_yields.config" % (self._name), 
					"rb")))
		else: 
			message = "SNe Ia yield settings not found for simulation: " 
			message += "%s/sneia_yields.config" % (self._name) 
			raise IOError(message) 

	def __load_ccsne_yields(self): 
		"""
		Reads in the CCSNe yield settings from the output 

		These may have functional yield settings 
		"""
		if os.path.exists("%s/ccsne_yields.config" % (self._name)): 
			try: 
				"""
				If functional yields can't be read in, that indicates the 
				simulation was ran on a computer that had dill installed, but 
				is reading them in on a computer that does not have dill. 
				"""
				yields = pickle.load(open("%s/ccsne_yields.config" % (
					self._name), "rb"))
			except ImportError: 
				message = "This output has encoded functional yields, " 
				message += "indicating that it was ran on a system in which " 
				message += "dill is installed (installable via pip). To "
				message += "read in this VICE output, please either install "
				message += "dill or rerun the integration on this machinge if "
				message += "its parameters are known. " 
				raise ImportError(message) 

			"""
			Check for forgotten functional attributes if the user doesn't have 
			dill 
			"""
			if any(map(lambda x: yields[x] == None, self._elements)): 
				"""
				Not the most elegant solution to needing an instance of a yield 
				dataframe here, but this doesn't cause nested import errors and 
				works in only one line. 
				"""
				from ..yields.ccsne import settings
				message = "Re-instancing functional yields from a VICE output " 
				message += "requires the python package dill (included with "
				message += "anaconda). The following elements tracked by this "
				message += "output will have a core-collapse yield set to the " 
				message += "current default, which may not reflect the yield " 
				message += "settings at the time of integration: " 
				for i in self._elements: 
					if yields[i] == None: 
						yields[i] = settings[i]
						message += "%s " % (i) 
					else:
						continue 

				del settings
				warnings.warn(message, ScienceWarning)

			else:
				pass 

			# Cast as a non-customizable dataframe 
			self._ccsne_yields = _noncustomizable_dataframe(yields) 
		else:
			message = "Core-collapse yield settings not found for simulation: " 
			message += "%s/ccsne_yields.config" % (self._name) 
			raise IOError(message) 





#------------------------------ VICE DATAFRAME ------------------------------#
class dataframe(object): 
	
	"""
                                 The VICE Dataframe 
	==========================================================================
	Provides a means of storing data indexed by strings in a case-insensitive 
	manner. VICE includes several instances of this class at the global level, 
	some of which have features specific to their instance. Users may call 
	these dataframes as a function using parentheses rather than square 
	brackets and it will return the same thing. If a dataframe stores 
	array-like attributes, it may also be indexed via an integer to pull that 
	element from each field. 

	Signature: vice.dataframe.__init__(frame) 

	Functions
	=========
	keys		
	todict

	Yield Setting Dataframes 
	======================== 
	The following dataframes store the user's settings for nucleosynthetic 
	yields from core collapse and type Ia supernovae. 

	yields.ccsne.settings :: Yield settings from core collapse supernovae 
	yields.sneia.settings :: Yield settings from type Ia supernovae 

	Functions Associated with these Dataframes 
	------------------------------------------ 
	factory_defaults :: Revert to VICE's original defaults 
	restore_defaults :: Revert to user's specified defaults 
	save_defaults :: Save current settings as defaults 

	Other Built-in dataframes 
	========================= 
	VICE provides the following dataframes. 

	atomic_number
	------------- 
	Stores the number of protons in the nucleus of each of VICE's recognized 
	elements. By design, this dataframe does not support item assignment 

	solar_z 
	-------  
	Stores the abundance by mass of elements in the sun. By nature, this 
	dataframe does not support user customization. Solar abundances are 
	derived from Asplund et al. (2009) and have been converted to a mass 
	fraction via: 

		Z_x,sun = (mu_x)(X_sun)10^((X/H) - 12) 

	where mu_x is the mean molecular weight of the element in amu, X_sun is 
	the solar hydrogen abundance by mass, and (X/H) = log10(Nx/NH) + 12, 
	which is what Asplund et al. (2009) reports. These calculations adopt 
	X_sun = 0.73 as the solar hydrogen abundances, also from Asplund et al. 
	(2009). 

	sources 
	-------  
	Stores strings denoting what astronomers generally believe to be the 
	dominant enrichment channels for each element. These are included purely 
	for convenience, and are adopted from Johnson (2019). This dataframe does 
	not support user customization.

		Enrichment Channels 
		------------------- 
		"CCSNE" :: core collapse supernovae 
		"SNEIA" :: type Ia supernovae 
		"AGB" :: asymptotic giant branch stars 
		"NSNS" :: binary neutron star mergers / r-process 

	References 
	========== 
	Asplund et al. (2009), ARA&A, 47, 481 
	Johnson (2019), Science, 6426, 474 
	"""

	def __init__(self, frame): 
		"""
		Parameters 
		==========
		frame :: dict 
			A python dictionary to construct the dataframe from 
		"""
		try:
			keys = tuple([i.lower() for i in frame.keys()])
			fields = tuple([frame[i] for i in frame.keys()])
			self._frame = dict(zip(keys, fields))  
		except AttributeError: 
			message = "All VICE dataframe keys must be of type str." 
			raise TypeError(message) 

	def __call__(self, key): 
		"""
		Returns the same thing as the __getitem__ function ---> this allows the 
		user to call the dataframe and achieve the same effect 
		"""
		return self.__getitem__(key) 

	def __getitem__(self, key): 
		"""
		Key the dataframe on key.lower() ---> allows case-insensitivity
		Simply raise a KeyError if it's not in the dataframe. 
		If key is a number, return the key'th element of each actual key within 
		the dataframe. 

		All VICE dataframes will be square by construction ---> they are not 
		user-initializable from a simple import without hacking VICE's source 
		code. 
		"""
		if isinstance(key, strcomp): # If they're indexing by column label 
			if key.lower() in self.keys(): # If it's in the frame 
				return self._frame[key.lower()] 
			else: 
				# Otherwise KeyError
				raise KeyError("Unrecognized dataframe key: %s" % (key)) 

		elif isinstance(key, numbers.Number): # If they're indexing by number 
			if key % 1 == 0: # If it's an integer 
				try: 
					lengths = [len(self._frame[i]) for i in self.keys()] 
				except TypeError: 
					# This only works if every field is array-like 
					message = "This dataframe cannot be indexed by " 
					message += "key of type int ---> not all fields are " 
					message += "array-like." 
					raise IndexError(message) 

				# If it's within the range allowed by the minimum length 
				if abs(key) <= min(lengths) and key != min(lengths): 
					return dataframe(dict(zip(self.keys(), 
						[self._frame[i][int(key)] for i in self.keys()]
					)))
				else:
					# Otherwise it's an IndexError 
					raise IndexError("Index out of bounds: %d" % (int(key)))

			else: 
				# If it couldn't be interpreted as an integer 
				message = "Index must be interpreted as an integer. " 
				message += "Got: %s" % (type(key))
				raise IndexError(message)

		else: 
			# If it was neither an integer nor a string 
			message = "Only integers and strings are valid indeces. " 
			message += "Got: %s" % (type(key)) 
			raise IndexError(message) 

	def __setitem__(self, key, value):  
		"""
		Only allow a __setitem__ given a string. VICE makes it lower-case 
		under the hood to allow case-insensitivity 
		"""
		if isinstance(key, strcomp): 
			self._frame[key.lower()] = value 
		else: 
			message = "Item assignment key must be of type string. Got: %s" % (
				type(key)) 
			raise TypeError(message) 

	def __repr__(self): 
		"""
		Fancy print of the format: 
		vice.dataframe{ 
		    field1 --------> value1 
		    field_other ---> value2
		}
		"""	
		rep = "vice.dataframe{\n" 
		keys = self._frame.keys() 
		for i in keys: 
			rep += "    %s " % (i) 
			arrow = "" 
			# terminate each arrow at the same point 
			for j in range(15 - len(i)): 
				arrow += '-' 
			rep += "%s> %s\n" % (arrow, str(self._frame[i])) 
		rep += '}'
		return rep 

	def __str__(self): 
		# Same as __repr__ 
		return self.__repr__() 

	def keys(self): 
		"""
		Signature: vice.dataframe.keys() 

		Returns the dataframe keys in lower-case format. 
		"""
		return [i.lower() for i in self._frame.keys()] 

	def todict(self): 
		"""
		Signature: vice.dataframe.todict() 

		Returns the dataframe as a standard python dictionary. Note however 
		that python dictionaries are case-sensitive, and are thus less 
		versatile than this object. 
		"""
		return self._frame 




#------------------------- VICE DATAFRAME SUBCLASSES -------------------------#
class _noncustomizable_dataframe(dataframe): 


	def __init__(self, frame): 
		"""
		Parameters 
		==========
		frame :: dict 
			A python dictionary to construct the dataframe from 
		"""
		dataframe.__init__(self, frame) 
		keys = tuple([i.lower() for i in frame.keys()]) 
		fields = tuple([frame[i] for i in frame.keys()]) 
		self._frame = dict(zip(keys, fields)) 
		self.__doc__ = dataframe.__doc__ 

	def __setitem__(self, key, value): 
		"""	
		Throw a TypeError whenever this is called 
		"""	
		raise TypeError("This dataframe does not support item assignment.") 

	def __getitem__(self, key): 
		"""
		The instances of this class are meant to hold things like yield 
		settings for individual elements, so indexing by row number is 
		not supported. 
		"""
		if isinstance(key, strcomp): 
			if key.lower() in self.keys(): 
				return self._frame[key.lower()] 
			else: 
				raise KeyError("Unrecognized element: %s" % (key)) 
		else:
			raise KeyError("Dataframe key must be of type string. Got: %s" % ( 
				type(key)))



class _customizable_yield_table(dataframe): 

	def __init__(self, frame, allow_funcs, config_field): 

		"""
		Parameters 
		==========
		frame :: dict 
			A python dictionary to construct the dataframe from 
		"""

		"""
		The above docstring entered purely to keep the __init__ docstring 
		consistent across built-in dataframes. The following is the actual 
		docstring of this class: 

		Parameters
		==========
		frame :: dict 
			A python dictionary to construct the dataframe from 
		allow_funcs :: bool 
			A boolean describing whether or not functional attribute are allowed 
		config_field :: str 
			The name of the '.config' file that is stored whenever the user 
			saves new default yield settings. 
		"""

		if config_field == "foo": 
			# allows dummy dataframes to be passed under the hood 
			keys = tuple([i.lower() for i in frame.keys()]) 
			fields = tuple([frame[i] for i in frame.keys()]) 
			self._frame = dict(zip(keys, fields)) 
		elif "settings.config" in os.listdir("%syields/%s" % (_DIRECTORY_, 
			config_field)): 
			# If saved yields are found, load those 
			self._frame = pickle.load(open("%syields/%s/settings.config" % (
				_DIRECTORY_, config_field), "rb")) 
		else: 
			# Or else use the ones that were passed 
			keys = tuple([i.lower() for i in frame.keys()]) 
			fields = tuple([frame[i] for i in frame.keys()]) 
			self._frame = dict(zip(keys, fields)) 

		# Call super and save all of the attributes 
		dataframe.__init__(self, self._frame)
		keys = tuple([i.lower() for i in frame.keys()]) 
		fields = tuple([frame[i] for i in frame.keys()]) 
		self.__defaults = dict(zip(keys, fields))
		self._allow_funcs = allow_funcs 
		self._config_field = config_field 
		self.__doc__ = dataframe.__doc__ 

	def __setitem__(self, key, value): 
		if isinstance(key, strcomp): # If it's a string 
			if key.lower() in self.keys(): # Don't allow creation of new fields 
				if isinstance(value, numbers.Number): 
					# If it's a number, that's always allowed 
					self._frame[key.lower()] = value 
				elif callable(value): 
					# If it's a function, that's not always allowed 
					if self._allow_funcs: 
						# If they are, check that it only takes one parameter 
						if not self.__args(value): 
							self._frame[key.lower()] = value 
						else:
							message = "Functional yields must take only one " 
							message += "parameter, which will be interpreted " 
							message += "as the metallicity by mass Z." 
							raise TypeError(message) 
					else: 
						# If functions aren't allowed 
						message = "This dataframe does not support functional " 
						message += "attributes." 
						raise TypeError(message) 
				else:
					message = "Yield must be either a numerical value or a " 
					message += "callable function of metallicity by mass Z. "
					message += "Got: %s" % (type(value))  
					raise TypeError(message) 
			else: 
				message = "Unrecognized element: %s" % (key) 
				raise KeyError(message) 
		else: 
			# If the key isn't a string, it's a TypeError 
			message = "Dataframe key must be of type string. Got: %s" % (
				type(key)) 
			raise TypeError(message) 

	def restore_defaults(self): 
		"""
		Restores the dataframe to its default parameters. 
		"""
		if self._config_field == "foo": 
			raise TypeError("This dataframe does not support defaults.") 
		elif "settings.config" in os.listdir("%syields/%s" % (_DIRECTORY_, 
			self._config_field)): 
			self._frame = pickle.load(open("%syields/%s/settings.config" % (
				_DIRECTORY_, self._config_field), "rb")) 
		else: 
			self._frame = dict(self.__defaults) 

	def factory_settings(self): 
		"""
		Restores the dataframe to its factory defaults. If user's wish to 
		revert their presets as well, simply call save_defaults() 
		immediately after. 
		"""
		self._frame = dict(self.__defaults) 

	def save_defaults(self): 
		"""
		Saves the current dataframe settings as the default values. 

		Saving functional attributes requires dill, which is installable via 
		'pip install dill'. 
		"""	
		if "dill" in sys.modules: 
			"""
			Regardless of the presence of callable functions, if dill is 
			imported, go ahead and save
			"""
			pickle.dump(self._frame, open("%syields/%s/settings.config" % (
				_DIRECTORY_, self._config_field), "wb")) 
		elif all(list(map(lambda x: not callable(self._frame[x]), 
			self.keys()))): 
			# Dill is not imported, but nothing is callable anyway 
			pickle.dump(self._frame, open("%syields/%s/settings.config" % (
				_DIRECTORY_, self._config_field), "wb")) 
		else: 
			message = "Package 'dill' not found. At least one element is set " 
			message += "to have a functional yield, and saving that requires " 
			message += "dill (installable via pip). After installing dill and "
			message += "relaunching your python interpreter, these yields " 
			message += "can be saved." 
			raise TypeError(message) 

	@staticmethod
	def __args(func): 
		"""
		Returns True if the function passed to it takes more than one parameter 
		or any keyword/variable/default arguments.
		This function is copied from the singlezone class, which applies this 
		same prescription to functional attributes. 
		"""
		if sys.version_info[0] == 2: 
			args = inspect.getargspec(func) 
		elif sys.version_info[0] == 3: 
			args = inspect.getfullargspec(func) 
		else:
			_VERSION_ERROR_()
		if args[1] != None: 
			return True 
		elif args[2] != None: 
			return True 
		elif args[3] != None: 
			return True 
		elif len(args[0]) != 1: 
			return True 
		else:
			return False  



class _history(dataframe): 

	def __init__(self, frame, adopted_solar_z): 

		"""
		Parameters 
		==========
		frame :: dict 
			A python dictionary to construct the dataframe from 
		"""

		"""
		The above docstring entered purely to keep the __init__ docstring 
		consistent across built-in dataframes. Below is the actual 
		docstring: 

		Parameters
		==========
		frame :: dict 
			A python dictionary to construct the dataframe from 
		adopted_solar_z :: real number 
			The metallicity by mass Z of the sun that the user adopted in 
			their simulation
		"""

		"""
		Import the solar_z dataframe from the _dataframes file. Not the most 
		elegant solution to needing that here, but it works with only one line 
		and doesn't cause a nested import error. Store it as an attribute 
		then get rid of the global variable. 

		Otherwise just construct the dataframe, call super, and move on. 
		"""
		from ._dataframes import solar_z 
		self._solar_z = solar_z 
		del solar_z 
		self._adopted_solar_z = adopted_solar_z 
		keys = tuple([i.lower() for i in frame.keys()]) 
		fields = tuple([frame[i] for i in frame.keys()]) 
		self._frame = dict(zip(keys, fields))  
		self.__original_keys = self.keys()
		dataframe.__init__(self, frame) 
		self.__doc__ = dataframe.__doc__ 

	def __getitem__(self, key): 
		"""
		Get an item from the dataframe given a specific key 
		"""
		if isinstance(key, strcomp): # If they're indexing by string 
			if key.lower() in self.keys(): # If it's in the dataframe 
				return self._frame[key.lower()] # go ahead and return 
			elif key.lower() in ["[m/h]", "z"]: # special keys 
				# Add up the total metallicities 
				arr = len(self._frame[self.keys()[0]]) * [0.] 
				# The elements tracked by the simulation 
				elements = list(filter(lambda x: x[:2] == "z(", self.keys())) 
				elements = [i[2:-1] for i in elements]
				# Their solar abundances 
				solar = sum([self._solar_z[i] for i in elements])
				"""
				Add up the metallicity by mass of each element at each 
				output time. 
				"""
				for i in range(len(arr)): 
					for j in elements: 
						arr[i] += self._frame["z(%s)" % (j)][i] 
					# Divide by the total solar abundance of each element 
					arr[i] /= solar 

				if key.lower() == "z": 
					# Scale off of the solar abundance 
					return [self._adopted_solar_z * i for i in arr]
				elif key.lower() == "[m/h]": 
					# Take the log10 to turn it into a [M/H] measurement 
					return [m.log10(i) if i != 0 else -float("inf") for i in arr]
				else:
					raise SystemError("This shouldn't be raised.") 
			else: 
				try: 
					"""
					If it wasn't found, see if they want an abundance ratio 
					[Y/X] when the simulation tracked [X/Y]
					"""
					return self.__XoverY(key) 
				except ValueError: 
					raise KeyError("Invalid dataframe key: %s" % (key)) 


		elif isinstance(key, numbers.Number): # if they're indexing by number 
			if key % 1 == 0: # if it's interpretable as an int 
				try: 
					lengths = [len(self._frame[i]) for i in self.keys()] 
				except TypeError: 
					# This only works if every field is array-like 
					message = "This dataframe cannot be indexed by " 
					message += "key of type int ---> not all fields are " 
					message += "array-like." 
					raise IndexError(message) 

				# If it's within the range allowed by the minimum length 
				if abs(key) <= min(lengths) and key != min(lengths): 
					return dataframe(dict(zip(self.keys(), 
						[self._frame[i][int(key)] for i in self.keys()]
					)))
				else:
					# Otherwise it's an IndexError 
					raise IndexError("Index out of bounds: %d" % (int(key)))
			else: # Got a real number that isn't an integer 
				message = "Index must be interpreted as an integer. " 
				message += "Got: %s" % (type(key))
				raise IndexError(message)
		else: 
			# Not a number or string ---> TypeError 
			message = "Only integers and strings are valid indeces. " 
			message += "Got: %s" % (type(key)) 
			raise IndexError(message) 

	def __setitem__(self, key, value): 
		# NumPy and Pandas compatibility ---> convert them to lists 
		if "numpy" in sys.modules and isinstance(value, np.ndarray): 
			copy = value.tolist() 
		elif "pandas" in sys.modules and isinstance(value, pd.DataFrame): 
			copy = [i[0] for i in value.values.tolist()] 
		elif type(value) in [tuple, list]: 
			copy = list(value[:]) 
		else:
			"""
			If none of the previous if statements evaluate to true, throw a 
			TypeEror ---> it's probably not an array like object 
			"""
			message = "Item assignment must be a 1-D array-like object of the " 
			message += "same length as the dataframe itself." 
			raise TypeError(message) 

		if isinstance(key, strcomp): 
			# Must be of type string 
			if key.lower() not in self.__original_keys: 
				# Don't allow modification of fields determined by VICE  
				if len(copy) == len(self._frame[self.keys()[0]]): 
					self._frame[key.lower()] = copy[:]
				else: 
					# Must be of the same length as the other fields 
					message = "Mismatch in array size: must match that of " 
					message += "dataframe. Dataframe size: %d. Got: %d" % ( 
						len(self._frame[self.keys()[0]]), len(copy))
					raise ValueError(message) 
			else: 
				# User trying to modify field determined by VICE 
				message = "Dataframe quantities determined by VICE do not " 
				message += "support item assignment." 
				raise TypeError(message) 
		else: 
			# Tried to initialize with variable that wasn't a string 
			message = "Can only set item with key of type string. Got: %s" % (
				type(key)) 
			raise KeyError(message) 

	def __XoverY(self, key): 
		"""
		If the user asks for an abundance ratio [Y/X] when the integration 
		tracked [X/Y], this automatically attaches the minus sign to 
		convert from one to the other. This is not done for the MDF because 
		that involves flipping the bins, not the values of the MDF themselves 
		"""
		element1 = key.split('/')[0][1:]
		element2 = key.split('/')[1][:-1]
		if "[%s/h]" % (element1.lower()) not in self.keys(): 
			raise ValueError 
		elif "[%s/h]" % (element2.lower()) not in self.keys(): 
			raise ValueError 
		else:
			return list(map(lambda x, y: x - y, 
				self._frame["[%s/h]" % (element1.lower())], 
				self._frame["[%s/h]" % (element2.lower())]
			))



