# cython: language_level = 3, boundscheck = False

cdef extern from "callback.h":
	unsigned short test_callback_1arg_evaluate()
	unsigned short test_callback_2arg_evaluate()

