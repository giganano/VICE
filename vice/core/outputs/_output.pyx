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
from .. import pickles
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
		from ...yields import agb
		from ...yields import ccsne
		from ...yields import sneia
		self._agb_yields = self.__load_saved_yields("agb", agb.settings)
		self._ccsne_yields = self.__load_saved_yields("ccsne", ccsne.settings)
		self._sneia_yields = self.__load_saved_yields("sneia", sneia.settings)

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

	def __load_saved_yields(self, channel, yield_settings):
		"""
		Load the saved_yields object associated with a given enrichment
		channel from the output.

		Parameters
		==========
		channel :: str
			The name of the enrichment channel
		yield_settings :: dataframe
			The current yields settings for this enrichment channel

		Returns
		=======
		A reconstructed copy of the yield settings as a saved_yields object

		Raises
		======
		UserWarning ::
			::	Yields not saved with the output
		"""
		yields = pickles.jar.open("%s/yields/%s" % (self._name, channel))
		copy = {}
		for i in yields.keys():
			if yields[i] is None:
				warnings.warn("""\
%s %s yield not encoded with output. Assuming the current yield setting, \
which may not reflect the yield setting at the time the simulation was \
ran.""" % (channel, i), UserWarning)
				copy[i] = yield_settings[i]
			else:
				copy[i] = yields[i]
		return saved_yields(copy, channel)

