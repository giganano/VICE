# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..objects._fromfile cimport FROMFILE
from ..objects._fromfile cimport fromfile_initialize
from ..objects._fromfile cimport fromfile_free
from ._base cimport base

cdef extern from "../../src/dataframe/fromfile.h":
	unsigned short fromfile_read(FROMFILE *ff)
	double *fromfile_column(FROMFILE *ff, char *label)
	unsigned short fromfile_modify_column(FROMFILE *ff, char *label,
		double *arr)
	unsigned short fromfile_new_column(FROMFILE *ff, char *label, double *arr)
	double *fromfile_row(FROMFILE *ff, unsigned long row)

cdef class fromfile(base):
	cdef FROMFILE *_ff

