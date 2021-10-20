# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/ssp/tests/crf.h":
	unsigned short test_CRF()
	unsigned short test_setup_CRF()

