# cython: language_level = 3, boundscheck = False

from ._current_state cimport CURRENT_STATE

cdef extern from "../../src/objects.h":
	ctypedef struct CALLBACK_CURRENT_STATE:
		double (*callback)(CURRENT_STATE, void *) except *
		void *user_func

cdef extern from "../../src/objects/callback_current_state.h":
	CALLBACK_CURRENT_STATE *callback_current_state_initialize()
	void callback_current_state_free(CALLBACK_CURRENT_STATE	*cbcs)
