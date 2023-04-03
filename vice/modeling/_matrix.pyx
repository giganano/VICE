# cython: language_level = 3, boundscheck = False

__all__ = ["matrix"]
from ..core._pyutils import copy_array_like_object
import numbers

from libc.stdlib cimport malloc, free
from libc.string cimport strcat, strlen
from libc.stdio cimport sprintf
from ..core.objects cimport _matrix
from . cimport _matrix

cdef class matrix:

	r"""
	A generic matrix object for linear algebra operations.

	**Signature**: vice.modeling.matrix(arr)

	.. versionadded:: 1.X.0

	.. seealso:: vice.modeling.vector

	Parameters
	----------
	arr : ``array-like``
		The matrix itself, type-casting a 2-dimensional array into a matrix.
		Must be rectangular (i.e., each "row," or element on the first axis,
		must be the same length as all of the others). Each element must be a
		numerical value. If the matrix is to have only one row, a 1-dimensional
		array can also be passed for this parameter.

	.. note::

		Once a matrix object has been created, its size cannot be changed.
		If a change in size is necessary, please create a new matrix
		object.

	Attributes
	----------
	n_rows : ``int``
		The number of rows in the matrix (i.e., the number of elements along
		the first axis).
	n_cols : ``int``
		The number of columns in the matrix (i.e., the number of elements along
		the second axis).

	Indexing and Item Assignment
	----------------------------
	Both proceed with two integers separated by a comma (e.g.,
	``mat[0, 0]``, ``mat[1, 0] = 0.8``), and the assigned value must be a
	real number. Negative indices are not supported.

	Functions
	---------
	zeroes : [classmethod]
		Returns a matrix of a given size where every entry is set to zero.
	identity : [classmethod]
		Returns the identity matrix for a given size.
	determinant : [instancemethod]
		Compute the determinant of the matrix.
	inverse : [instancemethod]
		Compute the inverse of the matrix.
	transpose : [instancemethod]
		Compute the transpose of the matrix.

	Example Code
	------------
	>>> from vice.modeling import matrix
	>>> import numpy as np

	Simple matrices, such as those full of zeroes or the square identity
	matrix which can act as starting points in constructing more complex
	matrices, can be obtained using the ``matrix.zeroes`` and
	``matrix.identity`` classmethods:

	>>> example = matrix.zeroes(2, 3) # 2 rows by 3 columns
	>>> example
	matrix([0.00e+00    0.00e+00    0.00e+00]
	       [0.00e+00    0.00e+00    0.00e+00])
	>>> example = matrix.identity(5) # 5x5 square identity matrix
	>>> example
	matrix([1.00e+00    0.00e+00    0.00e+00    0.00e+00    0.00e+00]
	       [0.00e+00    1.00e+00    0.00e+00    0.00e+00    0.00e+00]
	       [0.00e+00    0.00e+00    1.00e+00    0.00e+00    0.00e+00]
	       [0.00e+00    0.00e+00    0.00e+00    1.00e+00    0.00e+00]
	       [0.00e+00    0.00e+00    0.00e+00    0.00e+00    1.00e+00])

	Indexing and item assignment proceed with two integers ``i`` and ``j``,
	separated by a comma, to obtain or modify the matrix element :math:`x_{ij}`:

	>>> example = matrix.identity(5)
	>>> example[0, 0]
	1.0
	>>> example[0, 1]
	0.0
	>>> example[2, 0] = np.pi
	>>> example[2, 0]
	3.141592653589793
	>>> example
	matrix([1.00e+00    0.00e+00    0.00e+00    0.00e+00    0.00e+00]
	       [0.00e+00    1.00e+00    0.00e+00    0.00e+00    0.00e+00]
	       [3.14e+00    0.00e+00    1.00e+00    0.00e+00    0.00e+00]
	       [0.00e+00    0.00e+00    0.00e+00    1.00e+00    0.00e+00]
	       [0.00e+00    0.00e+00    0.00e+00    0.00e+00    1.00e+00])

	Equivalence comparison returns ``True`` if and only if the matrices have
	the same dimensions and each component passes an equivalence comparison
	(i.e., :math:`A_{ij} = B_{ij}` for all :math:`i` and :math:`j`):

	>>> example = matrix.identity(5)
	>>> for i in range(5):
	>>>     for j in range(5):
	>>>         example[i, j] = 10 * np.random.rand()
	>>> example
	matrix([1.12e+00    8.59e-01    8.95e+00    5.00e+00    6.12e+00]
	       [5.17e+00    1.78e+00    1.38e+00    3.82e+00    1.19e+00]
	       [2.39e+00    6.94e+00    3.38e+00    8.58e-01    5.62e+00]
	       [5.14e+00    1.41e+00    1.52e+00    9.56e+00    1.53e+00]
	       [8.69e+00    1.22e+00    8.29e+00    7.94e+00    8.56e+00])
	>>> copy = matrix.identity(5)
	>>> for i in range(5):
	>>>     for j in range(5):
	>>>         copy[i, j] = example[i, j]
	>>> copy == example
	True
	>>> example == matrix.identity(5)
	False
	>>> example = matrix.zeroes(2, 4)
	False
	>>> example = matrix.identity(4)
	>>> example == example.inverse()
	True

	For matrices with the same dimensions, addition and subtraction proceed as
	usual with the ``+`` and ``-`` operators:

	>>> example1 = matrix.zeroes(3, 4)
	>>> example2 = matrix.zeroes(3, 4)
	>>> for i in range(example1.n_rows):
	>>>     for j in range(example1.n_cols):
	>>>         example1[i, j] = 10 * np.random.rand()
	>>>         example2[i, j] = 10 * np.random.rand()
	>>> example1
	matrix([6.40e+00    6.39e+00    2.73e+00    6.39e+00]
	       [6.87e+00    1.98e-01    4.55e+00    1.85e+00]
	       [7.98e+00    4.17e+00    5.72e+00    6.98e+00])
	>>> example2
	matrix([5.46e+00    6.09e+00    6.40e+00    8.44e+00]
	       [9.25e+00    3.63e+00    9.81e-01    6.08e+00]
	       [9.18e+00    7.54e+00    9.35e+00    7.81e+00])
	>>> result = example1 + example2
	>>> result
	matrix([1.19e+01    1.25e+01    9.13e+00    1.48e+01]
	       [1.61e+01    3.83e+00    5.54e+00    7.93e+00]
	       [1.72e+01    1.17e+01    1.51e+01    1.48e+01])
	>>> for i in range(result.n_rows):
	>>>     for j in range(result.n_cols):
	>>>         assert result[i, j] == example1[i, j] + example2[i, j]
	>>> result = example1 - example2
	>>> result
	matrix([9.39e-01    3.07e-01    -3.66e+00    -2.05e+00]
	       [-2.38e+00   -3.43e+00   3.57e+00     -4.23e+00]
	       [-1.20e+00   -3.37e+00   -3.63e+00    -8.25e-01])
	>>> for i in range(result.n_rows):
	>>>     for j in range(result.n_cols):
	>>>         assert result[i, j] == example1[i, j] - example2[i, j]

	Multiplication proceeds as usual with the ``*`` operator for multiplication
	by both scalars and other matrices. For matrix multiplication, the number
	of rows in the second operand must equal the number of columns in the
	first operand for the operation to be possible.
	
	>>> 3 * matrix.identity(5)
	matrix([3.00e+00    0.00e+00    0.00e+00    0.00e+00    0.00e+00]
	       [0.00e+00    3.00e+00    0.00e+00    0.00e+00    0.00e+00]
	       [0.00e+00    0.00e+00    3.00e+00    0.00e+00    0.00e+00]
	       [0.00e+00    0.00e+00    0.00e+00    3.00e+00    0.00e+00]
	       [0.00e+00    0.00e+00    0.00e+00    0.00e+00    3.00e+00])
	>>> 2 * matrix.identity(5) == matrix.identity(5) + matrix.identity(5)
	True
	>>> example1 = matrix.zeroes(3, 4) # 3 rows by 4 columns
	>>> example2 = matrix.zeroes(4, 2) # 4 rows by 2 columns
	>>> for i in range(example1.n_rows):
	>>>     for j in range(example1.n_cols):
	>>>         example1[i, j] = 10 * np.random.rand()
	>>> for i in range(example2.n_rows):
	>>>     for j in range(example2.n_cols):
	>>>         example2[i, j] = 10 * np.random.rand()
	>>> example1
	matrix([3.19e-01    7.91e+00    8.74e+00    8.04e-02]
	       [9.41e-01    1.86e+00    4.02e+00    9.54e+00]
	       [4.28e+00    3.19e+00    3.70e+00    9.03e+00])
	>>> example1 * matrix.identity(4)
	matrix([3.19e-01    7.91e+00    8.74e+00    8.04e-02]
	       [9.41e-01    1.86e+00    4.02e+00    9.54e+00]
	       [4.28e+00    3.19e+00    3.70e+00    9.03e+00])
	>>> example2
	matrix([3.47e+00    5.48e-01]
	       [6.88e+00    8.34e-02]
	       [1.01e+00    8.74e+00]
	       [2.06e+00    8.84e+00])
	>>> np.pi * example2
	matrix([1.09e+01    1.72e+00]
	       [2.16e+01    2.62e-01]
	       [3.18e+00    2.75e+01]
	       [6.48e+00    2.78e+01])
	>>> result = example1 * example2 # result will be 3 rows by 2 columns
	>>> result
	matrix([6.45e+01    7.80e+01]
	       [3.98e+01    1.20e+02]
	       [5.92e+01    1.15e+02])

	Determinants of square matrices can be computed with ``x.determinant`` for
	a matrix ``x``:

	>>> example = matrix.zeroes(4, 4)
	>>> for i in range(example.n_rows):
	>>>     for j in range(example.n_cols):
	>>>         example[i, j] = 10 * np.random.rand()
	>>> example
	matrix([3.25e-01    8.87e+00    4.08e+00    5.92e+00]
	       [7.68e+00    8.14e+00    2.28e+00    9.67e+00]
	       [9.87e+00    4.52e+00    2.77e+00    4.38e+00]
	       [3.79e+00    9.90e+00    6.06e+00    6.33e+00])
	>>> example.determinant()
	-215.20245282995597
	>>> matrix.identity(5).determinant()
	1.0

	Square matrices can be inverted with ``x.inverse`` for a matrix ``x``:

	>>> example = matrix.zeroes(4, 4)
	>>> for i in range(4):
	>>>     for j in range(4):
	>>>         example[i, j] = 10 * np.random.rand()
	>>> example
	matrix([4.83e+00    4.26e+00    1.04e+00    9.79e+00]
	       [9.22e+00    5.79e+00    1.95e+00    5.59e+00]
	       [6.99e+00    7.55e-02    9.25e+00    3.35e+00]
	       [3.16e+00    9.48e+00    8.57e+00    8.32e+00])
	>>> example.inverse()
	matrix([-2.81e-02   1.18e-01    3.36e-02    -5.98e-02]
	       [-1.01e-01   9.32e-02    -9.60e-02   9.46e-02]
	       [-3.72e-02   -5.66e-02   7.74e-02    5.06e-02]
	       [1.64e-01    -9.28e-02   1.70e-02    -1.71e-02])
	>>> example * example.inverse()
	matrix([1.00e+00    0.00e+00    -8.33e-17   5.55e-17]
	       [1.11e-16    1.00e+00    -4.16e-17   1.11e-16]
	       [0.00e+00    -1.67e-16   1.00e+00    6.25e-17]
	       [2.22e-16    -1.11e-16   1.67e-16    1.00e+00])

	Note in the example above that the product of the 4x4 matrix and its
	inverse is not *exactly* the identity matrix, but the off-diagonal
	components are within floating-point precision of zero anyway.

	Matrices of any size can be transposed with ``x.transpose`` for a matrix
	``x``:

	>>> example = matrix.zeroes(3, 4)
	>>> for i in range(3):
	>>>     for j in range(4):
	>>>         example[i, j] = 10 * np.random.rand()
	>>> example
	matrix([9.44e-01    8.25e+00    9.92e+00    2.30e+00]
	       [3.69e+00    3.18e+00    9.04e+00    7.58e+00]
	       [5.44e+00    5.94e+00    7.98e-01    1.36e+00])
	>>> example.transpose()
	matrix([9.44e-01    3.69e+00    5.44e+00]
	       [8.25e+00    3.18e+00    5.94e+00]
	       [9.92e+00    9.04e+00    7.98e-01]
	       [2.30e+00    7.58e+00    1.36e+00])
	>>> matrix.identity(5) == matrix.identity(5).transpose()
	True
	"""

	def __cinit__(self, obj):
		r"""
		Allocate memory for a matrix. User access of this function is strongly
		discouraged.
		"""
		msg = """\
Matrix or vector must be a 1-dimensional or square 2-dimensional array-like \
object containing only numerical values."""
		try:
			obj = copy_array_like_object(obj)
		except TypeError:
			raise TypeError(msg)

		# determine if this is a 1-d or 2-d object. If it's 1-d, make it 2-d
		# by making it the 0'th element of a list and use the same
		# functionality as implemented for the 2-d objects.
		is2d = True
		for i in range(len(obj)): is2d &= hasattr(obj[i], "__getitem__")
		if not is2d:
			if all([isinstance(_, numbers.Number) for _ in obj]):
				obj = [obj]
			else:
				raise TypeError("""\
Matrix or vector must contain only numerical values.""")
		else: pass

		# if it's a 1-D array, simply make it 2-D and use same functionality
		# if all([isinstance(_, numbers.Number) for _ in obj]): obj = [obj]
		for i in range(len(obj)):
			try:
				obj[i] = copy_array_like_object(obj[i])
			except TypeError:
				raise TypeError(msg)
			if len(obj[i]) != len(obj[0]):
				raise TypeError(msg)
			else:
				for j in range(len(obj[i])):
					if not isinstance(obj[i][j], numbers.Number):
						raise TypeError(msg)
					else: pass
		self._m = _matrix.matrix_initialize(<unsigned short> len(obj),
			<unsigned short> len(obj[0]))


	def __init__(self, obj):
		r"""
		Initialize a matrix by type-casting a 2-dimensional array-like object.
		See help(vice.modeling.matrix) for more information.
		"""
		# simply make 1-D arrays 2-D
		if all([isinstance(_, numbers.Number) for _ in obj]): obj = [obj]
		for i in range(self.n_rows):
			for j in range(self.n_cols):
				self._m[0].matrix[i][j] = <double> obj[i][j]


	def __dealloc__(self):
		r"""
		Free up the memory stored by a matrix object. User access to this
		function is strongly discouraged.
		"""
		matrix_free(self._m)


	def __enter__(self):
		r"""
		Opens a with statement
		"""
		return self


	def __exit__(self, exc_type, exc_value, exc_tb):
		r"""
		Raises all exceptions inside with statements
		"""
		return exc_value is None


	def __repr__(self):
		r"""
		Returns a string representation of the matrix.
		"""
		rep = "matrix("
		for i in range(self.n_rows):
			if i:
				rep += "       ["
			else:
				rep += "["
			for j in range(self.n_cols):
				rep += "%.2e" % (self._m[0].matrix[i][j])
				if j != self.n_cols - 1: rep += "\t"
			rep += "]"
			if i != self.n_rows - 1: rep += "\n"
		rep += ")"
		return rep


	def __getitem__(self, key):
		r"""
		Index the matrix with self[key]. Key must be a pair of two integers
		separated by a comma.
		"""
		self.__indexing_error_handling__(key)
		return float(self._m[0].matrix[<unsigned short> key[0]][<unsigned short>
			key[1]])


	def __setitem__(self, key, value):
		r"""
		Set self[key] to a new value. Key must be a pair of two integers
		separated by a comma, and value must be a real number.
		"""
		self.__indexing_error_handling__(key)
		if isinstance(value, numbers.Number):
			self._m[0].matrix[<unsigned short> key[0]][<unsigned short>
				key[1]] = <double> value
		else:
			raise TypeError("""\
Item assignment requires a numerical value. Got: %s""" % (type(value)))


	def __indexing_error_handling__(self, key):
		r"""
		Does all error handling for indexing and item assignment.
		"""
		if not isinstance(key, tuple):
			raise IndexError("""\
Exactly 2 integer matrix indices must be provided. Got: %s""" % (str(key)))
		elif len(key) != 2:
			raise IndexError("""\
Exactly 2 integer matrix indices must be provided. Got: %d""" % (len(key)))
		elif key[0] % 1 or key[1] % 1:
			raise IndexError("""\
Indices must be non-negative integers. Got: (%g, %g)""" % (key[0], key[1]))
		elif key[0] < 0 or key[0] >= self.n_rows:
			raise IndexError("""\
Index out of bounds for matrix with %d rows: %d""" % (self.n_rows, key[0]))
		elif key[1] < 0 or key[1] >= self.n_cols:
			raise IndexError("""\
Index out of bounds for matrix with %d columns: %d""" % (self.n_cols, key[1]))
		else:
			return


	def __eq__(self, other):
		r"""
		Equivalence comparison between two matrix objects. Returns True if they
		are of the same size and each component-wise pair of elements passes
		the '==' equivalence test.
		"""
		if isinstance(other, matrix):
			if self.n_cols == other.n_cols and self.n_rows == other.n_rows:
				result = True
				for i in range(self.n_rows):
					for j in range(self.n_cols):
						result &= self[i, j] == other[i, j]
						if not result: break
					if not result: break
				return result
			else:
				return False
		else:
			return False


	def __add__(self, other):
		r"""
		Addition of two matrix objects. They must have the same number of rows
		and columns for the operation to be possible.
		"""
		if isinstance(other, matrix):
			return self.__add_matrices__(other)
		else:
			raise TypeError("""\
Matrix addition only possible with another matrix. Got: %s""" % (type(other)))


	def __add_matrices__(self, matrix other):
		r"""
		See matrix.__add__.
		"""
		if self.n_rows == other.n_rows and self.n_cols == other.n_cols:
			result = matrix(self.n_rows * [other.n_cols * [0.]])
			result._m = matrix_add(self._m[0], other._m[0], result._m)
			return result
		else:
			raise ArithmeticError("""\
Incompatible matrix dimensions for addition. Self: %d rows, %d columns. \
Other: %d rows, %d columns.""" % (
				self.n_rows, self.n_cols, other.n_rows, other.n_cols))


	def __sub__(self, other):
		r"""
		Subtraction of two matrices. They must have the same number of rows
		and columns for the operation to be possible.
		"""
		if isinstance(other, matrix):
			return self.__sub_matrices__(other)
		else:
			raise TypeError("""\
Matrix subtraction only possible with another matrix. Got: %s""" % (
				type(other)))


	def __sub_matrices__(self, matrix other):
		r"""
		See matrix.__sub__.
		"""
		if self.n_rows == other.n_rows and self.n_cols == other.n_cols:
			result = matrix(self.n_rows * [other.n_cols * [0.]])
			result._m = matrix_subtract(self._m[0], other._m[0], result._m)
			return result
		else:
			raise ArithmeticError("""\
Incompatible matrix dimensions for subtraction. Self %d rows, %d columns. \
Other: %d rows, %d columns.""" % (
				self.n_rows, self.n_cols, other.n_rows, other.n_cols))


	def __mul__(self, other):
		r"""
		Multiplication of a matrix with either another matrix or a scalar.
		If multiplying by a matrix, then the first must have the same number of
		columns as there are rows in the second matrix for the operation to
		be possible.
		"""
		if not isinstance(self, matrix): 
			# allows commutativity for scalar multiplication -> other must be a
			# matrix if this condition evaluated to True.
			return other.__mul__(self)
		elif isinstance(other, matrix):
			return self.__mul_matrices__(other)
		elif isinstance(other, numbers.Number):
			return self.__mul_scalar__(float(other))
		else:
			raise TypeError("""\
Matrix multiplication only possible with scalar or another matrix. \
Got: %s""" % (type(other)))


	def __mul_matrices__(self, matrix other):
		r"""
		See matrix.__mul__.
		"""
		if self.n_cols == other.n_rows:
			result = matrix(self.n_rows * [other.n_cols * [0.]])
			result._m = matrix_multiply(self._m[0], other._m[0], result._m)
			return result
		else:
			raise ArithmeticError("""\
Incompatible matrix dimensions for multiplication. Self: %d rows, %d columns. \
Other: %d rows, %d columns.""" % (
				self.n_rows, self.n_cols, other.n_rows, other.n_cols))


	def __mul_scalar__(self, float other):
		r"""
		See matrix.__mul__.
		"""
		result = matrix(self.n_rows * [self.n_cols * [0.]])
		for i in range(self.n_rows):
			for j in range(self.n_cols):
				result[i, j] = other * self._m[0].matrix[i][j]
		return result


	def __address(self):
		r"""
		Obtain the address of the matrix pointer in C as a string. Used in the
		process of linking covariances matrices to their respective data
		vectors. User access to this function is strongly discouraged.
		"""
		cdef char *address = <char *> malloc (100 * sizeof(char))
		sprintf(address, "%p", <void *> self._m)
		strcat(address, "\0")
		pycopy = "".join(chr(address[i]) for i in range(strlen(address)))
		free(address)
		return pycopy


	@property
	def n_rows(self):
		r"""
		Type : ``int`` [positive definite]

		The number of rows in the matrix (i.e., the number of elements along
		the first axis of indexing or item assignment).

		.. note::

			Once a matrix object has been created, its size cannot be changed.
			If a change in size is necessary, please create a new matrix
			object.

		Example Code
		------------
		>>> from vice.modeling import matrix
		>>> example = matrix.zeroes(2, 3) # 2 rows by 3 columns
		>>> example.n_rows
		2
		>>> example = matrix.identity(5)
		>>> example.n_rows
		5
		>>> example = matrix.zeroes(4, 7) # 4 rows by 7 columns
		>>> example.n_rows 4
		"""
		return self._m[0].n_rows


	@property
	def n_cols(self):
		r"""
		Type : ``int`` [positive definite]

		The number of columns in the matrix (i.e., the number of elements along
		the second axis of indexing or item assignment).

		.. note::

			Once a matrix object has been created, its size cannot be changed.
			If a change in size is necessary, please create a new matrix
			object.

		Example Code
		------------
		>>> from vice.modeling import matrix
		>>> example = matrix.zeroes(2, 3) # 2 rows by 3 columns
		>>> example.n_cols
		3
		>>> example = matrix.identity(5)
		>>> example.n_cols
		5
		>>> example = matrix.zeroes(4, 7) # 4 rows by 7 columns
		>>> example.n_cols
		7
		"""
		return self._m[0].n_cols


	@classmethod
	def zeroes(cls, n_rows, n_cols):
		r"""
		Obtain a matrix of the specified size with every entry set to zero.

		**Signature**: vice.modeling.matrix.zeroes(n_rows, n_cols)

		Parameters
		----------
		n_rows : ``int``
			The number of rows in the matrix (i.e., the number of elements
			along the first axis).
		n_cols : ``int``
			The number of columns in the matrix (i.e., the number of elements
			along the second axis).
		
		Returns
		-------
		mat : ``matrix``
			A matrix of the specified size, with each entry initialize to a
			value of zero.

		Raises
		------
		* TypeError
			- One or both of ``n_rows`` and ``n_cols`` are not numerical values.
		* ValueError
			- ``n_rows`` and ``n_cols`` are numerical, but one or both are
			  positive integers.

		Example Code
		------------
		>>> from vice.modeling import matrix
		>>> example = matrix.zeroes(3, 3)
		>>> example
		matrix([0.00e+00    0.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00    0.00e+00])
		>>> for i in range(example.n_rows):
		>>>     for j in range(example.n_cols):
		>>>         assert example[i, j] == 0
		>>> matrix.zeroes(5, 2)
		matrix([0.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00])
		>>> matrix.zeroes(3, 4)
		matrix([0.00e+00    0.00e+00    0.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00    0.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00    0.00e+00    0.00e+00])
		"""
		if (isinstance(n_rows, numbers.Number) and
			isinstance(n_cols, numbers.Number)):
			if (n_rows % 1 == 0 and n_rows > 0 and
				n_cols % 1 == 0 and n_cols > 0):
				return cls(int(n_rows) * [int(n_cols) * [0.]])
			else:
				raise ValueError("""\
Matrix dimensions must be positive integers. Got: (%s, %s)""" % (n_rows,
					n_cols))
		else:
			raise TypeError("""\
Matrix dimensions must be positive integers. Got: (%s, %s)""" % (type(n_rows),
				type(n_cols)))


	@classmethod
	def identity(cls, n):
		r"""
		Obtain the identity matrix.

		**Signature**: vice.modeling.matrix.identity(n)

		Parameters
		----------
		n : ``int``
			The number of rows and columns in the matrix.

		Returns
		-------
		ident : ``matrix``
			The identity matrix with ``n`` rows and ``n`` columns. According to
			definition, this matrix has 1's along the diagonal and 0's off the
			diagonal.

		Raises
		------
		* TypeError
			- ``n`` is not an integer.

		Example Code
		------------
		>>> from vice.modeling import matrix
		>>> example = matrix.identity(3)
		>>> example
		matrix([1.00e+00    0.00e+00    0.00e+00]
		       [0.00e+00    1.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00    1.00e+00])
		>>> for i in range(example.n_rows):
		>>>     for j in range(example.n_cols):
		>>>         assert example[i, j] == int(i == j)
		>>> matrix.identity(2)
		matrix([1.00e+00    0.00e+00]
		       [0.00e+00    1.00e+00])
		>>> matrix.identity(5)
		matrix([1.00e+00    0.00e+00    0.00e+00    0.00e+00    0.00e+00]
		       [0.00e+00    1.00e+00    0.00e+00    0.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00    1.00e+00    0.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00    0.00e+00    1.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00    0.00e+00    0.00e+00    1.00e+00])
		"""
		if isinstance(n, numbers.Number) and n % 1 == 0:
			n = int(n)
			result = cls(n * [n * [0]])
			for i in range(n):
				result[i, i] = 1
			return result
		else:
			raise TypeError("""\
Number of rows and columns must be an integer. Got: %s""" % (type(n)))


	def determinant(self):
		r"""
		Compute the determinant of the matrix.

		**Signature**: x.determinant()

		Parameters
		----------
		x : ``matrix``
			An instance of this class.

		Returns
		-------
		det : ``float``
			The determinant of the matrix, :math:`det(x)`, computed via a
			recursive implementation of expansion by minors combined with an
			iterative sum.

		Raises
		------
		* TypeError
			- 	``self.n_rows != self.n_cols``. The determinant is defined only
				for square matrices.

		Example Code
		------------
		>>> from vice.modeling import matrix
		>>> import numpy as np
		>>> example = matrix.zeroes(3, 3)
		>>> for i in range(3):
		>>>     for j in range(i + 1):
		>>>         example[i, j] = example[j, i] = 10 * np.random.rand()
		>>> example
		matrix([2.17e+00    4.92e+00    4.50e+00]
		       [4.92e+00    1.26e-01    9.05e+00]
		       [4.50e+00    9.05e+00    8.17e+00])
		>>> example.determinant()
		24.79425369051026
		>>> matrix.identity(10).determinant()
		1.0
		>>> example = matrix.zeroes(5, 5)
		>>> for i in range(example.n_rows):
		>>>     for j in range(i + 1):
		>>>         example[i, j] = example[j, i] = 10 * np.random.rand()
		>>> example
		matrix([1.41e+00    3.95e+00    7.47e+00    1.73e+00    6.18e+00]
		       [3.95e+00    1.71e-01    5.89e+00    2.55e+00    9.58e+00]
		       [7.47e+00    5.89e+00    1.99e+00    8.28e+00    2.35e+00]
		       [1.73e+00    2.55e+00    8.28e+00    6.20e-01    8.23e+00]
		       [6.18e+00    9.58e+00    2.35e+00    8.23e+00    5.04e+00])
		>>> example.determinant()
		-1242.4394974576412
		"""
		if self.n_rows == self.n_cols:
			return float(matrix_determinant(self._m[0]))
		else:
			raise TypeError("""\
Cannot compute the determinant of a non-square matrix. \
Dimensions: (%d, %d)""" % (self.n_rows, self.n_cols))


	def inverse(self):
		r"""
		Compute the inverse of the matrix.

		**Signature**: x.inverse()

		Parameters
		----------
		x : ``matrix``
			An instance of this class.

		Returns
		-------
		inv : ``matrix``
			The matrix y such that ``x * y == y * x == I``, where ``I`` is the
			identity matrix of the same size as ``x`` and ``y``.

		Raises
		------
		* TypeError
			- 	``self.n_rows != self.n_cols``. The inverse is defined only for
				square matrices. Non-square matrices may have a left-inverse
				``a`` such that ``a * x == I`` and a right-inverse ``b`` such
				that ``x * b == I``, but these calculations are not implemented
				here.
		* ArithmeticError
			-	``x.determinant() == 0``. A square matrix is invertible if and
				only if the determinant is nonzero.

		Example Code
		------------
		>>> from vice.modeling import matrix
		>>> matrix.identity(3) == matrix.identity(3).inverse()
		True
		>>> matrix.identity(5) == matrix.identity(5).inverse()
		True
		>>> example = matrix.zeroes(4, 4)
		>>> for i in range(example.n_rows):
		>>>     for j in range(i + 1):
		>>>         example[i, j] = example[j, i] = 10 * np.random.rand()
		>>> example
		matrix([9.06e+00    7.28e-01    2.05e+00    4.57e+00]
		       [7.28e-01    9.60e+00    7.92e+00    3.46e+00]
		       [2.05e+00    7.92e+00    1.33e+00    7.67e+00]
		       [4.57e+00    3.46e+00    7.67e+00    5.05e+00])
		>>> inv = example.inverse()
		>>> inv
		matrix([1.80e-01    8.36e-02    -6.40e-02   -1.23e-01]
		       [8.36e-02    1.65e-01    2.92e-03    -1.93e-01]
		       [-6.40e-02   2.92e-03    -6.57e-02   1.56e-01]
		       [-1.23e-01   -1.93e-01   1.56e-01    2.05e-01])
		>>> example * inv
		matrix([1.00e+00    -1.11e-16   -2.22e-16   0.00e+00]
		       [-5.55e-17   1.00e+00    1.11e-16    -2.22e-16]
		       [2.22e-16    -2.22e-16   1.00e+00    0.00e+00]
		       [2.22e-16    0.00e+00    -1.11e-16   1.00e+00])

		Note in the final example above that the product of the example 4x4
		matrix and its inverse is not *exactly* the identity matrix, but the
		off-diagonal components are within floating-point precision of zero
		anyway.
		"""
		if self.n_rows == self.n_cols:
			result = matrix(self.n_rows * [self.n_cols * [0.]])
			result._m = matrix_invert(self._m[0], result._m)
			if result._m is not NULL:
				return result
			else:
				raise ArithmeticError("""\
Matrix is not invertible; determinant is zero.""")
		else:
			raise TypeError("""\
Cannot compute the inverse of a non-square matrix. \
Dimensions: (%d, %d)""" % (self.n_rows, self.n_cols))


	def transpose(self):
		r"""
		Compute the transpose of the matrix.

		**Signature**: x.tranpsose()

		Parameters
		----------
		x : ``matrix``
			An instance of this class.

		Returns
		-------
		trans : ``matrix``
			The transpose of ``x``, defined as :math:`x_{ij}^T = x_{ji}`.

		Example Code
		------------
		>>> from vice.modeling import matrix
		>>> import numpy as np
		>>> example = matrix.zeroes(5, 2)
		>>> for i in range(example.n_rows):
		>>>     for j in range(example.n_cols):
		>>>         example[i, j] = 10 * np.random.rand()
		>>> example
		matrix([9.49e-01    4.66e-01]
		       [8.03e+00    3.99e+00]
		       [8.58e-01    5.35e+00]
		       [9.48e+00    7.49e+00]
		       [2.01e+00    3.10e-01])
		>>> example.transpose()
		matrix([9.49e-01    8.03e+00    8.58e-01    9.48e+00    2.01e+00]
		       [4.66e-01    3.99e+00    5.35e+00    7.49e+00    3.10e-01])
		>>> matrix.identity(4).transpose()
		matrix([1.00e+00    0.00e+00    0.00e+00    0.00e+00]
		       [0.00e+00    1.00e+00    0.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00    1.00e+00    0.00e+00]
		       [0.00e+00    0.00e+00    0.00e+00    1.00e+00])
		>>> example = matrix.zeroes(2, 3)
		>>> for i in range(example.n_rows):
		>>>     for j in range(example.n_cols):
		>>>         example[i, j] = 10 * np.random.rand()
		>>> example
		matrix([3.15e+00    4.50e+00    1.29e+00]
		       [5.20e+00    4.62e+00    9.36e+00])
		>>> example.transpose()
		matrix([3.15e+00    5.20e+00]
		       [4.50e+00    4.62e+00]
		       [1.29e+00    9.36e+00])
		"""
		result = matrix(self.n_cols * [self.n_rows * [0.]])
		result._m = matrix_transpose(self._m[0], result._m)
		return result

