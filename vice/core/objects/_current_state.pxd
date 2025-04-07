# cython: language_level = 3, boundscheck = False


cdef extern from "../../src/objects.h":
	ctypedef struct CURRENT_STATE:
		double mgas
		double star_formation_rate
		double infall_rate
		double outflow_rate
		unsigned short n_elements
		char **symbols
		double *Z


cdef extern from "../../src/objects/current_state.h":
	CURRENT_STATE *current_state_initialize(unsigned short n_elements)
	void current_state_free(CURRENT_STATE *cs)


