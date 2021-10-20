# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..dataframe._fromfile cimport fromfile as fromfile_obj

cdef fromfile_obj c_mdf(name)

