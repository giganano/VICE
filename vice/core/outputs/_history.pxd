# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..dataframe._history cimport history as history_obj

cdef history_obj c_history(name)

