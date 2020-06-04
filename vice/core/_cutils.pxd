# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from .objects._imf cimport IMF_ 
from .objects._callback_1arg cimport CALLBACK_1ARG 
from .objects._callback_2arg cimport CALLBACK_2ARG 

cdef extern from "../src/utils.h": 
	double *binspace(double start, double stop, long N) 
	void set_char_p_value(char *dest, int *ords, int length) 

cdef extern from "../src/imf.h": 
	double IMF_STEPSIZE 
	unsigned short imf_set_mass_distribution(IMF_ *imf, double *arr) 

cdef extern from "../src/objects.h": 
	CALLBACK_1ARG *callback_1arg_initialize() 
	void callback_1arg_free(CALLBACK_1ARG *cb1) 
	CALLBACK_2ARG *callback_2arg_initialize() 
	void callback_2arg_free(CALLBACK_2ARG *cb2) 


cdef void callback_1arg_setup(CALLBACK_1ARG *cb1, value) except * 
cdef void callback_2arg_setup(CALLBACK_2ARG *cb2, value) except * 
cdef double callback_1arg(double x, void *f) 
cdef double callback_2arg(double x, double y, void *f) 
cdef void setup_imf(IMF_ *imf, IMF) except * 
cdef void set_string(char *dest, pystr) except * 
cdef int *ordinals(pystr) except * 
cdef double *copy_pylist(pylist) except * 
cdef double **copy_2Dpylist(pylist) except * 
cdef double *map_pyfunc_over_array(pyfunc, pyarray) except * 

