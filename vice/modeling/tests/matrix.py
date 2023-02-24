
from ..matrix import matrix
from ...testing import moduletest
from ...testing import unittest
import random

_TEST_MATRIX_SIZE_ = (5, 3)


@moduletest
def test():
	r"""
	vice.modeling.matrix module test
	"""
	return ["vice.modeling.matrix",
		[
			test_initialize(),
			test_setitem(),
			test_getitem(),
			test_eq(),
			test_mul(),
			test_nrows(),
			test_ncols(),
			test_determinant(),
			test_inverse(),
			test_transpose(),
			test_zeroes(),
			test_identity()
		]
	]


@unittest
def test_initialize():
	r"""
	vice.modeling.matrix.__init__ unit test
	"""
	def test():
		global _TEST_
		arr = _TEST_MATRIX_SIZE_[0] * [None]
		for i in range(len(arr)):
			arr[i] = _TEST_MATRIX_SIZE_[1] * [None]
			for j in range(len(arr[i])):
				arr[i][j] = i + j
		try:
			_TEST_ = matrix(arr)
		except:
			return False
		success = isinstance(_TEST_, matrix)
		for i in range(_TEST_MATRIX_SIZE_[0]):
			for j in range(_TEST_MATRIX_SIZE_[1]):
				try:
					success &= _TEST_[i, j] == i + j
				except:
					return False
				if not success: break
			if not success: break
		return success
	return ["vice.modeling.matrix.__init__", test]


@unittest
def test_setitem():
	r"""
	vice.modeling.matrix.__setitem__ unit test
	"""
	def test():
		success = True
		for i in range(_TEST_MATRIX_SIZE_[0]):
			for j in range(_TEST_MATRIX_SIZE_[1]):
				try:
					_TEST_[i, j] = 0
				except:
					return False
				try:
					success &= _TEST_[i, j] == 0
				except:
					return None
				if not success: break
				try:
					_TEST_[i, j] = i * j
				except:
					return False
				try:
					success &= _TEST_[i, j] == i * j
				except:
					return None
				if not success: break
			if not success: break
		return success
	return ["vice.modeling.matrix.__setitem__", test]


@unittest
def test_getitem():
	r"""
	vice.modeling.matrix.__getitem__ unit test
	"""
	def test():
		success = True
		for i in range(_TEST_MATRIX_SIZE_[0]):
			for j in range(_TEST_MATRIX_SIZE_[1]):
				try:
					success &= _TEST_[i, j] == i * j
				except:
					return False
				if not success: break
				try:
					_TEST_[i, j] = i + j
				except:
					return None
				try:
					success &= _TEST_[i, j] == i + j
				except:
					return False
				if not success: break
			if not success: break
		return success
	return ["vice.modeling.matrix.__getitem__", test]


@unittest
def test_eq():
	r"""
	vice.modeling.matrix.__eq__ unit test
	"""
	def test():
		try:
			copy = matrix(
				_TEST_MATRIX_SIZE_[0] * [_TEST_MATRIX_SIZE_[1] * [0.]])
		except:
			return None
		for i in range(_TEST_MATRIX_SIZE_[0]):
			for j in range(_TEST_MATRIX_SIZE_[1]):
				try:
					copy[i, j] = _TEST_[i, j]
				except:
					return None
		try:
			return copy == _TEST_
		except:
			return False
	return ["vice.modeling.matrix.__eq__", test]


@unittest
def test_mul():
	r"""
	vice.modeling.matrix.__mul__ unit test
	"""
	def test():
		success = True
		try:
			other = matrix.identity(_TEST_MATRIX_SIZE_[1])
		except:
			return None
		try:
			result = _TEST_ * other
			success &= result == _TEST_
		except:
			return False
		try:
			other = matrix.zeroes(_TEST_MATRIX_SIZE_[1], _TEST_MATRIX_SIZE_[1])
		except:
			return None
		try:
			result = _TEST_ * other
			success &= result != _TEST_
			for i in range(_TEST_MATRIX_SIZE_[0]):
				for j in range(_TEST_MATRIX_SIZE_[1]):
					success &= result[i, j] == 0
					if not success: break
				if not success: break
		except:
			return False
		try:
			other = 2 * _TEST_
			for i in range(_TEST_MATRIX_SIZE_[0]):
				for j in range(_TEST_MATRIX_SIZE_[1]):
					success &= other[i, j] == 2 * _TEST_[i, j]
					if not success: break
				if not success: break
		except:
			return False
		return success
	return ["vice.modeling.matrix.__mul__", test]


@unittest
def test_nrows():
	r"""
	vice.modeling.matrix.n_rows unit test
	"""
	def test():
		return _TEST_.n_rows == _TEST_MATRIX_SIZE_[0]
	return ["vice.modeling.matrix.n_rows", test]


@unittest
def test_ncols():
	r"""
	vice.modeling.matrix.n_cols unit test
	"""
	def test():
		return _TEST_.n_cols == _TEST_MATRIX_SIZE_[1]
	return ["vice.modeling.matrix.n_cols", test]


@unittest
def test_determinant():
	r"""
	vice.modeling.matrix.determinant unit test
	"""
	def test():
		success = True
		random.seed() # no arg -> seeds based on system time
		for i in range(2, 8): # square matrix sizes 2x2 through 8x8
			try:
				test = matrix.identity(i)
			except:
				return None
			try:
				success &= test.determinant() == 1
			except:
				return False
			if not success: break
			for j in range(test.n_rows):
				try:
					test[j, j] = 10 * random.random()
				except:
					return None
			product = 1
			for j in range(test.n_rows): product *= test[j, j]
			try:
				success &= abs(test.determinant() - product) / product < 1.e-15
			except:
				return False
			if not success: break
		return success
	return ["vice.modeling.matrix.determinant", test]


@unittest
def test_inverse():
	r"""
	vice.modeling.matrix.inverse unit test
	"""
	def test():
		success = True
		random.seed() # no arg -> seeds based on system time
		for i in range(2, 8): # square matrix sizes 2x2 through 8x8
			try:
				test = matrix.zeroes(i, i)
			except:
				return None
			while True:
				for i in range(test.n_rows):
					for j in range(test.n_cols):
						try:
							test[i, j] = 10 * random.random()
						except:
							return None
				if test.determinant(): break # make sure it's invertible

			def compare_to_identity_matrix(prod):
				r"""
				Test the product of a matrix and its computed inverse to
				ensure that it is close enough to the identity matrix.
				"""
				result = True
				for i in range(prod.n_rows):
					for j in range(prod.n_cols):
						try:
							# though floating point error is 10^-15, in
							# practice, the 8x8 matrix sometimes has a few
							# off-diagonal elements at or just above this value,
							# so the maximum threshold is increased a bit.
							result &= abs(prod[i, j] - int(i == j)) < 1e-13
						except:
							return None
						if not result: break
					if not result: break
				return result

			try:
				inv = test.inverse()
			except:
				return None

			product = test * inv
			success &= compare_to_identity_matrix(product)
			product = inv * test
			success &= compare_to_identity_matrix(product)
			if not success: break
		return success
	return ["vice.modeling.matrix.inverse", test]
		

@unittest
def test_transpose():
	r"""
	vice.modeling.matrix.transpose unit test
	"""
	def test():
		success = True
		random.seed() # no arg -> seed based on system time
		try:
			trans = _TEST_.transpose()
		except:
			return False
		try:
			success &= trans.n_rows == _TEST_.n_cols
			success &= trans.n_cols == _TEST_.n_rows
		except:
			return None
		for i in range(_TEST_MATRIX_SIZE_[0]):
			for j in range(_TEST_MATRIX_SIZE_[1]):
				try:
					success &= _TEST_[i, j] == trans[j, i]
				except:
					return None
				if not success: break
			if not success: break
		for i in range(20): # some number of randomly generated matrices to test
			try:
				test = matrix.zeroes(2 + int(8 * random.random()),
					2 + int(8 * random.random()))
			except:
				return None
			for j in range(test.n_rows):
				for k in range(test.n_cols):
					try:
						test[j, k] = 10 * random.random()
					except:
						return None
			try:
				trans = test.transpose()
			except:
				return False
			for j in range(test.n_rows):
				for k in range(test.n_cols):
					try:
						success &= test[j, k] == trans[k, j]
					except:
						return None
					if not success: break
				if not success: break
			if not success: break
		return success
	return ["vice.modeling.matrix.transpose", test]


@unittest
def test_zeroes():
	r"""
	vice.modeling.matrix.zeroes unit test
	"""
	def test():
		success = True
		random.seed() # no arg -> seed based on system time
		for i in range(20): # some number of randomly generated test cases
			try:
				test = matrix.zeroes(2 + int(8 * random.random()),
					2 + int(8 * random.random()))
			except:
				return False
			for j in range(test.n_rows):
				for k in range(test.n_cols):
					try:
						success &= test[j, k] == 0
					except:
						return None
					if not success: break
				if not success: break
			if not success: break
		return success
	return ["vice.modeling.matrix.zeroes", test]


@unittest
def test_identity():
	r"""
	vice.modeling.matrix.identity unit test
	"""
	def test():
		success = True
		for i in range(2, 9): # range of matrix sizes: 2x2 through 8x8
			try:
				test = matrix.identity(i)
			except:
				return False
			try:
				success &= test == test.inverse()
			except:
				return None
			for j in range(test.n_rows):
				for k in range(test.n_cols):
					try:
						success &= test[j, k] == int(j == k)
					except:
						return None
					if not success: break
				if not success: break
			if not success: break
		return success
	return ["vice.modeling.matrix.identity", test]



