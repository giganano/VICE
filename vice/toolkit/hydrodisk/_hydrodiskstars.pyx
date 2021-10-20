# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..._globals import _VERSION_ERROR_
from ..._globals import _DIRECTORY_
from ..._globals import ScienceWarning
from ...core import _pyutils
from ...core.dataframe import base as dataframe
import warnings
import numbers
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
# from libc.stdlib cimport srand
from libc.stdlib cimport malloc, free
from libc.string cimport strcpy, strcmp, strlen
from ...core._cutils cimport copy_pylist
from ...core._cutils cimport set_string
from . cimport _hydrodiskstars

# The end time of the simulation in Gyr (13.2 Gyr by default - hard coded)
_END_TIME_ = _hydrodiskstars.HYDRODISK_END_TIME

# The recognized hydrodiskstars migration modes
_RECOGNIZED_MODES_ = ["linear", "sudden", "diffusion"]

# The number of star particles in the simulation
# _N_STAR_PARTICLES_ = 3102519
_N_STAR_PARTICLES_ = 3152211


cdef class c_hydrodiskstars:

	"""
	The C-implementation of the hydrodiskstars object. See python version for
	documentation.
	"""

	def __cinit__(self, radbins, N = 1e5, mode = "diffusion", idcolumn = 0,
		tformcolumn = 1, rformcolumn = 2, rfinalcolumn = 3, zformcolumn = 4,
		zfinalcolumn = 5, v_radcolumn = 6, v_phicolumn = 7, v_zcolumn = 8,
		decomp_column = 9):

		# allocate memory for hydrodiskstars object in C and import the data
		self._hds = _hydrodiskstars.hydrodiskstars_initialize()
		datafilestem = "%stoolkit/hydrodisk/data/h277/" % (_DIRECTORY_)
		if isinstance(N, numbers.Number):
			if N % 1 == 0:
				_hydrodiskstars.seed_random()
				if N > _N_STAR_PARTICLES_:
					N = _N_STAR_PARTICLES_
					warnings.warn("""\
There are only %d star particles from the hydrodynamical simulation available \
for this object. Running a multizone model with this many stellar populations \
will oversample these data.""" % (_N_STAR_PARTICLES_), ScienceWarning)
				else: pass
				if not _hydrodiskstars.hydrodiskstars_import(self._hds,
					<unsigned long> N,
					datafilestem.encode("latin-1"),
					<unsigned short> idcolumn,
					<unsigned short> tformcolumn,
					<unsigned short> rformcolumn,
					<unsigned short> rfinalcolumn,
					<unsigned short> zformcolumn,
					<unsigned short> zfinalcolumn,
					<unsigned short> v_radcolumn,
					<unsigned short> v_phicolumn,
					<unsigned short> v_zcolumn,
					<unsigned short> decomp_column):
					raise SystemError("Internal Error.")
				else:
					pass
			else:
				raise ValueError("Keyword arg 'N' must be an integer.")
		else:
			raise TypeError("Keyword arg 'N' must be an integer.")
		self.radial_bins = radbins
		self.mode = mode

	def __init__(self, radbins, N = 1e5, mode = "linear", idcolumn = 0,
		tformcolumn = 1, rformcolumn = 2, rfinalcolumn = 3, zformcolumn = 4,
		zfinalcolumn = 5, v_radcolumn = 6, v_phicolumn = 7, v_zcolumn = 8,
		decomp_column = 9):
		
		self._analog_idx = -1l
		self.__update_analog_data()

	def __dealloc__(self):
		_hydrodiskstars.hydrodiskstars_free(self._hds)

	def __call__(self, zone, tform, time):
		if isinstance(zone, int):
			if 0 <= zone < self._hds[0].n_rad_bins:
				birth_radius = (self._hds[0].rad_bins[zone] +
					self._hds[0].rad_bins[zone + 1]) / 2
				if (isinstance(tform, numbers.Number) and
					isinstance(time, numbers.Number)):
					if time - _END_TIME_ > 1.e-12: warnings.warn("""\
Simulations of galactic chemical evolution with the hydrodiskstars object for \
timescales longer than %g Gyr are not supported. This is the maximum range of \
star particle ages.""" % (_END_TIME_), ScienceWarning)
					if tform == time:
						self._analog_idx = (
							_hydrodiskstars.hydrodiskstars_find_analog(
								self._hds[0], <double> birth_radius,
								<double> tform)
						)
						return zone
					else:
						if self.mode == "linear":
							bin_ = int(_hydrodiskstars.calczone_linear(
								self._hds[0], tform, birth_radius, _END_TIME_,
								self._analog_idx, <double> time))
						elif self.mode == "sudden":
							bin_ = int(_hydrodiskstars.calczone_sudden(
								self._hds[0], self._migration_time,
								birth_radius, self._analog_idx, <double> time))
						elif self.mode == "diffusion":
							bin_ = int(_hydrodiskstars.calczone_diffusive(
								self._hds[0], tform, birth_radius, _END_TIME_,
								self._analog_idx, <double> time))
						else:
							raise SystemError("Internal Error.")
						if bin_ != -1:
							return bin_
						else:
							raise ValueError("""\
Radius out of bin range. Relevant information:
Analog ID: %d
Zone of formation: %d
Time of formation: %.4e Gyr
Time in simulation: %.4e Gyr""" % (self.analog_data["id"][self.analog_index],
								zone, tform, time))
				else:
					raise TypeError("""Time parameters must be numerical \
values. Got: (%s, %s)""" % (type(tform), type(time)))
			else:
				raise ValueError("Zone out of range: %d" % (zone))
		else:
			raise TypeError("Zone must be of type int. Got: %s" % (type(zone)))

	def __update_analog_data(self):
		self._analog_data = dataframe({
			"id": 		[self._hds[0].ids[i] for i in range(
				self._hds[0].n_stars)],
			"tform":	[self._hds[0].birth_times[i] for i in range(
				self._hds[0].n_stars)],
			"rform": 	[self._hds[0].birth_radii[i] for i in range(
				self._hds[0].n_stars)],
			"rfinal": 	[self._hds[0].final_radii[i] for i in range(
				self._hds[0].n_stars)],
			"zform": 	[self._hds[0].zform[i] for i in range(
				self._hds[0].n_stars)],
			"zfinal": 	[self._hds[0].zfinal[i] for i in range(
				self._hds[0].n_stars)],
			"vrad": 	[self._hds[0].v_rad[i] for i in range(
				self._hds[0].n_stars)],
			"vphi": 	[self._hds[0].v_phi[i] for i in range(
				self._hds[0].n_stars)],
			"vz": 		[self._hds[0].v_z[i] for i in range(
				self._hds[0].n_stars)],
			"decomp": 	[self._hds[0].decomp[i] for i in range(
				self._hds[0].n_stars)]
		})

	def object_address(self):
		"""
		Returns the memory address of the HYDRODISKSTARS object in C.
		"""
		return <long> (<void *> self._hds)

	@property
	def radial_bins(self):
		# docstring in python version
		return [self._hds[0].rad_bins[i] for i in range(
			self._hds[0].n_rad_bins + 1)]

	@radial_bins.setter
	def radial_bins(self, value):
		value = _pyutils.copy_array_like_object(value)
		_pyutils.numeric_check(value, TypeError,
			"Non-numerical value detected.")
		value = sorted(value)
		if not value[-1] >= 20: raise ValueError("""\
Maximum radius must be at least 20 kpc. Got: %g""" % (value[-1]))
		if value[0] != 0: raise ValueError("""\
Minimum radius must be zero. Got: %g kpc.""" % (value[0]))
		self._hds[0].n_rad_bins = len(value) - 1
		if self._hds[0].rad_bins is not NULL: free(self._hds[0].rad_bins)
		self._hds[0].rad_bins = copy_pylist(value)

	@property
	def analog_data(self):
		# docstring in python version
		return self._analog_data

	@property
	def analog_index(self):
		# docstring in python version
		return self._analog_idx

	@property
	def mode(self):
		# docstring in python version
		if self._hds[0].mode is NULL:
			return None
		else:
			return "".join([chr(self._hds[0].mode[i]) for i in range(strlen(
				self._hds[0].mode))])

	@mode.setter
	def mode(self, value):
		"""
		Enforcement of only subclasses having mode = None handled in python
		as necessary.
		"""
		if isinstance(value, strcomp):
			if value.lower() in _RECOGNIZED_MODES_:
				if self._hds[0].mode is NULL:
					self._hds[0].mode = <char *> malloc (12 * sizeof(char))
				else: pass
				set_string(self._hds[0].mode, value.lower())
			else:
				raise ValueError("Unrecognized mode: %s" % (value))
		elif value is None:
			if self._hds[0].mode is not NULL: free(self._hds[0].mode)
			self._hds[0].mode = NULL
		else:
			raise TypeError("""Attribute 'mode' must be either a string or
None. Got: %s""" % (type(value)))


	def decomp_filter(self, values):
		values = _pyutils.copy_array_like_object(values)
		if all([_ % 1 == 0 for _ in values]):
			values = [int(_) for _ in values]
			copy = <unsigned short *> malloc (len(values) *
				sizeof(unsigned short))
			for i in range(len(values)): copy[i] = <unsigned short> values[i]
			if not _hydrodiskstars.hydrodiskstars_decomp_filter(self._hds,
				copy, <unsigned short> len(values)):
				raise SystemError("Internal Error.")
			else:
				self.__update_analog_data()
		else:
			raise TypeError("Must contain only integers.")

