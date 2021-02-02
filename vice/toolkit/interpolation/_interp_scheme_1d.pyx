# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import 
import numbers 
from ...core import _pyutils 
from ...core._cutils cimport copy_pylist 
from . cimport _interp_scheme_1d 


cdef class c_interp_scheme_1d: 

	r""" 
	See docstring in interp_scheme_1d.py. 
	""" 

	# no __cinit__ in case this is subclassed in pure python with a different 
	# __init__ signature (in which case an error will be raised). 

	def __init__(self, xcoords, ycoords): 
		xcoords = _pyutils.copy_array_like_object(xcoords) 
		xcoords = sorted(xcoords) 
		ycoords = _pyutils.copy_array_like_object(ycoords) 
		if len(xcoords) == len(ycoords): 
			self._is1d = _interp_scheme_1d.interp_scheme_1d_initialize() 
			self._is1d[0].n_points = len(xcoords) 
			self._is1d[0].xcoords = copy_pylist(xcoords) 
			self._is1d[0].ycoords = copy_pylist(ycoords) 
		else: 
			raise ValueError("Array length mismatch. Got: (%d, %d)" % (
				len(xcoords), len(ycoords))) 

	def __dealloc__(self): 
		_interp_scheme_1d.interp_scheme_1d_free(self._is1d) 

	def __call__(self, x): 
		if isinstance(x, numbers.Number): 
			return _interp_scheme_1d.interp_scheme_1d_evaluate(self._is1d[0], 
				<double> x) 
		else: 
			raise TypeError("""X-coordinate to evaluate interpolation scheme \
at must be a numerical value. Got: %s""" % (type(x))) 

	def __getitem__(self, idx): 
		x = self.xcoords[idx] 
		y = self.ycoords[idx] 
		if isinstance(x, numbers.Number) and isinstance(y, numbers.Number): 
			return [x, y] 
		elif isinstance(x, list) and isinstance(y, list): 
			return [list(_) for _ in zip(x, y)] 
		else: 
			raise SystemError("Internal Error.") 

	@property 
	def xcoords(self): 
		r""" 
		Type : ``list`` [elements are real numbers] 

		The x-coordinates on which the function is sampled. 
		""" 
		return [self._is1d[0].xcoords[_] for _ in range(self._is1d[0].n_points)] 

	@property 
	def ycoords(self): 
		r""" 
		Type : ``list`` [elements are real numbers] 

		The y-coordinates on which the function is sampled. 
		""" 
		return [self._is1d[0].ycoords[_] for _ in range(self._is1d[0].n_points)] 

	@property 
	def n_points(self): 
		r""" 
		Type : ``int`` 

		The number of (x, y) points on which the function is sampled. 
		""" 
		return int(self._is1d[0].n_points) 

