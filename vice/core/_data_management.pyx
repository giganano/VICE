
# Python Functions
from __future__ import with_statement, division, unicode_literals
# from builtins import str, range, map, bytes
from io import open
import _globals
import numbers
from ctypes import *
import sys

# C Functions
cimport _readers
from libc.stdlib cimport malloc, free
clib = pydll.LoadLibrary("%score/enrichment.so" % (_globals.DIRECTORY))

__all__ = ["output"]

# This should always be caught at import anyway
def version_error():
	message = "Only Python versions 2.6, 2.7, and >= 3.3 are "
	message += "supported by VICE."
	raise SystemError(message)

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
		self._history = _dataframe("%s/history.out" % (self._name), 
			self.__history_columns())
		self._mdf = _dataframe("%s/mdf.out" % (self._name), 
			self.__mdf_columns())

	@property
	def name(self):
		"""
		The name of the integration that was ran. This is also the path to 
		its directory.
		"""
		return self._name

	@name.setter
	def name(self, value): 
		throw = False
		# Python 2.x string treatment
		if sys.version_info[0] == 2:
			if isinstance(value, basestring):
				self._name = value
				while self._name[-1] == '/':
					self._name = self._name[:-1]
			else:
				throw = True
		# Python 3.x string treatment
		elif sys.version_info[0] == 3:
			if isinstance(value, str):
				self._name = value
				while self._name[-1] == '/':
					self._name = self._name[:-1]
			else:
				throw = True
		else:
			# This should be caught at import anyway
			version_error()

		# TypeError
		if throw:
			message = "Attribute name must be of type string. Got: %s" % (
				type(value))
			raise TypeError(message)
		else:
			pass


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
			message = "Error: could not import python package matplotlib. "
			message += "Please install matplotlib and/or anaconda and "
			message += "try again."
			raise ImportError(message)

		_mpl.set_params()
		fig = plt.figure(figsize = (7, 7))
		ax = fig.add_subplot(111, facecolor = "white")
		# ax.ticklabel_format(useOffset = False, style = "plain")
		_mpl.set_frame(ax)

		if key.lower() in self._history.labels:
			ax.set_xlabel("t [Gyr]")
			ax.set_ylabel(key)
			ax.plot(self._history["time"][1:], self._history[key.lower()][1:], 
				c = 'k')
		elif self.__new_key_history(key) in self._history.labels:
			ax.set_xlabel("t [Gyr]")
			ax.set_ylabel(key)
			ax.plot(self._history["time"][1:], self._history[key.lower()][1:], 
				c = 'k')
		elif key.lower() in self._mdf.labels[2:]:
			ax.set_yscale("log")
			ax.set_xlabel(key[4:])
			ax.set_ylabel(key)
			xvals = list(map(lambda x, y: (x + y)/2., 
				self._mdf["bin_edge_left"], 
				self._mdf["bin_edge_right"]))
			ax.step(xvals, self._mdf[key.lower()], c = 'k')
		elif self.__flip_XoverY_mdf(key):
			if self.__new_key_mdf(key) in self._mdf.labels:
				ax.set_yscale("log")
				ax.set_xlabel(key[4:])
				ax.set_ylabel(key)
				xvals = list(map(lambda x, y: (-x + -y)/2., 
					self._mdf["bin_edge_left"], 
					self._mdf["bin_edge_right"]))
				ax.step(xvals, self._mdf[self.__new_key_mdf(key)], c = 'k')
			else:
				message = "Metallicity distribution function not found in "
				message += "output: %s" % (key)
				raise ValueError(message)
		elif key.lower() == "tau_star":
			tstar = list(map(lambda x, y: 1.e-9 * x / y, self._history["mgas"], 
				self._history["sfr"]))
			ax.set_xlabel("t [Gyr]") 
			ax.set_ylabel(r"$\tau_{*} = M_{gas}/\dot{M}_{*}$ [Gyr]")
			ax.plot(self._history["time"][1:], tstar[1:], c = 'k')
		elif key.lower() == "eta":
			eta = list(map(lambda x, y: x / y, self._history["ofr"], 
				self._history["sfr"]))
			ax.set_xlabel("t [Gyr]")
			ax.set_ylabel(r"$\eta = \dot{M}_{out}/\dot{M}_{*}$")
			ax.plot(self._history["time"][1:], eta[1:], c = 'k')
		elif '-' in key.lower():
			if len(key.split('-')) != 2:
				message = "Can only show tracks in 2-dimensional space.\n"
				message += "Key: %s" % (key)
				raise ValueError(message)
			else:
				abundance_y = key.split('-')[0]
				abundance_x = key.split('-')[1]
				ax.set_xlabel(abundance_x)
				ax.set_ylabel(abundance_y)
				ax.plot(self._history[abundance_x][1:], 
					self._history[abundance_y][1:], 
					c = 'k')
		else:
			plt.clf()
			del plt
			raise KeyError("Unrecognized dataframe key: %s" % (key))

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
		with open("%s/history.out" % (self._name), 'rb') as f:
			line = f.readline()
			while line[0] == '#' and line[:17] != "# COLUMN NUMBERS:":
				line = f.readline().decode('utf-8')
			if line[0] == '#':
				labels = []
				while line[0] == '#':
					line = f.readline().decode('utf-8').split()
					labels.append(line[2].lower())
				f.close()
				return tuple(labels[:-1])
			else:
				f.close()
				message = "Output history file appears to not be formatted "
				message += "correctly: %s/history.out" % (self._name)
				raise IOError(message)

	def __mdf_columns(self):
		"""
		Gets the column labels of output from the MDF file.
		"""
		with open("%s/mdf.out" % (self._name), 'rb') as f:
			line = f.readline().decode('utf-8').split()
			f.close()
			if line[0] == '#':
				return tuple(map(lambda x: x.lower(), line[1:]))
			else:
				message = "Output MDF file appears to not be formatted "
				message += "correctly."
				raise IOError(message)

	def __flip_XoverY_mdf(self, key):
		if key[:4].lower() == "dn/d":
			return True
		else:
			return False

	def __new_key_mdf(self, key):
		element1 = key[4:].split('/')[0][1:]
		element2 = key[4:].split('/')[1][:-1]
		return "dn/d[%s/%s]" % (element2.lower(), element1.lower())

	def __new_key_history(self, key):
		try:
			element1 = key.split('/')[0][1:]
			element2 = key.split('/')[1][:-1]
			return "[%s/%s]" % (element2.lower(), element1.lower())
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
		self._filename = filename.encode("latin-1")
		self.read(labels)
		self._labels = tuple(labels)
		# self.__drawn = False

	def __getitem__(self, value):
		if sys.version_info[0] == 2 and isinstance(value, basestring):
			if value.lower() in self._frame:
				return self._frame[value.lower()]
			else:
				try:
					return self.__XoverY(value)
				except ValueError:
					raise KeyError("Invalid dataframe key: %s" % (value))
		if sys.version_infor[0] == 3 and isinstance(value, str):
			if value.lower() in self._frame:
				return self._frame[value.lower()]
			else:
				try:
					return self.__XoverY(value)
				except ValueError:
					raise KeyError("Invalid dataframe key: %s" % (value))
		elif isinstance(value, numbers.Number):
			if value % 1 == 0:
				if value >= 0 and value < len(self._frame[self._labels[0]]):
					return [self._frame[i][value] for i in self._labels]
				else:
					raise IndexError("Index out of range: %d" % (value))
			else:
				raise ValueError("Indexing by number must be a valid integer.")
		else:
			message = "Index must be either a string or integer. Got: %s" % (
				type(value))
			raise TypeError(message)

	def __call__(self, value):
		return self.__getitem__(value)

	def __setitem__(self, key, value):
		try:
			copy = value[:]
		except:
			message = "Setting an item must be an array-like object of the "
			message += "same length as the dataframe itself."
			raise TypeError(message)
		if all(list(map(lambda x: isinstance(x, numbers.Numbers), value))):
			if len(value) == len(self._frame[self._labels[0]]):
				if isinstance(key, str):
					self._frame[key] = value
				else:
					message = "Can only set item based on column with key "
					message += "of type string."
					raise TypeError(message)
			else:
				message = "Mismatch in array size: must match that of "
				message += "dataframe. Dataframe size: %d. Got: %d" % (
					len(self._frame[self._labels[0]]), len(value))
				raise ValueError(message)
		else:
			raise TypeError("Non-numerical value detected.")

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
		# print("a")
		cdef long flen = _readers.num_lines(self._filename)
		# print("b")
		cdef int hlen = clib.header_length(self._filename)
		# print("c")
		cdef int dim = _readers.dimension(self._filename, hlen)
		# print("d")
		cdef double **contents = _readers.read_output(self._filename)
		# print("e")
		if contents == NULL:
			raise IOError("File not found: %s" % (self._filename))
		else:
			# print("f")
			self._frame = [[contents[i][j] for j in list(range(dim))] for i in 
				list(range(flen - hlen))]
			# print("g")
			free(contents)
			# print("h")
			cols = list(map(lambda x: __column(self._frame, x), 
				list(range(dim))))
			# print("i")
			if len(labels) != dim:
				raise ValueError("Must have a label for each dimension.")
			else:
				self._frame = dict(zip([i.lower() for i in labels], cols))

	def __XoverY(self, key):
		element1 = key.split('/')[0][1:]
		element2 = key.split('/')[1][:-1]
		if "[%s/h]" % (element1.lower()) not in self._labels:
			raise ValueError
		elif "[%s/h]" % (element2.lower()) not in self._labels:
			raise ValueError
		else:
			return list(map(lambda x, y: x - y, 
				self._frame["[%s/h]" % (element1.lower())], 
				self._frame["[%s/h]" % (element2.lower())]
			))

# Returns a column from a 2-D python list
def __column(mat, ind):
	return [row[ind] for row in mat]

