# cython: language_level = 3, boundscheck = False

from .._globals import _VERSION_ERROR_
from ..core import _pyutils
from ._matrix import matrix
import numbers
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()

from libc.stdlib cimport malloc, realloc, free
from libc.string cimport strlen, strcmp
from ..core._cutils cimport set_string
from ..core.objects cimport _datum
# from ..core.dataframe._base cimport base as dataframe
from . cimport _datum


class datum:

	def __init__(self, obj):
		if isinstance(obj, dict):
			keys = list(obj.keys())
			values = [obj[key] for key in keys]
			self._vector = datavector(values)
			for key in keys: self.keys()._append(key)
		else:
			raise TypeError("""\
Only objects of type dict can be type-cast to a datum. \
Got: %s""" % (type(obj)))

	def __getitem__(self, key):
		return self._vector[self.keys().index(key)]

	def __setitem__(self, key, value):
		self._vector[self.keys().index(key)] = value

	def __repr__(self):
		rep = "vice.datum {\n"
		keys = self.keys()
		copy = self.todict()
		for key in keys:
			rep += "    %s " % (key)
			arrow = ""
			for _ in range(15 - len(key)): arrow += "-"
			rep += "%s> %s\n" % (arrow, str(copy[key]))
		rep += "}"
		return rep

	def keys(self):
		return self._vector.keys

	def todict(self):
		return dict(zip(self.keys(),
			[self._vector[_] for _ in range(self._vector.dim)]))


cdef class datavector(vector):

	def __cinit__(self, obj):
		# simply reallocate and point self._d at the inherited matrix object
		self._m = <MATRIX *> realloc (self._m, sizeof(DATUM))
		self._d = <DATUM *> self._m
		self._d[0].labels = NULL
		self._keys = datum_keys()

		# this line must come AFTER assigning self._d[0].labels to NULL or it
		# will cause an invalid old size error with realloc, leading to a
		# memory dump
		self._keys._keys = self._d[0].labels

		self._cov = covariance_matrix.identity(self.dim)
		self._d[0].cov = <COVARIANCE_MATRIX *> self._cov._cov

	@property
	def keys(self):
		return self._keys


cdef class datum_keys:

	def __cinit__(self):
		self._keys = NULL

	def __init__(self):
		self._n_keys = 0

	def __dealloc__(self):
		if self._keys is not NULL:
			for i in range(self._n_keys): free(self._keys[i])
			free(self._keys)
		else: pass

	def __len__(self):
		return int(self._n_keys)

	def __iter__(self):
		for i in range(self._n_keys): yield self[i]

	def __getitem__(self, key):
		if isinstance(key, numbers.Number) and key % 1 == 0:
			if 0 <= key < self._n_keys:
				return "".join(
					chr(self._keys[<unsigned short> key][_]) for _ in range(
						strlen(self._keys[<unsigned short> key])))
			else:
				raise IndexError("""\
Index out of bounds for datum_keys object of length %d: %d""" % (self.n_keys,
					int(key)))
		else:
			raise IndexError("Index must be a positive integer. Got: %s" % (
				type(key)))

	def _append(self, obj):
		if isinstance(obj, strcomp):
			if obj.lower in self: raise ValueError(
				"Duplicate datum key: %s" % (obj))
			self._n_keys += 1
			self._keys = <char **> realloc (self._keys,
				self._n_keys * sizeof(char *))
			self._keys[self._n_keys - 1] = <char *> malloc (
				<unsigned long> (len(obj) + 1) * sizeof(char))
			set_string(self._keys[self._n_keys - 1], obj.lower())
		else:
			raise TypeError("Datum key must be of type str. Got: %s" % (obj))

	def index(self, obj):
		cdef char *copy = NULL
		if isinstance(obj, strcomp):
			copy = <char *> malloc (
				<unsigned long> (len(obj) + 1) * sizeof(char))
			set_string(copy, obj.lower())
			for i in range(self._n_keys):
				if not strcmp(copy, self._keys[i]):
					free(copy)
					return i
				else: continue
			free(copy)
			raise IndexError("Key not in datum: %s" % (obj))
		else:
			raise IndexError("Datum key must be of type str. Got: %s" % (obj))


cdef class covariance_matrix(matrix):

	def __cinit__(self, obj):
		if self.n_rows != self.n_cols: raise TypeError("""\
Covariance matrix must have the same number of rows as columns. \
Got: (%d, %d)""" % (self.n_rows, self.n_cols))
		self._m = <MATRIX *> realloc (self._m, sizeof(COVARIANCE_MATRIX))
		self._cov = <COVARIANCE_MATRIX *> self._m
		self._cov[0].inv = NULL

	def __setitem__(self, key, value):
		super().__setitem__(key, value)
		if key[0] == key[1] and value < 0: raise ValueError("""\
Diagonal elements of covariance matrix must be positive. \
self[%d, %d] = %.2e""" % (key[0], key[1], self[key[0], key[1]]))
		self._cov[0].inv = NULL

	@property
	def inv(self):
		if self._cov[0].inv is NULL:
			self._inv = self.inverse()
			self._cov[0].inv = <MATRIX *> self._inv._m
		else: pass
		return self._inv

		
				










# cdef class c_datum(dataframe):

# 	def __cinit__(self, obj):
# 		if isinstance(obj, dict):
# 			keys = list(obj.keys())
# 			if all([isinstance(_, strcomp) for _ in keys]):
# 				values = [obj[_] for _ in keys]
# 				if all([isinstance(_, numbers.Number) for _ in values]):
# 					self._d = datum_initialize(
# 						<unsigned short> len(keys))
# 					for i in range(self.dim):
# 						self._d[0].labels[i] = <char *> malloc (
# 							(<unsigned long> len(keys[i]) + 1) * sizeof(char))
# 						set_string(self._d[0].labels[i], keys[i].lower())
# 				else:
# 					raise TypeError("Non-numerical value detected in datum.")
# 			else:
# 				raise TypeError("All datum keys must be strings.")
# 		else:
# 			raise TypeError("""Only objects of type dict can be type-cast into \
# a datum.""")

# 		self._cov = matrix.identity(self.dim)
# 		address = self._cov.__address()
# 		cdef char *copy = <char *> malloc (
# 			<unsigned long> (len(address) + 1) * sizeof(char))
# 		set_string(copy, address)
# 		link_cov_matrix(self._d, copy)
# 		free(copy)

# 	def __init__(self, obj):
# 		n = 0
# 		for key in obj.keys():
# 			self._d[0].data[0][n] = <double> obj[key]
# 			n += 1
# 		super().__init__({}) # set dataframe's _frame to empty dict


# 	def __dealloc__(self):
# 		datum_free(self._d)


# 	def __repr__(self):
# 		return super().__repr__().replace(
# 			"dataframe", "modeling.datum").replace(
# 			"matrix(", "covariance_matrix(\n       ")


# 	def __setitem__(self, key, value):
# 		if isinstance(key, strcomp):
# 			if key.lower() == "cov": raise KeyError("""\
# Covariance matrix should not be modified in this manner. For a datum x, please \
# instead call x.cov[i, j] to modify the ij'th element of the covariance \
# matrix.""")
# 			keys = list(self.keys())
# 			if key.lower() in keys():
# 				if isinstance(value, numbers.Number):
# 					idx = keys.index(key.lower())
# 					self._d[0].data[0][idx] = <double> value
# 				else:
# 					raise TypeError("""\
# Only numerical data can be stored. Got: %s""" % (type(value)))
# 			else:
# 				raise KeyError("Unrecognized datum key: %s" % (key))
# 		else:
# 			raise TypeError("Datum key must be of type str. Got: %s" % (
# 				type(key)))


# 	def __getitem__(self, key):
# 		if isinstance(key, strcomp):
# 			if key.lower() == "cov": return self.cov
# 			keys = list(self.keys())
# 			if key.lower() in keys:
# 				idx = keys.index(key.lower())
# 				return float(self._d[0].data[0][idx])
# 			else:
# 				raise KeyError("Unrecognized datum key: %s" % (key))
# 		else:
# 			raise TypeError("Datum key must be of type str. Got: %s" % (
# 				type(key)))


# 	@property
# 	def dim(self):
# 		r"""
# 		The dimensionality of the datum. See docstring in python subclass.
# 		"""
# 		return self._d[0].n_cols


# 	@property
# 	def cov(self):
# 		r"""
# 		The covariance matrix of the datum. See docstring in python subclass.
# 		"""
# 		return self._cov


# 	def quantities(self):
# 		r"""
# 		Obtain the descriptors of the quantities of the data vector. See
# 		docstring in python subclass.
# 		"""
# 		result = []
# 		# column vectors are stored under the hood only.
# 		for i in range(self.dim): result.append(
# 			"".join(chr(self._d[0].labels[i][j]) for j in range(
# 				strlen(self._d[0].labels[i]))))
# 		return result


# 	def keys(self):
# 		r"""
# 		Obtain the dataframe keys. This is the same as calling
# 		self.quantities, but with "cov" included at the end. See docstring in
# 		python subclass.
# 		"""
# 		return self.quantities() + ["cov"]


# 	def todict(self):
# 		r"""
# 		Type-cast the datum back to a dictionary. See docstring in python
# 		subclass.
# 		"""
# 		# column vectors are stored under the hood only.
# 		values = [self._d[0].data[0][_] for _ in range(self.dim)]
# 		values += [self.cov]
# 		return dict(zip(self.keys(), values))

