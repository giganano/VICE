# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ._callback_2arg cimport CALLBACK_2ARG

cdef extern from "../../src/objects.h":
	ctypedef struct ISM:
		char *mode
		double *specified
		double mass
		double star_formation_rate
		double infall_rate
		double *star_formation_history
		double *eta
		double *enh
		double *tau_star
		CALLBACK_2ARG *functional_tau_star
		double schmidt_index
		double mgschmidt
		double smoothing_time
		int schmidt

cdef extern from "../../src/objects/ism.h":
	ISM *ism_initialize()
	void ism_free(ISM *ism)

