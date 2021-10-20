# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/ssp/tests/msmf.h":
	unsigned short test_MSMF()
	unsigned short test_setup_MSMF()
