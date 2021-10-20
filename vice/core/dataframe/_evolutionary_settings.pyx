# cython: language_level = 3, boundscheck = False
"""
This file implements a subclass of the elemental_settings object. All
settings are restricted to numerical values and callable functions accepting
one positional numerical value, which may represent any given quantity for
an arbitrary element x.
"""

from __future__ import absolute_import
from ..._globals import _VERSION_ERROR_
from ..._globals import _RECOGNIZED_ELEMENTS_
from .. import _pyutils
import numbers
import sys
if sys.version[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from . cimport _evolutionary_settings


#---------------------- EVOOLUTIONARY SETTINGS SUBCLASS ----------------------#
cdef class evolutionary_settings(elemental_settings):

	r"""
	The VICE dataframe: derived class (inherits from elemental_settings)

	Stores simulation parameters on an element-by-element basis which may or
	may not vary with time.

	Allowed Data Types
	------------------
	* Keys
		- ``str`` [case-insensitive] : elemental symbols
			The symbols of the elements as they appear on the periodic table.

	* Values
		- real number
			A constant which does not vary with time.

		- <function>
			Must accept time in Gyr as the only parameter, and return the
			value of this parameter at that time for a given element.

	Indexing
	--------
	- ``str`` [case-insensitive] : elemental symbols
		The symbols of the elements as they appear on the periodic table.

	Functions
	---------
	- keys
	- todict

	Example Code
	------------
	>>> import vice
	>>> example = vice.singlezone(name = "example", Zin = {})
	>>> example.Zin['o'] = 0.002
	>>> example.Zin['fe'] = lambda t: 0.001 * (t / 3)

	**Signature**: vice.core.dataframe.evolutionary_settings(frame, name)

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

		"""
		Now make sure that they're all either numerical values or functions of
		time.
		"""
		for i in self.keys():
			if isinstance(self._frame[i.lower()], numbers.Number):
				pass
			elif callable(self._frame[i.lower()]):
				_pyutils.args(self._frame[i.lower()], """Functional %s \
setting must take only one numerical parameter.""" % (self._name))
			else:
				raise TypeError("""%s setting must be either a numerical \
value or a callable function accepting one numerical parameter. Got: %s""" % (
					self._name, type(self._frame[i.lower()])))

	def __setitem__(self, key, value):
		if isinstance(key, strcomp):
			if key.lower() in _RECOGNIZED_ELEMENTS_:
				if isinstance(value, numbers.Number):
					self._frame[key.lower()] = float(value)
				elif callable(value):
					_pyutils.args(value, """Functional %s setting must \
accept only one numerical parameter.""" % (self._name))
					self._frame[key.lower()] = value
				else:
					raise TypeError("""%s setting must be either a numerical \
value or a function accepting one numerical parameter. Got: %s""" % (
						self._name, type(key)))
			else:
				raise ValueError("Unrecognized element: %s" % (key))
		else:
			raise TypeError("Dataframe key must be of type str. Got: %s" % (
				type(key)))

