# cython: language_level = 3, boundscheck = False

cdef extern from "../../src/yields/tests/integral.h":
	unsigned short test_quad_euler()
	unsigned short test_quad_trapzd()
	unsigned short test_quad_midpt()
	unsigned short test_quad_simp()

