# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import 
__all__ = ["hydrodiskstars"] 
from ..._globals import _VERSION_ERROR_ 
from ..._globals import _DIRECTORY_ 
from ...core import _pyutils 
from ...core.dataframe import base as dataframe 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from libc.stdlib cimport malloc, free 
from libc.string cimport strcpy, strcmp, strlen 
from ...core._cutils cimport copy_pylist 
from ...core._cutils cimport set_string 
from . cimport _hydrodiskstars 

# The end time of the simulation in Gyr 
_END_TIME_ = 12.8 


cdef class c_hydrodiskstars: 

	""" 
	The base hydrodiskstars object. See derived classes for more information. 
	""" 

	def __cinit__(self, radbins, tformcolumn = 1, rformcolumn = 2, 
		rfinalcolumn = 4): 
		self._hds = _hydrodiskstars.hydrodiskstars_initialize() 
		datafile = "%stoolkit/hydrodisk/data/UWhydro.dat" % (_DIRECTORY_) 
		if not _hydrodiskstars.hydrodiskstars_import(self._hds, 
			datafile.encode("latin-1"), 
			<unsigned short> tformcolumn, 
			<unsigned short> rformcolumn, 
			<unsigned short> rfinalcolumn): 
			raise IOError("Could not read file: %s" % (datafile)) 
		else: 
			pass 
		radbins = _pyutils.copy_array_like_object(radbins) 
		_pyutils.numeric_check(radbins, TypeError, 
			"Non-numerical value detected.") 
		radbins = sorted(radbins) 
		self._hds[0].n_rad_bins = <unsigned short> len(radbins) - 1 
		self._hds[0].rad_bins = copy_pylist(radbins) 

	def __init__(self, radbins, tformcolumn = 1, rformcolumn = 2, 
		rfinalcolumn = 4): 
		self._analog_idx = -1l 
		_hydrodiskstars.seed_random() 

	def __dealloc__(self): 
		_hydrodiskstars.hydrodiskstars_free(self._hds) 

	@property 
	def analog_data(self): 
		r""" 
		Type : dataframe 

		The star particle data from the hydrodynamical simulation. The 
		following keys map to the following data: 

			- tform:   The time the star particle formed in Gyr 
			- rform:   The radius the star particle formed at in kpc 
			- rfinal:  The radius the star particle ended up at in kpc 
		""" 
		return dataframe({
			"tform":	[self._hds[0].birth_times[i] for i in range(
				self._hds[0].n_stars)], 
			"rform": 	[self._hds[0].birth_radii[i] for i in range(
				self._hds[0].n_stars)], 
			"rfinal": 	[self._hds[0].final_radii[i] for i in range(
				self._hds[0].n_stars)] 
		})


cdef class c_linear(c_hydrodiskstars): 

	r""" 
	C-implementation of linear migration scheme. See python version for 
	docstrings. 
	""" 
	
	def __call__(self, zone, tform, time): 
		if isinstance(zone, int): 
			if 0 <= zone < self._hds[0].n_rad_bins: 
				birth_radius = (self._hds[0].rad_bins[zone] + 
					self._hds[0].rad_bins[zone + 1]) / 2 
				if tform == time: 
					self._analog_idx = (
						_hydrodiskstars.hydrodiskstars_find_analog(
							self._hds[0], <double> birth_radius, <double> tform) 
					) 
					return zone 
				else: 
					bin_ = int(_hydrodiskstars.calczone_linear(self._hds[0], 
						tform, birth_radius, _END_TIME_, self._analog_idx, 
						<double> time))
					if bin_ != -1: 
						return bin_ 
					else: 
						raise ValueError("Radius out of bin range.") 
			else: 
				raise ValueError("Zone out of range: %d" % (zone)) 
		else: 
			raise TypeError("Zone must be of type int. Got: %s" % (type(zone))) 


cdef class c_sudden(c_hydrodiskstars): 

	r""" 
	C-implementation of sudden migration scheme. See python version for 
	docstrings. 
	""" 

	def __init__(self, radbins, tformcolumn = 1, rformcolumn = 2, 
		rfinalcolumn = 4): 
		super().__init__(radbins, tformcolumn = tformcolumn, 
			rformcolumn = rformcolumn, rfinalcolumn = rfinalcolumn) 
		self._migration_time = 0 

	def __call__(self, zone, tform, time): 
		if isinstance(zone, int): 
			if 0 <= zone < self._hds[0].n_rad_bins: 
				birth_radius = (self._hds[0].rad_bins[zone] + 
					self._hds[0].rad_bins[zone + 1]) / 2 
				if tform == time: 
					self._analog_idx = (
						_hydrodiskstars.hydrodiskstars_find_analog(
							self._hds[0], birth_radius, tform) 
					) 
					self._migration_time = _hydrodiskstars.rand_range(tform, 
						_END_TIME_) 
					return zone 
				else: 
					bin_ = int(_hydrodiskstars.calczone_sudden(self._hds[0], 
						self._migration_time, birth_radius, self._analog_idx, 
						<double> time)) 
					if bin_ != -1: 
						return bin_ 
					else: 
						raise ValueError("Radius out of bin range.") 
			else: 
				raise ValueError("Zone out of range: %d" % (zone)) 
		else: 
			raise TypeError("Zone must be of type int. Got: %s" % (type(zone))) 


cdef class c_diffusion(c_hydrodiskstars): 

	r""" 
	C-implementation of diffusion migration scheme. See python version for 
	docstrings. 
	""" 

	def __call__(self, zone, tform, time): 
		if isinstance(zone, int): 
			if 0 <= zone < self._hds[0].n_rad_bins: 
				birth_radius = (self._hds[0].rad_bins[zone] + 
					self._hds[0].rad_bins[zone + 1]) / 2 
				if tform == time: 
					self._analog_idx = (
						_hydrodiskstars.hydrodiskstars_find_analog(
							self._hds[0], birth_radius, tform) 
					)  
					return zone 
				else: 
					bin_ = int(_hydrodiskstars.calczone_diffusive(self._hds[0], 
						tform, birth_radius, _END_TIME_, self._analog_idx, 
						<double> time)) 
					if bin_ != -1: 
						return bin_ 
					else: 
						raise ValueError("Radius out of bin range.") 
			else: 
				raise ValueError("Zone out of range: %d" % (zone)) 
		else: 
			raise TypeError("Zone must be of type int. Got: %s" % (type(zone)))

