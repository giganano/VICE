# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from .....core.multizone._multizone cimport c_multizone
from .....core.objects._multizone cimport MULTIZONE


### For use in constructing the no-migration edge-case test ###
cdef class generic(c_multizone):
	pass

cdef extern from "../../multizone.h":
	void multizone_evolve_full(MULTIZONE *mz)
	unsigned short multizone_setup(MULTIZONE *mz)
	void multizone_clean(MULTIZONE *mz)

cdef extern from "../../mdf.h":
	unsigned short tracers_MDF(MULTIZONE *mz)

cdef extern from "../../../io/multizone.h":
	void write_multizone_mdf(MULTIZONE mz)
	unsigned short multizone_open_tracer_file(MULTIZONE *mz)
	void write_tracers_header(MULTIZONE mz)
	void write_tracers_output(MULTIZONE mz)
	void multizone_close_tracer_file(MULTIZONE *mz)


### generic case unit tests ###
cdef extern from "../tracer.h":
	unsigned short generic_test_inject_tracers(MULTIZONE *mz)

