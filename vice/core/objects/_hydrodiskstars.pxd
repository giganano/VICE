# cython: language_level = 3, boundscheck = False

cdef extern from "../../src/objects.h": 
	ctypedef struct HYDRODISKSTARS: 
		unsigned long n_stars 
		double *birth_times 
		double *birth_radii 
		double *final_radii 
		double *rad_bins 
		unsigned short n_rad_bins 


cdef extern from "../../src/objects/hydrodiskstars.h": 
	HYDRODISKSTARS *hydrodiskstars_initialize() 
	void hydrodiskstars_free(HYDRODISKSTARS *hds) 

