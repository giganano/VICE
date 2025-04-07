# cython: language_level = 3, boundscheck = False

from ._current_state cimport CURRENT_STATE

cdef extern from "../../src/objects.h":
	ctypedef struct CALLBACK_CURRENT_STATE:
		double (*callback)(CURRENT_STATE *, void *) except *
		void *user_func
