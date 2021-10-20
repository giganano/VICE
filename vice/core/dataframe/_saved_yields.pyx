# cython: language_level = 3, boundscheck = False
"""
This file implements the saved_yields object, a subclass of the VICE dataframe
which is designed to hold saved nucleosynthetic yields. For that reason, it is
noncustomizable.
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
from . cimport _saved_yields


#--------------------------- SAVED YIELDS SUBCLASS ---------------------------#
cdef class saved_yields(noncustomizable):

	r"""
	The VICE dataframe: derived class (inherits from noncustomizable)

	Stores nucleosynthetic yield settings that were used in simulation. This
	is only a saved copy and is not modifiable by the user.

	.. seealso::
		- vice.core.dataframe.yield_settings
		- vice.yields.ccsne.settings
		- vice.yields.sneia.settings
		- vice.yields.agb.settings

	Allowed Data Types
	------------------
	* Keys
		- ``str`` [case-insensitive] : elemental symbol
			The symbol of a chemical element as it appears on the periodic
			table.

	* Values
		- real number
			A constant yield which does not vary with stellar mass or
			metallicity.

		- <function>
			A function of either one or two variables, depending on the
			enrichment channel. Core collapse and type Ia supernova yields
			will be function of metallicity, while asymptotic giant branch
			star yields will be functions of stellar mass and metallicity.

		- ``str``
			Keywords denoting a built-in table of yields sampled on a grid of
			stellar masses and metallicities. Only allowed for asymptotic
			giant branch star yields.

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
	>>> example = vice.output("example")
	>>> example.agb_yields
		vice.dataframe{
			fe -------------> cristallo11
			o --------------> cristallo11
			sr -------------> cristallo11
		}
	>>> example.ccsne_yields
		vice.dataframe{
			fe -------------> 0.000246
			o --------------> 0.00564
			sr -------------> 1.34e-08
		}

	**Signature**: vice.core.dataframe.saved_yields(frame, name)

	.. warning:: Users should avoid creating new instances of derived classes
		of the VICE dataframe and instead use the base class. Instances of
		this class are created automatically by the ``output`` object.

	Parameters
	----------
	frame : ``dict``
		A dictionary from which to construct the dataframe.
	name : ``str``
		String denoting a description of the values stored in this dataframe.
	"""

	def __init__(self, frame, name):
		super().__init__(frame, name)

		"""
		Saved yields will have already passed the necessary type-checking
		filters, so just make sure everything in the output looks okay. No
		need for _pyutils.args.
		"""
		for i in self.keys():
			if not (
				isinstance(self._frame[i.lower()], numbers.Number) or
				isinstance(self._frame[i.lower()], strcomp) or
				callable(self._frame[i.lower()])
			):
				raise TypeError("""%s yield setting must be either a \
numerical value, callable function, or string. Got: %s""" % (self._name,
					type(self._frame[i.lower()])))
			else:
				continue

