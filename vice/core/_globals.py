
from __future__ import unicode_literals
import numbers
import sys
import os
if sys.version_info[0] == 3:
	from builtins import str
else:
	pass

__all__ = ["_DEFAULT_FUNC", "_DEFAULT_BINS", "solar_z", "sources", 
	"ccsne_yields", "sneia_yields", "DIRECTORY", "RECOGNIZED_ELEMENTS"]

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DIRECTORY = DIRECTORY[:-4] # removes 'core' to get full path to dir

RECOGNIZED_ELEMENTS = tuple([str(i) for i in ["fe", "o", "sr", "c"]])
RECOGNIZED_IMFS = tuple([str(i) for i in ["kroupa", "salpeter"]])

# The default function for an integration object. Defined here because it by 
# design has to be a pure python function and thus cannot be ran through the 
# cython integrator.
def _DEFAULT_FUNC(t):
	return 9.1

# The default stellar MDF bins for the integration object. 
def _DEFAULT_BINS():
	bins = 401 * [0.]
	for i in range(401):
		bins[i] = -3. + .01 * i
	return bins


class _case_insensitive_dataframe(object):

	"""
	An simple implementation of a Pandas-like dataframe that is keyed 
	like a python dictionary, except in a case-insensitive manner. It can 
	also be called like a function, and will return the same values in 
	either case.  

	An example, using some of the instances of this class that are 
	included in VICE: 

	>>> import vice
	>>> vice.solar_z["fe"]
	0.0012
	>>> vice.sources["O"]
	["CCSNE"]
	>>> vice.ccsne_yields("sR")
	4.43e-08
	"""

	def __init__(self, frame, name, customizable):
		self._frame = dict(frame)
		self._name = name
		self._customizable = customizable
		self.__defaults = dict(frame)

	def __getitem__(self, value):
		if value.lower() in self._frame:
			return self._frame[value.lower()]
		else:
			message = "Unrecognized %s: %s" % (self._name, value)
			raise KeyError(message)

	def __call__(self, value):
		return self.__getitem__(value)

	def __setitem__(self, key, value):
		if self._customizable:
			if key.lower() in self._frame:
				if isinstance(value, numbers.Number):
					self._frame[key] = float(value)
				else:
					raise TypeError("Value must be a numerical value.")
			else:
				raise ValueError("Unrecognized %s: %s" % (self._name, value))
		else:
			message = "This data structure does not support user-specified "
			message += "parameters."
			raise StandardError(message)

	@property
	def customizable(self):
		"""
		A boolean describing whether or not this data-structure supports 
		user-specified parameters. 
		"""
		return self._customizable

	def todict(self):
		"""
		Returns this objects as a standard python dictionary. Note that by 
		design, Python dictionaries are case-sensitive, and are thus less 
		versatile than this object. 
		"""
		return self._frame

	def restore_defaults(self):
		"""
		Restores the data structure to its default parameters.
		"""
		self._frame = self.__defaults


# Instances of the _case_insensitive_dataframe for both user lookup as well 
# as customization, depending on the instance. 
solar_z = _case_insensitive_dataframe({
	"fe":		0.0012, 
	"o":		0.0056, 
	"sr":		4.474e-8, 
	"c":		0.0024
	}, "element", False)
sources = _case_insensitive_dataframe({
	"fe":		["CCSNE", "SNEIA"], 
	"o":		["CCSNE"], 
	"sr":		["CCSNE", "AGB"], 
	"c":		["CCSNE", "AGB"]
	}, "element", False)
ccsne_yields = _case_insensitive_dataframe({
	"fe":		0.0012, # 3.61e-4
	"o":		0.015, # 0.0246
	"sr":		3.53e-8, # 2.86e08
	"c":		1.11e-2
	}, "element", True)
sneia_yields = _case_insensitive_dataframe({
	"fe":		0.0017, 
	"o":		0.0, 
	"sr":		0.0, 
	"c":		0.0
	}, "element", True)



