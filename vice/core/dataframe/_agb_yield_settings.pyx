# cython: language_level = 3, boundscheck = False
"""
This file implements the agb_yield_settings object, a subclass of the
yield_settings object. This object allows strings denoting tables for
built-in yield studies and functions of two real numbers, interpreted as
stellar mass in Msun and metallicity by mass.
"""

from ..._globals import _VERSION_ERROR_
from ..._globals import _RECOGNIZED_ELEMENTS_
import numbers
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from . cimport _agb_yield_settings


#------------------------ AGB YIELD SETTINGS SUBCLASS ------------------------#
cdef class agb_yield_settings(yield_settings):

	r"""
	The VICE dataframe: derived class (inherits from yield_settings)

	Stores the current nucleosynthetic yield settings for asymptotic giant
	branch (AGB) stars.

	.. versionadded:: 1.2.0

	.. note:: Modifying yield settings through these dataframes is equivalent
		to going through the vice.elements module.

	Allowed Data Types
	------------------
	* Keys
		- ``str`` [case-insensitive] : elemental symbols
			The symbols of the elements as they appear on the periodic table.

	* Values
		- ``str`` [case-insensitive] : keywords
			Denote a built-in table of net yields published in a
			nucleosynthesis study.

			Recognized Keywords:

				- "cristallo11" : Cristallo et al. (2011) [1]_
				- "karakas10" : Karakas (2010) [2]_
				- "ventura13" : Ventura et al. (2013) [3]_
				- "karakas16": Karakas & Lugaro (2016) [4]_; Karakas et al.
				  (2018) [5]_


		- <function> : Mathematical function describing the yield.
			Must accept the stellar mass in :math:`M_\odot` and the
			metallicity by mass :math:`Z` as parameters, in that order.

			.. note:: Functions of mass and metallicity to describe these
				yields can significantly increase the required integration
				time in simulations, especially for fine timestepping.

	Indexing
	--------
	- ``str`` [case-insensitive] : elemental symbols
		Must be indexed by the symbol of an element recognized by VICE as it
		appears on the periodic table.

	Functions
	---------
	- keys
	- todict
	- restore_defaults
	- factory_settings
	- save_defaults

	Built-In Instances
	------------------
	- vice.yields.agb.settings
		The user's current nucleosynthetic yield settings for asymptotic giant
		branch stars.

	Example Code
	------------
	>>> import math
	>>> from vice.yields.agb import settings as example
	>>> example["c"] = "karakas10"
	>>> def f(m, z):
		return 1e-3 * m * math.exp(-m / 2) * (z / 0.014)
	>>> example["C"] = f

	**Signature**: vice.core.dataframe.agb_yield_settings(frame, name,
	allow_funcs, config_field)

	.. warning:: Users should avoid creating new instances of derived classes
		of the VICE dataframe and instead use the base class. Instances of
		this class are created automatically.

	Parameters
	----------
	frame : ``dict``
		A dictionary from which to construct the dataframe.
	name : ``str``
		String denoting a description of the values stored in this dataframe.
	allow_funcs : ``bool``
		If True, functional attributes will be allowed.
	config_field : ``str``
		The name of the ".config" file that is stored in VICE's install
		directory whenever the user saves new default yield settings.

	.. [1] Cristallo et al. (2011), ApJS, 197, 17
	.. [2] Karakas (2010), MNRAS, 403, 1413
	.. [3] Ventura et al. (2013), MNRAS, 431, 3642
	.. [4] Karakas & Lugaro (2016), ApJ, 825, 26
	.. [5] Karakas et al. (2018), MNRAS, 477, 421
	"""

	def __init__(self, frame, name, allow_funcs, config_field):
		super().__init__(frame, name, allow_funcs, config_field)


	def __setitem__(self, key, value):
		# These import statements cause import errors when in the preamble
		from ...yields.agb._grid_reader import _RECOGNIZED_STUDIES_
		from ...yields.agb._grid_reader import _VENTURA13_ELEMENTS_
		from ._builtin_dataframes import atomic_number

		if isinstance(key, strcomp):
			if key.lower() in _RECOGNIZED_ELEMENTS_:
				if isinstance(value, strcomp):
					if value.lower() in _RECOGNIZED_STUDIES_:
						if (value.lower() == "karakas10" and
							atomic_number[key] > 28):
							# Karakas (2010) table only goes up to Ni.
							raise LookupError("""\
The Karakas (2010), MNRAS, 403, 1413 study did not report yields for elements \
heavier than nickel. Cannot assign "karakas10" as the element %s's AGB star \
yield setting.""" % (key.lower()))
						elif (value.lower() == "ventura13" and
							key.lower() not in _VENTURA13_ELEMENTS_):
							# Ventura tables only have a few elements
							raise LookupError("""\
The Ventura et al. (2013), MNRAS, 431, 3642 study did not report yields for \
the element %s. "ventura13" can be assigned as the AGB star yield setting for \
only the following elements: %s""" % (key.lower(), str(_VENTURA13_ELEMENTS_)))
						else:
							self._frame[key.lower()] = value.lower()
					else:
						raise ValueError("""Unrecognized AGB star yield \
study: %s""" % (value))

				elif callable(value):
					# Callable function -> store a copy of it if it passes
					try:
						# Try calling it at a typical mass and metallicity
						x = value(3, 0.01)
					except:
						raise TypeError("""AGB star yield settings, when \
callable, must accept two numerical parameters rather than one. The first \
argument is interpreted as the stellar mass in Msun and the second as the \
metallicity by mass Z.""")
					if isinstance(x, numbers.Number):
						self._frame[key.lower()] = value
					else:
						raise TypeError("""AGB star yield settings, when \
callable, must return a numerical value.""")
				else:
					raise TypeError("""Functional AGB star yield settings \
must be either a callable function accepting two numerical parameters or a
string denoting an AGB star yield study.""")
			else:
				raise ValueError("Unrecognized element: %s" % (key))
		else:
			raise TypeError("Dataframe key must be of type str. Got: %s" % (
				type(key)))

