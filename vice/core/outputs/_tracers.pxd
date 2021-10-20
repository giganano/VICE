# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..dataframe._tracers cimport tracers as tracers_obj

cdef tracers_obj c_tracers(name)
