# cython: language_level = 3, boundscheck = False


cdef extern from "../../src/objects.h":
	ctypedef struct FROMFILE:
		char *name
		char **labels
		unsigned long n_rows
		unsigned long n_cols
		double **data


cdef extern from "../../src/dataframe/fromfile.h":
	FROMFILE *fromfile_initialize()
	void fromfile_free(FROMFILE *ff)

