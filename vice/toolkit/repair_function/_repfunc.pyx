# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import 
import numbers 
from ...core._cutils cimport copy_pylist 
from . cimport _repfunc 


cdef class c_repfunc: 

	r""" 
	The C implementation of the repaired_function class. 
	""" 

	def __cinit__(self, xcoords, ycoords): 
		if isinstance(xcoords, list) and isinstance(ycoords, list): 
			if len(xcoords) == len(ycoords): 
				self._rpf = _repfunc.repfunc_initialize() 
				self._rpf[0].n_points = len(xcoords) 
				self._rpf[0].xcoords = copy_pylist(xcoords) 
				self._rpf[0].ycoords = copy_pylist(ycoords) 
			else: 
				raise ValueError("Array length mismatch. Got: (%d, %d)" % (
					len(xcoords), len(ycoords))) 
		else: 
			raise TypeError("""Both xcoords and ycoords must be of type list. \
Got: (%s, %s)""" % (type(xcoords), type(ycoords))) 

	def __init__(self, xcoords, ycoords): 
		pass 

	def __dealloc__(self): 
		_repfunc.repfunc_free(self._rpf) 

	def __call__(self, x): 
		if isinstance(x, numbers.Number): 
			return _repfunc.repfunc_evaluate(self._rpf[0], <double> x) 
		else: 
			raise TypeError("""X-coordinate to evaluate repaired function at \
must be a numerical value. Got: %s""" % (type(x))) 

	def __getitem__(self, idx): 
		x = self.xcoords[idx] 
		y = self.ycoords[idx] 
		if isinstance(x, numbers.Number) and isinstance(y, numbers.Number): 
			return [x, y] 
		elif isinstance(x, list) and isinstance(y, list): 
			return [list(i) for i in zip(x, y)] 
		else: 
			raise SystemError("Internal Error") 

	@property 
	def xcoords(self): 
		r""" 
		Docstring in python version -> list of the x coordinates. 
		""" 
		return [self._rpf[0].xcoords[i] for i in range(self._rpf[0].n_points)] 

	@property 
	def ycoords(self): 
		r""" 
		Docstring in python version -> list of the y coordinates. 
		""" 
		return [self._rpf[0].ycoords[i] for i in range(self._rpf[0].n_points)] 

	@property 
	def n_points(self): 
		r""" 
		Docstring in python version -> the number of points that the function 
		is sampled on. 
		""" 
		return int(self._rpf[0].n_points) 

