# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
import numbers
from ...core import _pyutils
from libc.stdlib cimport malloc
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

			# using copy_pylist from vice/core/_cutils.pyx causes a NameError
			# upon import stating that the "numbers" module isn't imported
			# when creating the built-in instances of explodability engines in
			# the vice.yields.ccsne.engines module. Who knows why.... but don't
			# use that here because it breaks things. Implementing the memory
			# allocation and copying over is simple enough and works just fine.
			self._is1d[0].xcoords = <double *> malloc (self._is1d[0].n_points *
				sizeof(double))
			self._is1d[0].ycoords = <double *> malloc (self._is1d[0].n_points *
				sizeof(double))
			for i in range(self._is1d[0].n_points):
				if isinstance(xcoords[i], numbers.Number):
					self._is1d[0].xcoords[i] = <double> xcoords[i]
				else:
					raise TypeError("Non-numerical value detected.")
				if isinstance(ycoords[i], numbers.Number):
					self._is1d[0].ycoords[i] = <double> ycoords[i]
				else:
					raise TypeError("Non-numerical value detected.")
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

