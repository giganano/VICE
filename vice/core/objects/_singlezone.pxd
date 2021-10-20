# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from libc.stdio cimport FILE
from ._element cimport ELEMENT
from ._ism cimport ISM
from ._mdf cimport MDF
from ._ssp cimport SSP

cdef extern from "../../src/objects.h":
	ctypedef struct SINGLEZONE:
		char *name
		FILE *history_writer
		FILE *mdf_writer
		double dt
		double current_time
		double *output_times
		unsigned long timestep
		unsigned long n_outputs
		double Z_solar
		unsigned int n_elements
		unsigned short verbose
		ELEMENT **elements
		ISM *ism
		MDF *mdf
		SSP *ssp


cdef extern from "../../src/singlezone.h":
	double SINGLEZONE_MAX_EVAL_TIME
	long BUFFER
	SINGLEZONE *singlezone_initialize()
	void singlezone_free(SINGLEZONE *sz)
	long singlezone_address(SINGLEZONE *sz)
	unsigned short singlezone_evolve(SINGLEZONE *sz)
	void singlezone_cancel(SINGLEZONE *sz)
	unsigned long n_timesteps(SINGLEZONE sz)

