
__all__ = ["matrix"]
from ._matrix import c_matrix
import numbers
import sys

class matrix(c_matrix):

	r"""
	A generic matrix object for linear algebra operations.

	**Signature**: vice.modeling.matrix(arr)

	Parameters
	----------
	arr : ``array-like``
		The matrix itself, type-casting a 2-dimensional array into a matrix.
		Must be rectangular (i.e., each "row," or element on the first axis,
		must be the same length as all of the others). Each element must be a
		numerical value.

	Attributes
	----------
	n_rows : ``int``
		The number of rows in the matrix (i.e., the number of elements along
		the first axis).
	n_cols : ``int``
		The number of columns in the matrix (i.e., the number of elements along
		the second axis).

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
	"""

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
			- One or both of ``n_rows`` and ``n_cols`` are not integers.

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
		if (isinstance(n_rows, numbers.Number) and n_rows % 1 == 0 and
			isinstance(n_cols, numbers.Number) and n_cols % 1 == 0):
			return cls(int(n_rows) * [int(n_cols) * [0.]])
		else:
			raise TypeError("""\
Matrix dimensions must be integers. Got: (%s, %s)""" % (type(n_rows),
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
		return super().determinant()


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
		matrix and its inverse is not *exactly* the identity matrix, though the
		off-diagonal components are within numerical precision of zero anyway.
		"""
		return super().inverse()


	def transpose(self):
		r"""
		Compute the transpose of a matrix.

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
		return super().transpose()

