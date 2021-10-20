
from __future__ import absolute_import
from ._multioutput import c_multioutput
from . import _output_utils
import os

class multioutput:

	r"""
	Reads in the output from multizone simulations and allows the user to
	access it easily via dataframes.

	**Signature**: vice.multioutput(name)

	.. versionadded:: 1.2.0

	Parameters
	----------
	name : ``str``
		The full or relative path to the output directory. The '.vice'
		extension is not required.

	.. note:: If ``name`` corresponds to output from the ``singlezone`` class,
		an ``output`` object is created instead.

	Attributes
	----------
	name : ``str``
		The full or relative path to the output directory.
	zones : ``dataframe``
		A dataframe containing each zone's corresponding ``output`` object.
		The keys to this dataframe are the names of the ``singlezone`` objects
		contained in the ``multizone`` object which produced the output.
	stars : ``dataframe``
		A dataframe containing all star particle data.

	Example Code
	------------
	>>> import vice
	>>> example = vice.output("example")
	>>> example.name
		"example"
	>>> example.zones
		vice.dataframe{
			zone0 ----------> <VICE output from singlezone: example.vice/zone0>
			zone1 ----------> <VICE output from singlezone: example.vice/zone1>
			zone2 ----------> <VICE output from singlezone: example.vice/zone2>
			zone3 ----------> <VICE output from singlezone: example.vice/zone3>
			zone4 ----------> <VICE output from singlezone: example.vice/zone4>
			zone5 ----------> <VICE output from singlezone: example.vice/zone5>
			zone6 ----------> <VICE output from singlezone: example.vice/zone6>
			zone7 ----------> <VICE output from singlezone: example.vice/zone7>
			zone8 ----------> <VICE output from singlezone: example.vice/zone8>
			zone9 ----------> <VICE output from singlezone: example.vice/zone9>
		}
	>>> example.stars
		vice.dataframe{
			formation_time -> [0, 0, 0, ... , 10, 10, 10]
			zone_origin ----> [0, 1, 2, ... , 7, 8, 9]
			zone_final -----> [0, 1, 2, ... , 7, 8, 9]
			mass -----------> [3e+07, 3e+07, 3e+07, ... , 2.96329e+07, 2.96329e+07, 2.96329e+07]
			z(fe) ----------> [0, 0, 0, ... , 0.000846062, 0.000846062, 0.000846062]
			z(sr) ----------> [0, 0, 0, ... , 1.03519e-08, 1.03519e-08, 1.03519e-08]
			z(o) -----------> [0, 0, 0, ... , 0.0018231, 0.0018231, 0.0018231]
			[fe/h] ---------> [-inf, -inf, -inf, ... , -0.183187, -0.183187, -0.183187]
			[sr/h] ---------> [-inf, -inf, -inf, ... , -0.660756, -0.660756, -0.660756]
			[o/h] ----------> [-inf, -inf, -inf, ... , -0.496585, -0.496585, -0.496585]
			[sr/fe] --------> [nan, nan, nan, ... , -0.477569, -0.477569, -0.477569]
			[o/fe] ---------> [nan, nan, nan, ... , -0.313397, -0.313397, -0.313397]
			[o/sr] ---------> [nan, nan, nan, ... , 0.164171, 0.164171, 0.164171]
			z --------------> [0, 0, 0, ... , 0.0053307, 0.0053307, 0.0053307]
			[m/h] ----------> [-inf, -inf, -inf, ... , -0.419344, -0.419344, -0.419344]
			age ------------> [10, 10, 10, ... , 0, 0, 0]
		}
	"""

	def __new__(cls, name):
		r"""
		__new__ is overridden such that in the event of a singlezone object,
		an output object is returned.
		"""
		name = _output_utils._get_name(name)
		if _output_utils._is_multizone(name):
			return super(multioutput, cls).__new__(cls)
		else:
			from .output import output
			return output(name)

	def __init__(self, name):
		self.__c_version = c_multioutput(name)

	def __repr__(self):
		r"""
		Prints the name of the simulation
		"""
		return "<VICE multioutput from multizone: %s>" % (self.name)

	def __str__(self):
		r"""
		Returns self.__repr__()
		"""
		return self.__repr__()

	def __eq__(self, other):
		r"""
		Returns True if both multizone output objects come from the same
		directory
		"""
		if isinstance(other, multioutput):
			return os.path.abspath(self.name) == os.path.abspath(other.name)
		else:
			return False

	def __ne__(self, other):
		r"""
		Returns not self.__eq__(other)
		"""
		return not self.__eq__(other)

	def __enter__(self):
		r"""
		Opens a with statement
		"""
		return self

	def __exit__(self, exc_type, exc_value, exc_tb):
		r"""
		Raises all exceptions inside with statements
		"""
		return exc_value is None

	@property
	def name(self):
		r"""
		Type : ``str``

		The name of the ".vice" directory containing the output of a
		``multizone`` object. The attributes of this object, its corresponding
		singlezone outputs, and their attributes, are all contained in this
		directory.

		Example Code
		------------
		>>> import vice
		>>> example = vice.multioutput("example")
		>>> example.name
			"example"
		"""
		return self.__c_version.name

	@property
	def zones(self):
		r"""
		Type : ``dataframe``

		The data for each simulated zone. The keys to this dataframe are the
		names of the ``singlezone`` objects contained in the ``multizone``
		object which produced the output.

		Example Code
		------------
		>>> import vice
		>>> example = vice.multioutput("example")
		>>> example.zones
			vice.dataframe{
				zone0 ----------> <VICE output from singlezone: example.vice/zone0>
				zone1 ----------> <VICE output from singlezone: example.vice/zone1>
				zone2 ----------> <VICE output from singlezone: example.vice/zone2>
				zone3 ----------> <VICE output from singlezone: example.vice/zone3>
				zone4 ----------> <VICE output from singlezone: example.vice/zone4>
				zone5 ----------> <VICE output from singlezone: example.vice/zone5>
				zone6 ----------> <VICE output from singlezone: example.vice/zone6>
				zone7 ----------> <VICE output from singlezone: example.vice/zone7>
				zone8 ----------> <VICE output from singlezone: example.vice/zone8>
				zone9 ----------> <VICE output from singlezone: example.vice/zone9>
			}
		>>> example.zones["zone0"].name
			"example.vice/zone0"
		"""
		return self.__c_version.zones

	@property
	def stars(self):
		r"""
		Type : ``dataframe``

		The data for the star particles of this simulation. This stores the
		formation time in Gyr of each particle, its mass, its formation and
		final zone numbers, and the metallicity by mass of each element in the
		simulation.

		Example Code
		------------
		>>> import vice
		>>> example = vice.multioutput("example")
		>>> example.stars
			vice.dataframe{
				formation_time -> [0, 0, 0, ... , 10, 10, 10]
				zone_origin ----> [0, 1, 2, ... , 7, 8, 9]
				zone_final -----> [0, 1, 2, ... , 7, 8, 9]
				mass -----------> [3e+07, 3e+07, 3e+07, ... , 2.96329e+07, 2.96329e+07, 2.96329e+07]
				z(fe) ----------> [0, 0, 0, ... , 0.000846062, 0.000846062, 0.000846062]
				z(sr) ----------> [0, 0, 0, ... , 1.03519e-08, 1.03519e-08, 1.03519e-08]
				z(o) -----------> [0, 0, 0, ... , 0.0018231, 0.0018231, 0.0018231]
				[fe/h] ---------> [-inf, -inf, -inf, ... , -0.183187, -0.183187, -0.183187]
				[sr/h] ---------> [-inf, -inf, -inf, ... , -0.660756, -0.660756, -0.660756]
				[o/h] ----------> [-inf, -inf, -inf, ... , -0.496585, -0.496585, -0.496585]
				[sr/fe] --------> [nan, nan, nan, ... , -0.477569, -0.477569, -0.477569]
				[o/fe] ---------> [nan, nan, nan, ... , -0.313397, -0.313397, -0.313397]
				[o/sr] ---------> [nan, nan, nan, ... , 0.164171, 0.164171, 0.164171]
				z --------------> [0, 0, 0, ... , 0.0053307, 0.0053307, 0.0053307]
				[m/h] ----------> [-inf, -inf, -inf, ... , -0.419344, -0.419344, -0.419344]
				age ------------> [10, 10, 10, ... , 0, 0, 0]
			}
		"""
		return self.__c_version.stars

