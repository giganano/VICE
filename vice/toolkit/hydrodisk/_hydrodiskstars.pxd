# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ...core.objects._hydrodiskstars cimport HYDRODISKSTARS

cdef extern from "../../src/objects/hydrodiskstars.h":
	HYDRODISKSTARS *hydrodiskstars_initialize()
	void hydrodiskstars_free(HYDRODISKSTARS *hds)


cdef extern from "../../src/toolkit/hydrodiskstars.h":
	unsigned short hydrodiskstars_import(HYDRODISKSTARS *hds,
		unsigned long Nstars, char *filestem, unsigned short ids_column,
		unsigned short birth_times_column, unsigned short birth_radii_column,
		unsigned short final_radii_column, unsigned short zformcolumn,
		unsigned short zfinal_column, unsigned short v_radcolumn,
		unsigned short v_phicolumn, unsigned short v_zcolumn,
		unsigned short decomp_column)
	unsigned short hydrodiskstars_decomp_filter(HYDRODISKSTARS *hds,
		unsigned short *decomp_values, unsigned short n_decomp_values)
	long hydrodiskstars_find_analog(HYDRODISKSTARS hds, double birth_radius,
		double birth_time)
	double calczone_linear(HYDRODISKSTARS hds, double birth_time,
		double birth_radius, double end_time, long analog_idx, double time)
	double calczone_sudden(HYDRODISKSTARS hds, double migration_time,
		double birth_radius, long analog_idx, double time)
	double calczone_diffusive(HYDRODISKSTARS hds, double birth_time,
		double birth_radius, double end_time, long analog_idx, double time)
	double HYDRODISK_END_TIME


cdef extern from "../../src/utils.h":
	void seed_random()
	double rand_range(double minimum, double maximum)


cdef class c_hydrodiskstars:
	cdef HYDRODISKSTARS *_hds
	cdef long _analog_idx
	cdef double _migration_time
	cdef object _analog_data
