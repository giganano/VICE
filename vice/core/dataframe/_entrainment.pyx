# cython: language_level = 3, boundscheck = False
"""
This file implements the entrainment settings objects. Every enrichment
channel in every zone has a zone_entrainment object as an attribute. The data
stored here represent the mass fractions of various elements that are
retained by the interstellar medium of a galaxy in a given zone, the remainder
of which is added directly to outflows.
"""

# Python imports
from __future__ import absolute_import
from ..._globals import _RECOGNIZED_ELEMENTS_
from ..._globals import _VERSION_ERROR_
from ..._globals import _DIRECTORY_
from ..._globals import ScienceWarning
from .. import _pyutils
import math as m
import warnings
import numbers
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from . cimport _entrainment


cdef class channel_entrainment(elemental_settings):

	r"""
	The VICE dataframe: derived class (inherits from elemental_settings)

	Stores entrainment fractions for each element from a given enrichment
	channel. These numbers denote the mass fraction of that element produced
	by some enrichment channel which is retained by the interstellar medium,
	the remainder of which is added directly to an outflow.

	Allowed Data Types
	------------------
	* Keys
		- ``str`` [case-insensitive] : elemental symbols
			The symbols of the elements as they appear on the periodic table.

	* Values
		- real number : mass fraction
			The mass fraction of the element that is entrained. Must be
			between 0 and 1.

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
	>>> example = vice.singlezone(name = "example")
	>>> example.entrainment.ccsne['o'] = 0.9
	>>> example.entrainment.ccsne['fe'] = 0.95
	>>> example.entrainment.sneia['fe'] = 0.95

	**Signature**: vice.core.dataframe.entrainment(frame)

	.. warning:: Users should avoid creating new instances of derived classes
		of the VICE dataframe and instead use the base class. Instances of
		this class are created automatically by the ``singlezone`` object.

	Parameters
	----------
	frame : ``dict``
		A dictionary from which to construct the dataframe.
	"""

	def __init__(self, frame):
		# error handling in super
		super().__init__(frame)

	def __setitem__(self, key, value):
		if isinstance(key, strcomp):
			if key.lower() in _RECOGNIZED_ELEMENTS_:
				if isinstance(value, numbers.Number):
					if 0 <= value <= 1:
						self._frame[key.lower()] = float(value)
					else:
						raise ValueError("""Entrainment fraction must be \
between 0 and 1. Got: %g""" % (value))
				else:
					raise TypeError("""Entrainment fraction must be a \
real number. Got: %s""" % (type(value)))
			else:
				raise ValueError("Unrecognized element: %s" % (key))
		else:
			raise TypeError("""Item assignment must be done via type str. \
Got: %s""" % (type(key)))

