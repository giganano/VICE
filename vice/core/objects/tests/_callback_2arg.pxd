# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/objects/tests/callback_2arg.h":
	unsigned short test_callback_2arg_initialize()
	unsigned short test_callback_2arg_free()

