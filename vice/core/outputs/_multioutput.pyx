# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from .output import output
from . import _output_utils
import os
from . cimport _multioutput
from ..dataframe._base cimport base
from . cimport _tracers


cdef class c_multioutput:

	"""
	The C version of the multioutput object. Docstrings can be found in the
	python version in multioutput.py.
	"""

	def __init__(self, name):
		"""
		Args
		====
		name :: str
			The name of the output
		"""
		self._name = _output_utils._get_name(name)

		# Find the zones within the output directory
		zones = list(filter(lambda x: x.endswith(".vice"),
			os.listdir(self._name)))
		zones = [i[:-5] for i in zones]

		# Setup the zones as an instance of the VICE dataframe base class
		self._zones = base(dict(zip(
			zones,
			[output("%s/%s" % (self._name, i)) for i in zones]
		)))

		# setup the tracers attribute as a tracers object
		self._stars = _tracers.c_tracers(self._name)

	@property
	def name(self):
		"""
		Type :: str

		The name of the ".vice" directory containing the output of a
		multizone object. The ".vice" extension need not be specified with
		the name.
		"""
		return self._name[:-5]

	@property
	def zones(self):
		"""
		Type :: VICE dataframe

		The data for each simulated zone. The keys of this dataframe are the
		names of each zone, and these map onto the associated output objects.
		"""
		return self._zones

	@property
	def stars(self):
		"""
		Type :: VICE dataframe

		The data for the tracer particles of this simulation. This stores the
		formation time in Gyr of each particle, its mass, its formation and
		final zone numbers, and the metallicity by mass of each element in the
		simulation.
		"""
		return self._stars

