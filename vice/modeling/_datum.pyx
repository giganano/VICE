# cython: language_level = 3, boundscheck = False

from .._globals import _VERSION_ERROR_
from ..core._pyutils import copy_array_like_object
from .matrix import matrix
import numbers
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()

from libc.stdlib cimport malloc, free
from libc.string cimport strlen
from libc.stdint cimport uintptr_t
from libc.stdio cimport sscanf
from ..core._cutils cimport set_string
from ..core.objects cimport _datum
from ..core.dataframe._base cimport base as dataframe
from . cimport _datum


cdef class c_datum(dataframe):

	def __cinit__(self, obj):
		if isinstance(obj, dict):
			keys = list(obj.keys())
			if all([isinstance(_, strcomp) for _ in keys]):
				values = [obj[_] for _ in keys]
				if all([isinstance(_, numbers.Number) for _ in values]):
					self._d = datum_initialize(
						<unsigned short> len(keys))
					for i in range(self.dim):
						self._d[0].labels[i] = <char *> malloc (
							(<unsigned long> len(keys[i]) + 1) * sizeof(char))
						set_string(self._d[0].labels[i], keys[i].lower())
				else:
					raise TypeError("Non-numerical value detected in datum.")
			else:
				raise TypeError("All datum keys must be strings.")
		else:
			raise TypeError("""Only objects of type dict can be type-cast into \
a datum.""")

		self._cov = matrix.identity(self.dim)
		address = self._cov.__address()
		cdef char *copy = <char *> malloc (
			<unsigned long> (len(address) + 1) * sizeof(char))
		set_string(copy, address)
		link_cov_matrix(self._d, copy)
		free(copy)

	def __init__(self, obj):
		n = 0
		for key in obj.keys():
			self._d[0].data[0][n] = <double> obj[key]
			n += 1
		super().__init__({}) # set dataframe's _frame to empty dict


	def __dealloc__(self):
		datum_free(self._d)


	def __repr__(self):
		return super().__repr__().replace(
			"dataframe", "modeling.datum").replace(
			"matrix(", "covariance_matrix(\n       ")


	def __setitem__(self, key, value):
		if isinstance(key, strcomp):
			if key.lower() == "cov": raise KeyError("""\
Covariance matrix should not be modified in this manner. For a datum x, please \
instead call x.cov[i, j] to modify the ij'th element of the covariance \
matrix.""")
			keys = list(self.keys())
			if key.lower() in keys():
				if isinstance(value, numbers.Number):
					idx = keys.index(key.lower())
					self._d[0].data[0][idx] = <double> value
				else:
					raise TypeError("""\
Only numerical data can be stored. Got: %s""" % (type(value)))
			else:
				raise KeyError("Unrecognized datum key: %s" % (key))
		else:
			raise TypeError("Datum key must be of type str. Got: %s" % (
				type(key)))


	def __getitem__(self, key):
		if isinstance(key, strcomp):
			if key.lower() == "cov": return self.cov
			keys = list(self.keys())
			if key.lower() in keys:
				idx = keys.index(key.lower())
				return float(self._d[0].data[0][idx])
			else:
				raise KeyError("Unrecognized datum key: %s" % (key))
		else:
			raise TypeError("Datum key must be of type str. Got: %s" % (
				type(key)))


	@property
	def dim(self):
		r"""
		The dimensionality of the datum. See docstring in python subclass.
		"""
		return self._d[0].n_cols


	@property
	def cov(self):
		r"""
		The covariance matrix of the datum. See docstring in python subclass.
		"""
		return self._cov


	def quantities(self):
		r"""
		Obtain the descriptors of the quantities of the data vector. See
		docstring in python subclass.
		"""
		result = []
		# column vectors are stored under the hood only.
		for i in range(self.dim): result.append(
			"".join(chr(self._d[0].labels[i][j]) for j in range(
				strlen(self._d[0].labels[i]))))
		return result


	def keys(self):
		r"""
		Obtain the dataframe keys. This is the same as calling
		self.quantities, but with "cov" included at the end. See docstring in
		python subclass.
		"""
		return self.quantities() + ["cov"]


	def todict(self):
		r"""
		Type-cast the datum back to a dictionary. See docstring in python
		subclass.
		"""
		# column vectors are stored under the hood only.
		values = [self._d[0].data[0][_] for _ in range(self.dim)]
		values += [self.cov]
		return dict(zip(self.keys(), values))

