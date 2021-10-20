# cython: language_level = 3, boundscheck = False

cdef extern from "stats.h":
	unsigned short test_convert_to_PDF()
