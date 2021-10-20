# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
import numbers
from ...core import _pyutils
from libc.stdlib cimport malloc
from . cimport _interp_scheme_2d


cdef class c_interp_scheme_2d:

	r"""
	See docstring in interp_scheme_2d.py.
	"""

	# no __cinit__ in case this is subclasses in pure python with a different
	# __init__ signature (in which case an error will be raised).

	def __init__(self, xcoords, ycoords, zcoords):

		# all parameters need to be array-like, zcoords being the only 2-D one,
		# and containing numerical values. This simply makes sure they're of
		# the proper lengths, allocates memory for them, and copies the values
		# over.
		xcoords = sorted(_pyutils.copy_array_like_object(xcoords))
		ycoords = sorted(_pyutils.copy_array_like_object(ycoords))
		zcoords = _pyutils.copy_array_like_object(zcoords)
		if len(xcoords) == len(zcoords):
			self._is2d = _interp_scheme_2d.interp_scheme_2d_initialize()
			self._is2d[0].n_x_values = <unsigned long> len(xcoords)
			self._is2d[0].n_y_values = <unsigned long> len(ycoords)
			self._is2d[0].xcoords = <double *> malloc (
				self._is2d[0].n_x_values * sizeof(double))
			self._is2d[0].zcoords = <double **> malloc (
				self._is2d[0].n_x_values * sizeof(double *))
			for i in range(self._is2d[0].n_x_values):
				if isinstance(xcoords[i], numbers.Number):
					self._is2d[0].xcoords[i] = <double> xcoords[i]
				else:
					raise TypeError("Non-numerical value detected.")
				if len(zcoords[i]) == len(ycoords):
					zcoords[i] = _pyutils.copy_array_like_object(zcoords[i])
					self._is2d[0].zcoords[i] = <double *> malloc (
						self._is2d[0].n_y_values * sizeof(double))
					for j in range(self._is2d[0].n_y_values):
						if isinstance(zcoords[i][j], numbers.Number):
							self._is2d[0].zcoords[i][j] = <double> zcoords[i][j]
						else:
							raise TypeError("Non-numerical value detected.")
				else:
					raise ValueError("""Array length mismatch. All elements of \
attribute 'zcoords' must be of the same length as attribute 'ycoords'. \
Got: (%d, %d).""" % (len(ycoords), len(zcoords[i])))
			self._is2d[0].ycoords = <double *> malloc (
				self._is2d[0].n_y_values * sizeof(double))
			for i in range(self._is2d[0].n_y_values):
				if isinstance(ycoords[i], numbers.Number):
					self._is2d[0].ycoords[i] = <double> ycoords[i]
				else:
					raise TypeError("Non-numerical value detected.")
		else:
			raise ValueError("""Array length mismatch. Attribute 'zcoords' \
must be of the same length as 'xcoords'. Got: (%d, %d).""" % (
				len(xcoords), len(zcoords)))


	def __dealloc__(self):
		_interp_scheme_2d.interp_scheme_2d_free(self._is2d)


	def __call__(self, x, y):
		if isinstance(x, numbers.Number) and isinstance(y, numbers.Number):
			return _interp_scheme_2d.interp_scheme_2d_evaluate(self._is2d[0],
				<double> x, <double> y)
		else:
			raise TypeError("Must be numerical values. Got: (%s, %s)." % (
				type(x), type(y)))


	@property
	def xcoords(self):
		r"""
		Type : ``list`` [elements are real numbers]

		The x-coordinates on which the function is sampled.
		"""
		return [self._is2d[0].xcoords[_] for _ in range(
			self._is2d[0].n_x_values)]


	@property
	def ycoords(self):
		r"""
		Type : ``list`` [elements are real numbers]

		The y-coordinates on which the function is sampled.
		"""
		return [self._is2d[0].ycoords[_] for _ in range(
			self._is2d[0].n_y_values)]


	@property
	def zcoords(self):
		r"""
		Type : ``list`` [elements are of type ``list``, storing real numbers]

		The z-coordinates on which the function is sampled. A 2-D list, this
		attribute stores a value at each of the (x, y) coordinates on which
		a z-coordinate is known. The first axis corresponds to the x-coordinate,
		and the second the y-coordinate.
		"""
		zcoords = self._is2d[0].n_x_values * [None]
		for i in range(self._is2d[0].n_x_values):
			zcoords[i] = [self._is2d[0].zcoords[i][_] for _ in range(
				self._is2d[0].n_y_values)]
		return zcoords


	@property
	def n_x_values(self):
		r"""
		Type : ``int``

		The number of x-coordinates on which the function is sampled. For each
		x-coordinate, there are ``n_y_values`` y-coordinates at which the
		z-coordinate is known.
		"""
		return self._is2d[0].n_x_values


	@property
	def n_y_values(self):
		r"""
		Type : ``int``

		The number of y-coordinates on which the function is sampled. For each
		y-coordinate, there are ``n_x_values`` x-coordinates at which the
		z-coordinate is known.
		"""
		return self._is2d[0].n_y_values

