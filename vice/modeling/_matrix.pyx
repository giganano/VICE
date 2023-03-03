# cython: language_level = 3, boundscheck = False

from ..core._pyutils import copy_array_like_object
import numbers

from libc.stdlib cimport malloc, free
from libc.string cimport strcat, strlen
from libc.stdio cimport sprintf
from ..core.objects cimport _matrix
from . cimport _matrix

cdef class c_matrix:

	def __cinit__(self, obj):
		msg = """\
Matrix must be a square 2-dimensional array-like object containing only \
numerical values.\
"""
		try:
			obj = copy_array_like_object(obj)
		except TypeError:
			raise TypeError(msg)
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
		for i in range(self.n_rows):
			for j in range(self.n_cols):
				self._m[0].matrix[i][j] = <double> obj[i][j]


	def __dealloc__(self):
		matrix_free(self._m)


	def __repr__(self):
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
		self.__indexing_error_handling__(key)
		return float(self._m[0].matrix[<unsigned short> key[0]][<unsigned short>
			key[1]])


	def __setitem__(self, key, value):
		self.__indexing_error_handling__(key)
		if isinstance(value, numbers.Number):
			self._m[0].matrix[<unsigned short> key[0]][<unsigned short>
				key[1]] = <double> value
		else:
			raise TypeError("""\
Item assignment requires a numerical value. Got: %s""" % (type(value)))


	def __indexing_error_handling__(self, key):
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
		if isinstance(other, c_matrix):
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


	def __mul__(self, other):
		if not isinstance(self, c_matrix): 
			# allows commutativity for scalar multiplication -> other must be a
			# c_matrix if this function is getting called at all.
			return other.__mul__(self)
		elif isinstance(other, c_matrix):
			return self.__multiply_matrix__(other)
		elif isinstance(other, numbers.Number):
			return self.__multiply_scalar__(float(other))
		else:
			raise TypeError("""\
Matrix multiplication only possible with scalar or another matrix. \
Got: %s""" % (type(other)))


	def __multiply_matrix__(self, c_matrix other):
		if self.n_cols == other.n_rows:
			result = c_matrix(self.n_rows * [other.n_cols * [0.]])
			result._m = matrix_multiply(self._m[0], other._m[0], result._m)
			return result
		else:
			raise ArithmeticError("""\
Incompatible matrix dimensions for multiplication. Self: %d rows, %d columns. \
Other: %d rows, %d columns.""" % (
				self.n_rows, self.n_cols, other.n_rows, other.n_cols))


	def __multiply_scalar__(self, float other):
		result = c_matrix(self.n_rows * [self.n_cols * [0.]])
		for i in range(self.n_rows):
			for j in range(self.n_cols):
				result[i, j] = other * self._m[0].matrix[i][j]
		return result


	def __address(self):
		r"""
		Obtain the address of the matrix pointer in C as a string. Used in the
		process of linking covariances matrices to their respective data
		vectors.
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
		The number of rows in the matrix. See docstring in matrix.py.
		"""
		return self._m[0].n_rows


	@property
	def n_cols(self):
		r"""
		The number of columns in the matrix. See docstring in matrix.py.
		"""
		return self._m[0].n_cols


	def determinant(self):
		r"""
		Compute the determinant of the matrix. See docstring in matrix.py.
		"""
		if self.n_rows == self.n_cols:
			return float(matrix_determinant(self._m[0]))
		else:
			raise TypeError("""\
Cannot compute the determinant of a non-square matrix. \
Dimensions: (%d, %d)""" % (self.n_rows, self.n_cols))


	def inverse(self):
		r"""
		Compute the inverse matrix. See docstring in matrix.py.
		"""
		if self.n_rows == self.n_cols:
			result = c_matrix(self.n_rows * [self.n_cols * [0.]])
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
		Compute the transpose of the matrix. See docstring in matrix.py.
		"""
		result = c_matrix(self.n_cols * [self.n_rows * [0.]])
		result._m = matrix_transpose(self._m[0], result._m)
		return result

