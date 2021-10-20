# cython: language_level = 3, boundscheck = False
"""
This file implements the noncustomizable dataframe, a subclass of the
elemental_settings object. These do not allow item assignment for any
element whatsoever. The only objects of this type are built-in data, and
hold either numerical values or lists.
"""

from ..._globals import _VERSION_ERROR_
import numbers
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from . cimport _noncustomizable


#-------------------- NONCUSTOMIZABLE DATAFRAME SUBCLASS --------------------#
cdef class noncustomizable(elemental_settings):

	r"""
	The VICE dataframe: derived class (inherits from elemental_settings)

	Stores data on an element-by-element basis that is not modifiable by the
	user.

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
	>>> vice.atomic_number['c']
		6
	>>> vice.solar_z['c']
		0.00236

	**Signature**: vice.core.dataframe.noncustomizable(frame)

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
	# cdef object _name

	def __init__(self, frame, name):
		super().__init__(frame)
		if isinstance(name, strcomp):
			self._name = name
		else:
			raise TypeError("Attribute 'name' must be of type str. Got: %s" % (
				type(name)))


	def __setitem__(self, key, value):
		"""
		Override the base __setitem__ function to throw a TypeError whenever
		this function is called.
		"""
		raise TypeError("This dataframe does not support item assignment.")

