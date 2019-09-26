# cython: language_level = 3, boundscheck = False
""" 
This file implements the polynomial object and wraps its core routines written 
at vice/src/polynomial.c 
""" 

from ._objects cimport POLYNOMIAL
from . cimport _numparam  
from . cimport _polynomial 

cdef class polynomial: 

	cdef POLYNOMIAL *_poly 

	def __cinit__(self, coeffs): 
		self._poly = _polynomial.polynomial_initialize(len(coeffs)) 

	def __dealloc__(self): 
		_polynomial.polynomial_free(self._poly) 


