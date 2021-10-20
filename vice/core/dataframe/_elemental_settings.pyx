# cython: language_level = 3, boundscheck = False
"""
This file handles the implementation of the elemental_settings subclass of the
VICE dataframe. These only allow __getitem__ via strings of elemental symbols
case-insensitively.
"""

from ..._globals import _VERSION_ERROR_
from ..._globals import _RECOGNIZED_ELEMENTS_
import numbers
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
	input = raw_input
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from . cimport _elemental_settings


#---------------------------- ELEMENTAL SETTINGS ----------------------------#
cdef class elemental_settings(base):

	r"""
	The VICE dataframe: derived class (inherits from base)

	Stores data on an element-by-element basis.

	Allowed Data Types
	------------------
	* Keys
		- ``str`` [case-insensitive] : elemental symbol
			The symbol of a chemical element as it appears on the periodic
			table.

	* Values
		- All

	Indexing
	--------
	- ``str`` [case-insensitive] : elemental symbol
		The symbol of a chemical element as it appears on the periodic table.

	Functions
	---------
	- keys
	- todict

	Example Code
	------------
	>>> import vice
	>>> vice.yields.ccsne.settings['o'] = 0.01
	>>> vice.yields.ccsne.settings['fe'] = 0.0012
	>>> vice.yields.sneia.settings['o'] = 0.0
	>>> vice.yields.sneia.settings['fe'] = 0.0017

	**Signature**: vice.core.dataframe.elemental_settings(frame)

	.. warning:: Users should avoid creating new instances of derived classes
		of the VICE dataframe and instead use the base class. Instances of
		this class are created automatically.

	Parameters
	----------
	frame : ``dict``
		A dictionary from which to construct the dataframe.
	name : ``str``
		String denoting a description of the values stored in this dataframe.
	"""

	def __init__(self, frame):
		# super will make sure frame is a dict whose keys are of type str
		super().__init__(frame)

		# Now make sure each keys is a recognized element
		for i in self.keys():
			if i.lower() not in _RECOGNIZED_ELEMENTS_:
				raise ValueError("Unrecognized element: %s" % (i))
			else:
				continue

	def __getitem__(self, key):
		if isinstance(key, strcomp):
			if key.lower() in self.keys():
				return self._frame[key.lower()]
			else:
				raise KeyError("Unrecognized element: %s" % (key))
		else:
			raise IndexError("Dataframe key must be of type str. Got: %s" % (
				type(key)))


	def __setitem__(self, key, value):
		if isinstance(key, strcomp):
			if key.lower() in _RECOGNIZED_ELEMENTS_:
				self._frame[key.lower()] = value
			else:
				raise TypeError("Unrecognized element: %s" % (key))
		else:
			raise TypeError("""Item assignment must be done via type str. \
Got: %s""" % (type(key)))


	def remove(self, key):
		"""
		This function throws a TypeError whenever called. This derived class
		of the VICE dataframe does not support item deletion.
		"""
		# Allowing this could let user's break their own singlezone objects
		raise TypeError("This dataframe does not support item deletion.")


	def filter(self, key, relation, value):
		"""
		This function throws a TypeError whenever called. This derived class
		of the VICE dataframe does not support filtering.
		"""
		raise TypeError("This dataframe does not support the filter function.")

