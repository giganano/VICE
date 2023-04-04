# cython: language_level = 3, boundscheck = False

from ..core._pyutils import copy_array_like_object
import numbers
from . cimport _vector

cdef class vector(matrix):

	r"""
	A generic vector object for linear algebra operations.

	**Signature**: vice.modeling.vector(arr)

	.. versionadded:: 1.X.0

	.. seealso:: vice.modeling.matrix

		This object inherits from the base class ``matrix`` in order to treat
		vectors the same as matrices with a single row.

	Parameters
	----------
	arr : ``array-like``
		The vector itself, type-casting a 1-dimensional array into a vector.
		Each element must be a numerical value.

	.. note::
		Once a vector object has been created, its size cannot be changed.
		If a change in size is necessary, please create a new vector object.

	Attributes
	----------
	dim : ``int``
		The dimensionality of the vector. Equivalent to ``len(x)`` for any
		vector ``x``.

	Functions
	---------
	zeroes : [classmethod]
		Returns a vector of a given dimensionality with each component set to
		zero.
	transpose : [instancemethod]
		Tranpose the vector from a row vector into a column vector.

		.. note::

			The returned vector will be of type ``matrix``, the base class,
			as opposed to ``vector``. All of the same functionality of vectors
			will proceed as normal. This inherited class simply handles row
			vectors as opposed to column vectors.

	Indexing and Item Assignment
	----------------------------
	Both proceed with a single integer (e.g., ``vec[0]`` or ``vec[1] = 0.8``),
	and the assigned value must be a real number. Negative indeces are not
	supported.

	Example Code
	------------
	>>> from vice.modeling import vector, matrix
	>>> import numpy as np

	A vector full of zeroes, which can act as a starting point for constructing
	other vectors, can be obtained with the ``vector.zeroes`` function:

	>>> example = vector.zeroes(4)
	>>> example
	vector([0.00e+00    0.00e+00    0.00e+00    0.00e+00])
	>>> example.dim
	4
	>>> len(example)
	4
	>>> example = vector.zeroes(3)
	vector([0.00e+00    0.00e+00    0.00e+00])
	>>> example.dim
	3
	>>> len(example)
	3

	Indexing and item assignment proceed with a single integer ``i`` to obtain
	or modify :math:`v_i`:

	>>> example = matrix.zeroes(3)
	>>> example[1] = 2
	>>> example
	vector([0.00e+00    2.00e+00    0.00e+00])
	>>> example[0]
	0.0
	>>> example[1]
	2.0
	>>> example[2] = 12
	>>> example
	vector([0.00e+00    2.00e+00    1.20e+01])

	Equivalence comparison returns ``True`` if and only if the vectors have the
	same dimensionality and each component passes an equivalence comparison
	(i.e., :math:`A_i = B_i` for :math:`i`).

	>>> x = vector([1, 2, 3])
	>>> y = vector([1, 2, 3])
	>>> x == y
	True
	>>> for i in range(len(y)): y[i] += 1
	>>> x == y
	False

	For vectors with the same dimensions, addition and subtraction proceed as
	usual with the ``+`` and ``-`` operators:

	>>> x
	vector([1.00e+00    2.00e+00    3.00e+00])
	>>> y
	vector([2.00e+00    3.00e+00    4.00e+00])
	>>> x + y
	vector([3.00e+00    5.00e+00    7.00e+00])
	>>> y - x
	vector([1.00e+00    1.00e+00    1.00e+00])

	The dot product of vectors with the same dimension can be computed with the
	``*`` operator:

	>>> x * y
	20.0
	>>> y * x
	>>> for i in range(len(y)): y[i] += 1
	>>> x * y
	26.0

	As this class implements row vectors as opposed to column vectors, the
	associated column vector can be obtained with the ``transpose`` function:

	>>> x.transpose()
	matrix([1.00e+00]
	       [2.00e+00]
	       [3.00e+00])
	>>> y.transpose()
	matrix([3.00e+00]
	       [4.00e+00]
	       [5.00e+00])

	Note however that the returned type is of the base class ``matrix`` as
	opposed to this class ``vector``. Nonetheless, the same functionality
	proceeds with the same syntax.

	>>> isinstance(x.transpose(), vector)
	False
	>>> isinstance(x. transpose(), matrix)
	True
	>>> isinstance(x, vector)
	True
	>>> isinstance(x, matrix)
	True
	"""

	def __cinit__(self, obj):
		if self.n_rows != 1: raise TypeError("""\
Vector must be a 1-dimensional array-like object containing only numerical \
values.""")


	def __len__(self):
		r"""
		Determine the number of quantities stored in the vector.

		.. seealso:: vice.modeling.vector.dim
		"""
		return self.dim


	def __iter__(self):
		r"""
		Iterates through each vector component
		"""
		for i in range(self.dim): yield self[i]


	def __repr__(self):
		r"""
		Returns a string representation of the vector.
		"""
		return super().__repr__().replace("matrix", "vector")


	def __getitem__(self, key):
		r"""
		Index the vector with self[key]. Key must be an integer.
		"""
		if isinstance(key, numbers.Number) and key % 1 == 0:
			try:
				return super().__getitem__((0, int(key)))
			except IndexError as exc:
				raise IndexError(str(exc).replace(
					"matrix", "vector").replace(
					"rows", "quantities").replace(
					"columns", "quantities"))
		else:
			raise IndexError("Index must be an integer. Got: %s" % (type(key)))


	def __setitem__(self, key, value):
		r"""
		Set self[key] to a new value. Key must be an integer, and value must
		be numerical.
		"""
		if isinstance(key, numbers.Number) and key % 1 == 0:
			try:
				super().__setitem__((0, int(key)), value)
			except IndexError as exc:
				raise IndexError(str(exc).replace(
					"matrix", "vector").replace(
					"rows", "quantities").replace(
					"columns", "quantities"))
		else:
			raise IndexError("Index must be an integer. Got: %s" % (type(key)))


	def __eq__(self, other):
		r"""
		Equivalence comparison between two vectors. Returns True if they are
		of the same dimensionality and each component-wise pair of elements
		passes the '==' equivalence test.
		"""
		if isinstance(other, vector):
			if self.dim == other.dim:
				result = True
				for i in range(self.dim):
					result &= self[i] == other[i]
					if not result: break
				return result
			else:
				return False
		else:
			return False


	def __add_matrices__(self, vector other):
		r"""
		Override the __add_matrices__ function of the parent class to accept a
		vector as opposed to a matrix.
		"""
		if self.dim == other.dim:
			result = vector(self.dim * [0.])
			result._m = matrix_add(self._m[0], other._m[0], result._m)
			return result
		else:
			raise ArithmeticError("""Vectors must be the same dimensionality \
for addition. Got: (%d, %d)""" % (self.dim, other.dim))


	def __sub_matrices__(self, vector other):
		r"""
		Overrides the inherited __sub_matrices__ to return a vector as opposed
		to a matrix.
		"""
		if self.dim == other.dim:
			result = vector(self.dim * [0.])
			result._m = matrix_subtract(self._m[0], other._m[0], result._m)
			return result
		else:
			raise ArithmeticError("""Vectors must be the same dimensionality \
for subtraction. Got: (%d, %d)""" % (self.dim, other.dim))


	def __mul__(self, other):
		r"""
		Multiplication of a vector with another vector, a matrix, or a scalar.

		.. seealso:: vice.modeling.matrix.__mul__
		"""
		# only need to check if multiplying by a matrix object that isn't a
		# vector subclass, otherwise the base class __mul__ function does the
		# trick.
		if isinstance(other, matrix) and not isinstance(other, vector):
			return super().__mul_matrices__(other)
		else:
			return super().__mul__(other)


	def __mul_matrices__(self, vector other):
		r"""
		Overrides the inherited __mul_matrices__ to return a vector as opposed
		to a matrix.
		"""
		if self.dim == other.dim:
			result = 0
			for i in range(self.dim): result += self[i] * other[i]
			return result
		else:
			raise ArithmeticError("""Vectors must be the same dimensionality \
for dot product. Got: (%d, %d)""" % (self.dim, other.dim))


	def __mul_scalar__(self, float other):
		r"""
		Overrides the inherited __mul_scalar__ to return a vector as opposed
		to a matrix.
		"""
		result = vector(self.dim * [0.])
		for i in range(self.dim): result[i] = other * self[i]
		return result


	@property
	def dim(self):
		r"""
		Type : ``int`` [positive definite]

		The number of quantities stored in the vector.

		.. note::

			This property can also be accessed with ``len(x)`` for any vector
			``x``.

		.. note::

			Once a vector object has been created, its size cannot be changed.
			If a change in size is necessary, please create a new vector
			object.

		Example Code
		------------
		>>> from vice.modeling import vector
		>>> example = vector([1, 2, 3])
		>>> example.dim
		3
		>>> len(example)
		3
		>>> example = vector([0, 0])
		>>> example.dim
		2
		"""
		return super().n_cols

	@classmethod
	def zeroes(cls, n):
		r"""
		Obtain a vector of a given size with every entry set to zero.

		**Signature**: vice.modeling.vector.zeroes(n)

		Parameters
		----------
		n : ``int``
			The dimensionality of the resultant vector.

		Returns
		-------
		vec : ``vector``
			A vector of the specified size, with every entry set to value of
			zero.

		Raises
		------
		* TypeError
			- ``n`` is not a numerical value.
		* ValueError
			- ``n`` is numerical, but not a positive integer.

		Example Code
		------------
		>>> from vice.modeling import vector
		>>> example = vector.zeroes(3)
		>>> example
		vector([0.00e+00    0.00e+00    0.00e+00])
		>>> example = vector.zeroes(4)
		>>> example
		vector([0.00e+00    0.00e+00    0.00e+00    0.00e+00])
		"""
		if isinstance(n, numbers.Number):
			if n % 1 == 0 and n > 0:
				return cls(int(n) * [0.])
			else:
				raise ValueError("""\
Vector dimensionality must be a positive integer. Got: %s""" % (str(n)))
		else:
			raise TypeError("""\
Vector dimensionality must be a positive integer. Got: %s""" % (type(n)))


	@classmethod
	def identity(cls, *args, **kwargs):
		r"""
		Raises a TypeError to disable the inherited function.
		"""
		raise TypeError("""\
This function is undefined for vector objects. Did you mean to call \
vice.modeling.matrix.identity instead?""")


	@classmethod
	def determinant(cls, *args, **kwargs):
		r"""
		Raises a TypeError to disable the inherited function.
		"""
		raise TypeError("""\
This function is undefined for vector objects. Did you mean to call \
vice.modeling.matrix.determinant instead?""")


	@classmethod
	def inverse(cls, *args, **kwargs):
		r"""
		Raises a TypeError to disable the inherited function.
		"""
		raise TypeError("""\
This function is undefined for vector objects. Did you mean to call \
vice.modeling.matrix.inverse instead?""")


	def transpose(self):
		r"""
		Turn the row vector into a column vector by taking its matrix
		transpose.

		**Signature**: x.transpose()

		Parameters
		----------
		x : ``vector``
			An instance of this class.

		Returns
		-------
		trans : ``matrix``
			The transpose of ``x``, defined as :math:`x_{1,i}^T = x_{i,1}`.

		.. warning::

			Since this class simply handles row vectors as opposed to column
			vectors, users should be aware that this function will return an
			instance of the base class ``matrix`` as opposed to an instance of
			the ``vector`` class. All of the same functionality of a ``vector``
			should proceed the same anyway. If column vectors must be
			distinguished from row vectors and other matrices, then this can be
			done by checking ``if mat.n_cols == 1`` for a given matrix ``mat``.

		Example Code
		------------
		>>> from vice.modeling import vector
		>>> example = vector([1, 2, 3])
		>>> example
		vector([1.00e+00    2.00e+00    3.00e+00])
		>>> trans = example.transpose()
		>>> trans
		matrix([1.00e+00]
			   [2.00e+00]
			   [3.00e+00])
		>>> isinstance(trans, vector) # see warning above
		False
		>>> isinstance(trans, matrix)
		True
		>>> example = vector([1, 2, 3, 4, 5])
		>>> example.transpose()
		matrix([1.00e+00]
			   [2.00e+00]
			   [3.00e+00]
			   [4.00e+00]
			   [5.00e+00])
		"""
		return super().transpose()

