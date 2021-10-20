# cython: language_level = 3, boundscheck = False

cdef extern from "../../src/objects.h":
	ctypedef struct HYDRODISKSTARS:
		unsigned long n_stars
		unsigned long *ids
		double *birth_times
		double *birth_radii
		double *final_radii
		double *zform
		double *zfinal
		double *v_rad
		double *v_phi
		double *v_z
		double *rad_bins
		unsigned short *decomp
		unsigned short n_rad_bins
		char *mode


cdef extern from "../../src/objects/hydrodiskstars.h":
	HYDRODISKSTARS *hydrodiskstars_initialize()
	void hydrodiskstars_free(HYDRODISKSTARS *hds)

