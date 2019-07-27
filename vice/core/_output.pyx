# cython: language_level = 3, boundscheck = False 
"""
This file handles the history and mdf functions along with the output class. 
These features handle VICE output automatically so that the user need not do 
it themselves. 
""" 

from __future__ import absolute_import 

__all__ = ["history", "mdf", "output"] 
__all__ = [str(i) for i in __all__] 		# appease python 2 strings 

from .._globals import _DIRECTORY_ 
from .._globals import _VERSION_ERROR_ 
from .._globals import ScienceWarning 
from ._dataframe import history as _history 
from ._dataframe import fromfile 
from ._dataframe import saved_yields 
import math as m 
import warnings 
import inspect 
import numbers 
import pickle 
import atexit 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
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

	"""
	Format name off user's specification and make sure files are there. Then 
	pull the keys and adopted solar Z from the output, make a _history 
	object and return. 
	""" 
	name = _get_name(name) 
	_check_output(name) 
	keys = _history_keys("%s/history.out" % (name)) 
	try: 
		adopted_solar_z = pickle.load(open("%s/params.config" % (name), 
			"rb"))["Z_solar"]  
	except TypeError: 
		raise SystemError("""\
Error reading encoded parameters stored in output. It appears this output \
was produced in a version of python other than the current interpreter. \
""") 
	return _history("%s/history.out" % (name), adopted_solar_z, labels = keys) 


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

	"""
	Format name off user's specification and make sure files are there. Then 
	pull the keys from the file, construct a fromfile object, and return. 
	""" 
	name = _get_name(name) 
	_check_output(name) 
	with open("%s/mdf.out" % (name), 'r') as f: 
		line = f.readline() 
		keys = [i.lower() for i in line.split()[1:]] 
		f.close() 
	return fromfile("%s/mdf.out" % (name), labels = keys) 



#-------------- PRIVATE SUBROUTINES OF HISTORY AND MDF READERS --------------#
def _get_name(name): 
	"""
	Gets the name of a VICE output given the user-specified name. 
	""" 
	if isinstance(name, strcomp): 
		while name[-1] == '/': 
			# Remove the '/' at the end of a directory name 
			name = name[:-1] 
		# Recognize the forced '.vice' extension 
		if name.lower().endswith(".vice"): 
			name = "%s.vice" % (name[:-5]) 
		else: 
			name = "%s.vice" % (name) 
		return name 
	else: 
		raise TypeError("'name' must be of type string. Got: %s" % (
			type(name)))

def _check_output(name): 
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

def _history_keys(filename): 
	""" 
	Gets the column labels of output from the history file of a VICE singlezone 
	output. 
	""" 
	if os.path.exists(filename): 
		with open(filename, 'r') as f: 
			line = f.readline() 
			while line[0] == '#' and not line.startswith("# COLUMN NUMBERS:"): 
				# read until we get to the column labels 
				line = f.readline() 
			if line[0] == '#': 
				labels = [] 
				while line[0] == '#':		# just append each label 
					line = f.readline().split() 
					labels.append(line[2].lower()) 
				f.close() 
				return tuple(labels[:-1]) 
			else: 
				# bad formatting 
				f.close() 
				raise IOError("""Output history file not formatted correctly: \
%s""" % (filename)) 
	else: 
		raise IOError("Output history file not found: %s" % (filename)) 

def _load_elements(filename): 
	"""
	Gets the elements tracked by a singlezone simulation from the history 
	file of its output. 
	""" 
	elements = [] 
	for i in _history_keys(filename): 
		if i.startswith("mass("): 
			# Find elements based on those with columns of reported masses 
			elements.append("%s" % (i.split('(')[1][:-1].lower())) 
		else: 
			continue 
	return tuple(elements[:]) 


#------------------------------ OUTPUT OBJECT ------------------------------# 
cdef class output: 
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

	cdef object _hist 
	cdef object _mdf 
	cdef object _elements 
	cdef object _ccsne_yields 
	cdef object _sneia_yields 
	cdef object _name 

	def __init__(self, name): 
		"""
		Parameters 
		========== 
		name :: str 
			The name of the .vice directory containing the output. This can 
			also be the full path to the output directory. The '.vice' 
			extension need not be included. 
		"""
		# Set the name with some forethought about the directory 
		self._name = _get_name(name) 

		# Now pull in all of the output information 
		self._hist = history(self.name) 
		self._mdf = mdf(self.name) 
		self._elements = _load_elements("%s.vice/history.out" % (self.name)) 

		# Read in the yield settings 
		self.__load_ccsne_yields() 
		self.__load_sneia_yields() 

	def __repr__(self): 
		"""
		Prints the name of the simulation 
		"""
		return "<VICE output object from simulation: %s>" % (self._name[:-5]) 

	def __str__(self): 
		""" 
		Returns self.__repr__() 
		""" 
		return self.__repr__() 

	def __eq__(self, other): 
		""" 
		Returns True if the outputs point to the same simulation 
		""" 
		return os.path.abspath(self._name) == os.path.abspath(other._name) 

	def __ne__(self, other): 
		""" 
		Returns not self.__eq__(other) 
		""" 
		return not self.__eq__(other) 

	def __enter__(self): 
		""" 
		Opens a with statement 
		""" 
		return self 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		""" 
		Raises all exceptions inside with statements. 
		""" 
		return exc_value is None 

	@property 
	def name(self): 
		"""
		Type :: str 

		The name of the ".vice" directory containing the output of a 
		singlezone object. The ".vice" extension need not be specified with 
		the name. 
		"""
		return self._name[:-5]

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
		return self._hist 

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

	def show(self, key, xlim = None, ylim = None): 
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
		xlim :: array-like object containing two real numbers 
			The x-limits to impose on the shown plot 
		ylim :: array-like object containing two real numbers 
			The y-limits to impose on the shown plot 

		Raises 
		====== 
		KeyError :: 
			::	Key is not found in either history or mdf attributes 
		ImportError/ModuleNotFoundError :: 
			::	matplotlib version >= 2 is not found in the user's system. 
				(The ModuleNotFoundError is raised in python version >= 3.6.) 
		All other errors are raised by matplotlib.pyplot.show

		Notes 
		===== 
		This function is NOT intended to generate publication quality plots for 
		users. It is included purely as a convenience function for users to be 
		able to read in and immediately inspect the results of their 
		simulations in a plot with only a few lines of code. 

		Example 
		======= 
		>>> out = vice.output("example") 
		>>> out.show("dn/d[o/fe]") 
		>>> out.show("sfr") 
		>>> out.show("[o/fe]-[fe/h]") 
		"""	
		try: 
			import matplotlib as mpl 
		except (ImportError, ModuleNotFoundError): 
			# matplotlib not found 
			raise ModuleNotFoundError("""\
Matplotlib not found. This function requires matplotlib >= 2.0.0. \
""") 

		if int(mpl.__version__[0]) < 2: 
			warnings.warn("""\
This function requires matplotlib >= 2.0.0. Got: %s. This may cause this \
function to fail. Install matplotlib >= 2 to prevent this in the future. \
""" % (mpl.__version__), 
				DeprecationWarning)
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

		# Type check the key 
		if not isinstance(key, strcomp):
			message = "Argument must be of type str. Got: %s" % (type(key)) 
			raise TypeError(message)
		else:
			pass 

		# dark background, make a figure and axes 
		plt.style.use("dark_background") 
		fig = plt.figure() 
		if int(mpl.__version__[0]) < 2: 
			ax = fig.add_subplot(111, axisbg = "black") 
		else: 
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
		if x_key.lower() in self._hist.keys(): 
			x = self._hist[x_key.lower()]
		elif self.__flip_key_history(x_key) in self._hist.keys(): 
			x = [-1 * i for i in self._hist[x_key.lower()]] 
		elif x_key == "mdf": 
			x = list(map(lambda x, y: (x + y) / 2., self._mdf["bin_edge_left"], 
				self._mdf["bin_edge_right"])) 
		else: 
			try: 
				# One last shot in the dark before throwing a KeyError 
				x = self._hist[x_key.lower()] 
			except KeyError: 
				plt.clf() 
				del mpl
				del plt 
				raise KeyError("Unrecognized dataframe key: %s" % (x_key))

		# Find the y-values based on the history and mdf keys 
		if y_key.lower() in self._hist.keys(): 
			y = self._hist[y_key.lower()] 
		elif self.__flip_key_history(y_key) in self._hist.keys(): 
			y = self._hist[y_key.lower()] 
		elif y_key.lower() in self._mdf.keys(): 
			y = self._mdf[y_key.lower()] 
		elif self.__flip_key_mdf(y_key) in self._mdf.keys(): 
			x = [-1 * i for i in x] 
			y = self._mdf[self.__flip_key_mdf(y_key).lower()] 
		else: 
			try: 
				# One last shot in the dark before throwing a KeyError 
				y = self._hist[y_key.lower()]
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

		# do what we can with the specified limits, both x and y 
		if xlim is not None: 
			ax.set_xlim(xlim) 
		else: 
			pass 

		if ylim is not None: 
			ax.set_ylim(ylim) 
		elif (ax.get_ylim()[1] - ax.get_ylim()[0]) < 0.5: 
			# widen the axes if they're particularly narrow 
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
		if '/' in key: 
			element1 = key.split('/')[0][1:] 
			element2 = key.split('/')[1][:-1] 
			return "[%s/%s]" % (element2.lower(), element1.lower()) 
		else: 
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
			self._sneia_yields = saved_yields(
				pickle.load(open("%s/sneia_yields.config" % (self._name), 
					"rb")), "SNe Ia") 
		else: 
			raise IOError("""SNe Ia yield settings not found for simulation: \
%s/sneia_yields.config""" % (self._name)) 

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
				raise ImportError("""\
This output has encoded functional yields, indicating that it was ran on a \
system on which dill is installed (installable via pip). to read in this \
VICE output, please either install dill or rerun the integration on this 
machine if its parameters are known.""") 

			"""
			Check for forgotten functional attributes if the user doesn't have 
			dill 
			"""
			if any(list(map(lambda x: yields[x] == None, self._elements))): 
				"""
				Not the most elegant solution to needing an instance of a yield 
				dataframe here, but this doesn't cause nested import errors and 
				works in only one line. 
				"""
				from ..yields.ccsne import settings 
				message = """\
Re-instancing functional yields from a VICE output requires the python \
package dill (installable via pip). The following elements tracked by this \
simulation will have a core-collapse yield set to the current setting, which \
may not reflect the yield settings at the time of integration: """
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
			self._ccsne_yields = saved_yields(yields, "CCSNe")  
		else:
			raise IOError("""Core-collapse yield settings not found for \
simulation: %s/ccsne_yields.config""" % (self._name)) 


