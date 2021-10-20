# cython: language_level = 3, boundscheck = False
"""
This file implements the yield_settings class, a subclass of the
elemental_settings object. Instances of this object store the user's
nucleosynthetic yields from core-collapse and type Ia supernove.
"""

from __future__ import absolute_import
from ..._globals import _DIRECTORY_
from ..._globals import _RECOGNIZED_ELEMENTS_
from ..._globals import _VERSION_ERROR_
from .. import _pyutils
import numbers
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
	encoded. In later versions of python 3, dill.dump must be called instead
	of pickle.dump. All cases can be taken care of by overriding the native
	pickle module and letting dill masquerade as pickle.
	"""
	import dill as pickle
except (ModuleNotFoundError, ImportError):
	pass
from . cimport _yield_settings


#------------------------- YIELD DATAFRAME SUBCLASS -------------------------#
cdef class yield_settings(elemental_settings):

	r"""
	The VICE dataframe: derived class (inherits from elemental_settings)

	Stores the current nucleosynthetic yield settings for different enrichment
	channels.

	.. note:: Modifying yield settings through these dataframes is equivalent
		to going through the vice.elements module.

	Allowed Data Types
	------------------
	* Keys
		- ``str`` [case-insensitive] : elemental symbols
			The symbols of the elements as they appear on the periodic table.

	* Values
		- real number : denote a constant, metallicity-independent yield.

		- <function> : Mathematical function describing the yield.
			Must accept the metallicity by mass :math:`Z` as the only
			parameter.

			.. note:: Functions of metallicity for yields of delayed
				enrichment channels (e.g. type Ia supernovae) can
				significantly increase the required integration time in
				simulations, especially for fine timestepping.

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
	- vice.yields.ccsne.settings
		The user's current nucleosynthetic yield settings for core collapse
		supernovae.
	- vice.yields.sneia.settings
		The user's current nucleosynthetic yield settings for type Ia
		supernovae.

	Example Code
	------------
	>>> from vice.yields.ccsne import settings as example
	>>> example["fe"] = 0.001
	>>> example["FE"] = 0.0012
	>>> def f(z):
		return 0.005 + 0.002 * (z / 0.014)
	>>> example["Fe"] = f

	**Signature**: vice.core.dataframe.yield_settings(frame, name,
	allow_funcs, config_field)

	.. warning:: Users should avoid creating new instances of derived classes
		of the VICE dataframe.

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
		directory whenever the user saved new default yield settings.
	"""

	# cdef object __defaults
	# cdef object _allow_funcs
	# cdef object _config_field

	def __init__(self, frame, name, allow_funcs, config_field):
		if "settings.config" in os.listdir("%syields/%s" % (_DIRECTORY_,
			config_field)):
			# load settings based on saved yields
			super().__init__(pickle.load(open("%syields/%s/settings.config" % (
				_DIRECTORY_, config_field), "rb")))
		else:
			# load what was passed
			super().__init__(frame)
		if isinstance(name, strcomp):
			self._name = name
		else:
			raise TypeError("Attribute 'name' must be of type str. Got: %s" % (
				type(name)))

		"""
		first argument to this function will always be the factory default
		yields. Save those as a private attribute.
		"""
		keys = tuple([i.lower() for i in frame.keys()])
		fields = tuple([frame[i] for i in frame.keys()])
		self.__defaults = dict(zip(keys, fields))

		# Other private attributes
		self._allow_funcs = allow_funcs
		self._config_field = config_field

	def __setitem__(self, key, value):
		if isinstance(key, strcomp):
			if key.lower() in _RECOGNIZED_ELEMENTS_:
				if isinstance(value, numbers.Number):
					# Numerical values are always allowed
					self._frame[key.lower()] = value
				elif callable(value):
					# functions aren't always allowed
					if self._allow_funcs:
						_pyutils.args(value, """Functional %s yield settings \
must take only one numerical parameter.""" % (self._name))
						self._frame[key.lower()] = value
					else:
						raise TypeError("""This dataframe does not support \
functional attributes.""")
				else:
					raise TypeError("""%s yield settings must be either \
numerical values or callable functions accepting one numerical parameter. \
Got: %s""" % (self._name, type(value)))
			else:
				raise ValueError("Unrecognized element: %s" % (key))
		else:
			raise TypeError("Dataframe key must be of type str. Got: %s" % (
				type(key)))

	def restore_defaults(self):
		r"""
		Restores the dataframe to its default parameters.

		**Signature**: x.restore_defaults()

		Parameters
		----------
		x : ``yield_settings``
			An instance of this class.

		Example Code
		------------
		>>> from vice.yields.ccsne import settings as example
		>>> example["fe"]
		0.000246
		>>> example["fe"] = 0.001
		>>> example.restore_defaults()
		>>> example["fe"]
		0.000246
		"""	
		if "settings.config" in os.listdir("%syields/%s" % (_DIRECTORY_,
			self._config_field)):
			self._frame = pickle.load(open(
				"%syields/%s/settings.config" % (_DIRECTORY_,
					self._config_field), "rb"))
		else:
			self._frame = dict(self.__defaults)

	def factory_settings(self):
		r"""
		Restores the dataframe to its factory defaults.

		**Signature**: x.factory_settings()

		.. tip:: To revert your nucleosynthetic yield settings back to the
			production defaults *permanently*, simply call ``x.save_defaults()``
			immediately following this function.

		Parameters
		----------
		x : ``yield_settings``
			An instance of this class

		Example Code
		------------
		>>> from vice.yields.ccsne import settings as example
		>>> example["fe"]
		0.001 # <--- previously saved preset
		>>> example.factory_settings()
		0.000246
		"""
		self._frame = dict(self.__defaults)

	def save_defaults(self):
		r"""
		Saves the current dataframe settings as the default values.

		**Signature**: x.save_defaults()

		Parameters
		----------
		x : ``yield_settings``
			An instance of this class.

		.. note:: Saving functional yields requires the package dill_, an
			extension to ``pickle`` in the python standard library. It is
			recommended that VICE users install dill_ >= 0.2.0.

			.. _dill: https://pypi.org/project/dill/

		Example Code
		------------
		>>> from vice.yields.ccsne import settings as example
		>>> example["fe"] = 0.001
		>>> example.save_defaults()
		
		After re-launching the python interpreter:

		>>> from vice.yields.ccsne import settings as example
		>>> example["fe"]
		0.001
		"""
		if "dill" in sys.modules:
			"""
			Regardless of the presence of callable functions, if dill is
			imported, go ahead and save.
			"""
			pickle.dump(self._frame, open("%syields/%s/settings.config" % (
				_DIRECTORY_, self._config_field), "wb"))
		elif all(map(lambda x: not callable(self._frame[x]), self.keys())):
			# nothing is callable anyway
			pickle.dump(self._frame, open("%syields/%s/settings.config" % (
				_DIRECTORY_, self._config_field), "wb"))
		else:
			raise TypeError("""\
Package 'dill' not found. At least one element is set to have a functional \
yield, and saving this requires dill (installable via pip). After installing \
dill and relaunching your python interpreter, these yields can be saved.""")

