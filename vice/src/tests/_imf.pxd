# cython: language_level = 3, boundscheck = False

cdef extern from "imf.h":
	unsigned short test_imf_evaluate()
	unsigned short test_salpeter55()
	unsigned short test_kroupa01()
