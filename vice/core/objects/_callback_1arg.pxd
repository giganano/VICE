# cython: language_level = 3, boundscheck = False


cdef extern from "../../src/objects.h":
	ctypedef struct CALLBACK_1ARG:
		double (*callback)(double, void *)
		double assumed_constant
		void *user_func


cdef extern from "../../src/objects/callback_1arg.h":
	CALLBACK_1ARG *callback_1arg_initialize()
	void callback_1arg_free(CALLBACK_1ARG *cb1)

