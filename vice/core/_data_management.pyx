
# Python Functions
from __future__ import with_statement, division, unicode_literals
from builtins import str, range, map
from io import open
import _globals
import numbers
from ctypes import *

# C Functions
cimport _readers
from libc.stdlib cimport malloc, free
clib = pydll.LoadLibrary(u"%score/enrichment.so" % (_globals.DIRECTORY))

__all__ = [u"output"]

class output(object):

	"""
	CLASS: output
	=============
	A class designed explicitly for handling the output of the integrator class. 

	Attributes:
	===========
	history:			The output stored in name/history.out
	mdf:				The output stored in name/mdf.out
	name:				The name of the integration that produced the outputs

	Functions:
	==========
	show

	The history and mdf attributes are coded as dataframes. That is, they can 
	be indexed by either a string indicating a column label or by index, which 
	will return a line of the output file. For example:

		>>> import onezone as oz
		>>> out = oz.output("example")
		>>> out.history["mgas"]
		>>> out.history[14]
		>>> out.mdf["dN/[o/fE]"]

	Where we have purposefully made case errors in the last line to illustrate 
	that these data frames are case-insensitive. 

	Passing one of these strings to the show function will place that quantity 
	on a graph and use matplotlib's pyplot.show() function to immediately 
	display it for the user. 
	"""

	def __init__(self, name):
		"""
		Args:
		=====
		name:		The name of the output. This attribute is inherited from 
				the integrator class, and so it is initialized in the exact 
				same manner. See its docstring for details.
		"""
		self.name = name
		# labels = tuple(["time", "mgas", "mstar", "sfr", "ifr", "ofr", 
		# 	"mass(fe)", "mass(o)", "mass(sr)", "z(fe)", "z(o)", "z(sr)", 
		# 	"[fe/h]", "[o/h]", "[sr/h]", "[o/fe]", "[sr/fe]", "eta_0", "r"])
		self._history = _dataframe(u"%s/history.out" % (self._name), 
			self.__history_columns())
		# labels = tuple(["bins_left", "bins_right", "dn/d[fe/h]", "dn/d[o/h]", 
		# 	"dn/d[sr/h]", "dn/d[o/fe]", "dn/d[sr/fe]", "dn/d[sr/o]"])
		self._mdf = _dataframe(u"%s/mdf.out" % (self._name), 
			self.__mdf_columns())

	@property
	def name(self):
		"""
		The name of the integration that was ran. This is also the path to 
		its directory.
		"""
		return self._name

	@name.setter
	def name(self, char *value):
		self._name = value
		while self._name[-1] == u'/':
			self._name = self._name[:-1]

	@property
	def history(self):
		"""
		The dataframe that has been read in from the history output file of the 
		integration. 
		"""
		return self._history

	@property
	def mdf(self):
		"""
		The dataframe that has been read in from the mdf output file of the 
		integration.
		"""
		return self._mdf

	def show(self, key):
		"""
		Show the quantity within the output object referenced by its key. If 
		this is a parameter from the history output, it will be shown on a 
		graph plotted against time. If it a parameter from the mdf output, it 
		will show the corresponding stellar metallicity distribution function. 

		The user can also specify a key as y-x, in which case it will plot y 
		versus x. In this way the user can show tracks in abundance space. 
		For example:

		>>> import onezone as oz
		>>> out = oz.output("example")
		>>> out.show("[O/Fe]-[Fe/H]")

		The above will show the example integration's track in [O/Fe]-[Fe/H] 
		abundance space.
		"""
		try:
			import matplotlib.pyplot as plt
			import _mpl
		except ImportError:
			message = u"Error: could not import python package matplotlib. "
			message += u"Please install matplotlib and/or anaconda and "
			message += u"try again."
			raise ImportError(message)

		_mpl.set_params()
		fig = plt.figure(figsize = (7, 7))
		ax = fig.add_subplot(111, facecolor = u"white")
		# ax.ticklabel_format(useOffset = False, style = "plain")
		_mpl.set_frame(ax)

		if key.lower() in self._history.labels:
			ax.set_xlabel(u"t [Gyr]")
			ax.set_ylabel(key)
			ax.plot(self._history[u"time"][1:], self._history[key.lower()][1:], 
				c = u'k')
		elif self.__new_key_history(key) in self._history.labels:
			ax.set_xlabel(u"t [Gyr]")
			ax.set_ylabel(key)
			ax.plot(self._history[u"time"][1:], self._history[key.lower()][1:], 
				c = u'k')
		elif key.lower() in self._mdf.labels[2:]:
			ax.set_yscale(u"log")
			ax.set_xlabel(key[4:])
			ax.set_ylabel(key)
			xvals = list(map(lambda x, y: (x + y)/2., 
				self._mdf[u"bin_edge_left"], 
				self._mdf[u"bin_edge_right"]))
			ax.step(xvals, self._mdf[key.lower()], c = u'k')
		elif self.__flip_XoverY_mdf(key):
			if self.__new_key_mdf(key) in self._mdf.labels:
				ax.set_yscale(u"log")
				ax.set_xlabel(key[4:])
				ax.set_ylabel(key)
				xvals = list(map(lambda x, y: (-x + -y)/2., 
					self._mdf[u"bin_edge_left"], 
					self._mdf[u"bin_edge_right"]))
				ax.step(xvals, self._mdf[self.__new_key_mdf(key)], c = u'k')
			else:
				message = u"Metallicity distribution function not found in "
				message += u"output: %s" % (key)
				raise ValueError(message)
		elif key.lower() == u"tau_star":
			tstar = list(map(lambda x, y: 1.e-9 * x / y, self._history[u"mgas"], 
				self._history[u"sfr"]))
			ax.set_xlabel(u"t [Gyr]") 
			ax.set_ylabel(r"$\tau_{*} = M_{gas}/\dot{M}_{*}$ [Gyr]")
			ax.plot(self._history[u"time"][1:], tstar[1:], c = u'k')
		elif key.lower() == u"eta":
			eta = list(map(lambda x, y: x / y, self._history[u"ofr"], 
				self._history[u"sfr"]))
			ax.set_xlabel(u"t [Gyr]")
			ax.set_ylabel(r"$\eta = \dot{M}_{out}/\dot{M}_{*}$")
			ax.plot(self._history[u"time"][1:], eta[1:], c = u'k')
		elif u'-' in key.lower():
			if len(key.split(u'-')) != 2:
				message = u"Can only show tracks in 2-dimensional space.\n"
				message += u"Key: %s" % (key)
				raise ValueError(message)
			else:
				abundance_y = key.split(u'-')[0]
				abundance_x = key.split(u'-')[1]
				ax.set_xlabel(abundance_x)
				ax.set_ylabel(abundance_y)
				ax.plot(self._history[abundance_x][1:], 
					self._history[abundance_y][1:], 
					c = u'k')
		else:
			plt.clf()
			del plt
			raise KeyError(u"Unrecognized dataframe key: %s" % (key))

		if (ax.get_ylim()[1] - ax.get_ylim()[0]) < 0.5:
			mean = sum(ax.get_ylim()) / 2.
			ax.set_ylim([mean - 0.25, mean + 0.25])
		else:
			pass

		plt.show()
		del plt

	def __history_columns(self):
		"""
		Gets the column labels of output from the history file.
		"""
		with open(u"%s/history.out" % (self._name), 'rb') as f:
			line = f.readline()
			while line[0] == u'#' and line[:17] != u"# COLUMN NUMBERS:":
				line = f.readline().decode('utf-8')
			if line[0] == u'#':
				labels = []
				while line[0] == u'#':
					line = f.readline().decode('utf-8').split()
					labels.append(line[2].lower())
				f.close()
				return tuple(labels[:-1])
			else:
				f.close()
				message = u"Output history file appears to not be formatted "
				message += u"correctly: %s/history.out" % (self._name)
				raise IOError(message)

	def __mdf_columns(self):
		"""
		Gets the column labels of output from the MDF file.
		"""
		with open(u"%s/mdf.out" % (self._name), 'rb') as f:
			line = f.readline().decode('utf-8').split()
			f.close()
			if line[0] == u'#':
				return tuple(map(lambda x: x.lower(), line[1:]))
			else:
				message = u"Output MDF file appears to not be formatted "
				message += u"correctly."
				raise IOError(message)

	def __flip_XoverY_mdf(self, key):
		if key[:4].lower() == u"dn/d":
			return True
		else:
			return False

	def __new_key_mdf(self, key):
		element1 = key[4:].split(u'/')[0][1:]
		element2 = key[4:].split(u'/')[1][:-1]
		return u"dn/d[%s/%s]" % (element2.lower(), element1.lower())

	def __new_key_history(self, key):
		try:
			element1 = key.split(u'/')[0][1:]
			element2 = key.split(u'/')[1][:-1]
			return u"[%s/%s]" % (element2.lower(), element1.lower())
		except IndexError:
			return None




	

class _dataframe(object):

	"""
	A simple implementation of a dataframe for wrapping into the output class. 
	It will read in an output file immediately upon receiving the name of the 
	file, which is determined when the user passes the name of the integration 
	to the output class.

	Calling its attributes is case-insensitive.

	Direct access to this class by the user is discouraged lightly. It is 
	primarily built for access via the built-in attributes of the output class. 
	"""

	def __init__(self, filename, labels):
		self._filename = filename
		self.read(labels)
		self._labels = tuple(labels)
		# self.__drawn = False

	def __getitem__(self, value):
		if isinstance(value, str):
			if value.lower() in self._frame:
				return self._frame[value.lower()]
			else:
				try:
					return self.__XoverY(value)
				except ValueError:
					raise KeyError(u"Invalid dataframe key: %s" % (value))
		elif isinstance(value, numbers.Number):
			if value % 1 == 0:
				if value >= 0 and value < len(self._frame[self._labels[0]]):
					return [self._frame[i][value] for i in self._labels]
				else:
					raise IndexError(u"Index out of range: %d" % (value))
			else:
				raise ValueError(u"Indexing by number must be a valid integer.")
		else:
			message = u"Index must be either a string or integer. Got: %s" % (
				type(value))
			raise TypeError(message)

	def __call__(self, value):
		return self.__getitem__(value)

	def __setitem__(self, key, value):
		try:
			copy = value[:]
		except:
			message = u"Setting an item must be an array-like object of the "
			message += u"same length as the dataframe itself."
			raise TypeError(message)
		if all(list(map(lambda x: isinstance(x, numbers.Numbers), value))):
			if len(value) == len(self._frame[self._labels[0]]):
				if isinstance(key, str):
					self._frame[key] = value
				else:
					message = u"Can only set item based on column with key "
					message += u"of type string."
					raise TypeError(message)
			else:
				message = u"Mismatch in array size: must match that of "
				message += u"dataframe. Dataframe size: %d. Got: %d" % (
					len(self._frame[self._labels[0]]), len(value))
				raise ValueError(message)
		else:
			raise TypeError(u"Non-numerical value detected.")

	@property
	def filename(self):
		"""
		The name of the file that produced this dataframe.
		"""
		return self._filename

	@property
	def labels(self):
		"""
		The labels in the dataframe in the order they're presented when 
		indexed by row number (by an integer).
		"""
		return self._labels

	@property
	def table(self):
		"""
		Returns the dataframe in the form of a 2-D python list. The first 
		dimension will correspond to the line number of the output file, and 
		the second to the column number
		"""
		return [[self._frame[i][j] for i in self._labels] for j in list(range(
			len(self._frame[self._labels[0]])))]

	def read(self, labels):
		"""
		Reads in the dataframe given the column labels (not determined by the 
		user).
		"""
		cdef long flen = _readers.num_lines(self._filename)
		cdef int hlen = clib.header_length(self._filename)
		cdef int dim = _readers.dimension(self._filename, hlen)
		cdef double **contents = _readers.read_output(self._filename)
		if contents == NULL:
			raise IOError(u"File not found: %s" % (self._filename))
		else:
			self._frame = [[contents[i][j] for j in list(range(dim))] for i in 
				list(range(flen - hlen))]
			free(contents)
			cols = list(map(lambda x: __column(self._frame, x), 
				list(range(dim))))
			if len(labels) != dim:
				raise ValueError(u"Must have a label for each dimension.")
			else:
				self._frame = dict(zip([i.lower() for i in labels], cols))

	def __XoverY(self, key):
		element1 = key.split(u'/')[0][1:]
		element2 = key.split(u'/')[1][:-1]
		if u"[%s/h]" % (element1.lower()) not in self._labels:
			raise ValueError
		elif u"[%s/h]" % (element2.lower()) not in self._labels:
			raise ValueError
		else:
			return list(map(lambda x, y: x - y, 
				self._frame[u"[%s/h]" % (element1.lower())], 
				self._frame[u"[%s/h]" % (element2.lower())]
			))

# Returns a column from a 2-D python list
def __column(mat, ind):
	return [row[ind] for row in mat]

