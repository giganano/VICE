# cython: language_level = 3, boundscheck = False

cdef extern from "../../src/objects.h":
	ctypedef struct MDF:
		double **abundance_distributions
		double **ratio_distributions
		double *bins
		unsigned long n_bins

cdef extern from "../../src/objects/mdf.h":
	MDF *mdf_initialize()
	void mdf_free(MDF *mdf)

