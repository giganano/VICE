# cython: language_level = 3, boundscheck = False 
""" 
This file implements the output object, the class designed to read in, store, 
and handle output from the singlezone object. 
""" 

from __future__ import absolute_import 
from ..._globals import _VERSION_ERROR_ 
from ..._globals import ScienceWarning 
from . import _output_utils 
import warnings 
import pickle 
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
from . cimport _output 
from . cimport _history 
from . cimport _mdf 


cdef class c_output: 

	""" 
	The C version of the output object. Docstrings can be found in the python 
	version in output.py. 
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
		# Set the name with some forethought about the directory 
		self._name = _output_utils._get_name(name) 

		# Now pull in all of the output information 
		self._hist = _history.c_history(self.name) 
		self._mdf = _mdf.c_mdf(self.name) 
		self._elements = self._hist._load_elements() 

		# Read in the yield settings 
		# self.__load_ccsne_yields() 
		# self.__load_sneia_yields() 
		# self.__load_agb_yields() 

		from ...yields import agb 
		from ...yields import ccsne 
		from ...yields import sneia 
		self._agb_yields = self.__load_saved_yields( 
			"agb_yields.config", agb.settings, "AGB star" 
		) 
		self._ccsne_yields = self.__load_saved_yields(
			"ccsne_yields.config", ccsne.settings, "CCSN"
		) 
		self._sneia_yields = self.__load_saved_yields(
			"sneia_yields.config", sneia.settings, "SN Ia"
		) 

	@property 
	def name(self): 
		# docstring in python version 
		return self._name[:-5]

	@property
	def elements(self):
		# docstring in python version 
		return self._elements 

	@property
	def history(self):
		# docstring in python version 
		return self._hist 

	@property
	def mdf(self):
		# docstring in python version 
		return self._mdf 

	@property
	def ccsne_yields(self): 
		# docstring in python version 
		return self._ccsne_yields 

	@property
	def sneia_yields(self): 
		# docstring in python version 
		return self._sneia_yields 

	@property 
	def agb_yields(self): 
		# docstring in python version 
		return self._agb_yields 

	def show(self, key, xlim = None, ylim = None): 
		# docstring in python version 
		try: 
			import matplotlib as mpl 
		except (ModuleNotFoundError, ImportError): 
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
		if x_key == "mdf": 
			x = list(map(lambda x, y: (x + y) / 2., self._mdf["bin_edge_left"], 
				self._mdf["bin_edge_right"])) 
		else: 
			try: 
				x = self._hist[x_key.lower()] 
			except KeyError: 
				plt.clf() 
				del mpl
				del plt 
				raise KeyError("Unrecognized dataframe key: %s" % (x_key))

		# Find the y-values based on the history and mdf keys 
		if y_key.lower() in self._mdf.keys(): 
			y = self._mdf[y_key.lower()] 
		elif self.__flip_key_mdf(y_key) in self._mdf.keys(): 
			x = [-1 * i for i in x] 
			y = self._mdf[self.__flip_key_mdf(y_key).lower()] 
		else: 
			try: 
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

	def __load_saved_yields(self, config_filename, yield_settings, name): 
		""" 
		Loads the saved_yields object associated with a given enrichment 
		channel from the output. 

		Parameters 
		========== 
		config_filename :: str 
			The name of the file that stores the saved yields within the 
			output. 
		yield_settings :: str 
			The current yield settings for this enrichment channel. 
		name :: str 
			The name of the enrichment channel. 

		Returns 
		======= 
		A reconstructed copy of the yield settings as a saved_yield object 

		Raises 
		====== 
		IOError :: 
			::	File holding encoded settings not found 
		ScienceWarning :: 
			::	Functional yields not saved in the output 
		""" 
		if os.path.exists("%s/%s" % (self._name, config_filename)): 
			yields = pickle.load(
				open("%s/%s" % (self._name, config_filename), "rb") 
			) 
			if "dill" not in sys.modules: 
				if any([yields[i] is None for i in self.elements]): 
					lost = list(filter(
						lambda x: yields[x] is None, self.elements
					))
					msg = """\
Re-instancing functional yields from a VICE output requires the python \
package dill (installable via pip). The following elements tracked by this \
simulation will have a %s yield set to the current setting, which may not \
reflect the yield settings at the time of integration: """ % (name) 
					for i in lost: 
						yields[i] = yield_settings[i] 
						msg += "%s " % (i) 
					warnings.warn(msg, ScienceWarning) 
				else: pass # no functions anway, move on 
			else: pass # functions would've been read just fine 
			return saved_yields(yields, name) 
		else: 
			raise IOError("""%s yield settings not found for simulation: \
%s/%s""" % (name, self._name, config_filename)) 


# 	def __load_ccsne_yields(self): 
# 		"""
# 		Reads in the CCSNe yield settings from the output 

# 		These may have functional yield settings 
# 		"""
# 		if os.path.exists("%s/ccsne_yields.config" % (self._name)): 
# 			try: 
# 				"""
# 				If functional yields can't be read in, that indicates the 
# 				simulation was ran on a computer that had dill installed, but 
# 				is reading them in on a computer that does not have dill. 
# 				"""
# 				yields = pickle.load(open("%s/ccsne_yields.config" % (
# 					self._name), "rb"))
# 			except ImportError: 
# 				raise ImportError("""\
# This output has encoded functional yields, indicating that it was ran on a \
# system on which dill is installed (installable via pip). to read in this \
# VICE output, please either install dill or rerun the integration on this 
# machine if its parameters are known.""") 

# 			"""
# 			Check for forgotten functional attributes if the user doesn't have 
# 			dill 
# 			"""
# 			if any(list(map(lambda x: yields[x] == None, self._elements))): 
# 				"""
# 				Not the most elegant solution to needing an instance of a yield 
# 				dataframe here, but this doesn't cause nested import errors and 
# 				works in only one line. 
# 				"""
# 				from ...yields.ccsne import settings 
# 				message = """\
# Re-instancing functional yields from a VICE output requires the python \
# package dill (installable via pip). The following elements tracked by this \
# simulation will have a core-collapse yield set to the current setting, which \
# may not reflect the yield settings at the time of integration: """
# 				for i in self._elements: 
# 					if yields[i] == None: 
# 						yields[i] = settings[i]
# 						message += "%s " % (i) 
# 					else:
# 						continue 

# 				del settings
# 				warnings.warn(message, ScienceWarning)

# 			else:
# 				pass 

# 			# Cast as a non-customizable dataframe 
# 			self._ccsne_yields = saved_yields(yields, "CCSNe")  
# 		else:
# 			raise IOError("""Core-collapse yield settings not found for \
# simulation: %s/ccsne_yields.config""" % (self._name)) 

# 	def __load_sneia_yields(self): 
# 		"""
# 		Reads in the SN Ia yield settings from the output 

# 		These may have functional yield settings 
# 		"""
# 		if os.path.exists("%s/sneia_yields.config" % (self._name)): 
# 			try: 
# 				"""
# 				If functional yields can't be read in, that indicates the 
# 				simulation was ran on a computer that had dill installed, but 
# 				is reading them in on a computer that does not have dill. 
# 				"""
# 				yields = pickle.load(open("%s/sneia_yields.config" % (
# 					self._name), "rb"))
# 			except ImportError: 
# 				raise ImportError("""\
# This output has encoded functional yields, indicating that it was ran on a \
# system on which dill is installed (installable via pip). to read in this \
# VICE output, please either install dill or rerun the integration on this 
# machine if its parameters are known.""") 

# 			"""
# 			Check for forgotten functional attributes if the user doesn't have 
# 			dill 
# 			"""
# 			if any(list(map(lambda x: yields[x] == None, self._elements))): 
# 				"""
# 				Not the most elegant solution to needing an instance of a yield 
# 				dataframe here, but this doesn't cause nested import errors and 
# 				works in only one line. 
# 				"""
# 				from ...yields.sneia import settings 
# 				message = """\
# Re-instancing functional yields from a VICE output requires the python \
# package dill (installable via pip). The following elements tracked by this \
# simulation will have a type Ia supernova yield set to the current setting, \
# which may not reflect the yield settings at the time of integration: """
# 				for i in self._elements: 
# 					if yields[i] == None: 
# 						yields[i] = settings[i]
# 						message += "%s " % (i) 
# 					else:
# 						continue 

# 				del settings
# 				warnings.warn(message, ScienceWarning)

# 			else:
# 				pass 

# 			# Cast as a non-customizable dataframe 
# 			self._sneia_yields = saved_yields(yields, "SNe Ia")  
# 		else:
# 			raise IOError("""Type Ia supernova yield settings not found for \
# simulation: %s/ccsne_yields.config""" % (self._name)) 

