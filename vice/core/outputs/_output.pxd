# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..dataframe._history cimport history
from ..dataframe._fromfile cimport fromfile
from ..dataframe._saved_yields cimport saved_yields

cdef class c_output:
	cdef history _hist
	cdef fromfile _mdf
	cdef object _elements
	cdef saved_yields _ccsne_yields
	cdef saved_yields _sneia_yields
	cdef saved_yields _agb_yields
	cdef object _name


