# cython: language_level = 3, boundscheck = False

cdef class zone_array:
	cdef object _zones
	cdef int _n

