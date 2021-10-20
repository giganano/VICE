# cython: language_level = 3, boundscheck = False
r"""
This file links the mass-lifetime relationship features between Python and C.
"""

from .._globals import _DIRECTORY_
from .._globals import _VERSION_ERROR_
import numbers
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from . cimport _mlr


cdef class _mlr_linker:

	# The following are maps to and from the hash-codes #define'd in
	# vice/src/ssp/mlr.h.

	__NAMES__ = {
		"powerlaw": 881,
		"vincenzo2016": 1077,
		"hpt2000": 526,
		"ka1997": 422,
		"pm1993": 435,
		"mm1989": 437,
		"larson1974": 868
	}

	__HASHCODES__ = {
		881: "powerlaw",
		1077: "vincenzo2016",
		526: "hpt2000",
		422: "ka1997",
		435: "pm1993",
		437: "mm1989",
		868: "larson1974"
	}

	# Not using a @property object for setting here b/c it would get overridden
	# by the subclass in mlr.py -> these names will persist in the subclass
	# even when setting is @property'd.

	@staticmethod
	def _get_setting():
		# see docstring in vice/core/mlr.py
		return _mlr_linker.__HASHCODES__[_mlr.get_mlr_hashcode()]

	@staticmethod
	def _set_setting(value):
		if isinstance(value, strcomp):
			if value.lower() in _mlr_linker.__NAMES__.keys():
				if _mlr.set_mlr_hashcode(
					<unsigned short> _mlr_linker.__NAMES__[value.lower()]):
					raise SystemError("Internal Error.")
				else: pass
			else:
				raise ValueError("Unrecognized MLR setting: %s" % (value))
		else:
			raise TypeError("MLR setting must be of type str. Got: %s" % (
				type(value)))


cdef class _powerlaw:

	r"""
	See mlr.powerlaw property docstring
	"""

	def __call__(self, qty, postMS = 0.1, which = "mass"):
		mlr_error_handling(qty, postMS = postMS, Z = 0.014, which = which)
		if qty == 0:
			return float("inf")
		else:
			if which.lower() == "mass":
				return _mlr.powerlaw_lifetime(<double> qty, <double> postMS,
					0.014)
			else:
				return _mlr.powerlaw_turnoffmass(<double> qty, <double> postMS,
					0.014)


cdef class _vincenzo2016:

	r"""
	See mlr.vincenzo2016 property docstring
	"""

	def __init__(self):
		self._imported = 0

	def __dealloc__(self):
		if self._imported:
			_mlr.vincenzo2016_free()
		else: pass

	def __call__(self, qty, Z = 0.014, which = "mass"):
		if not self._imported: self.__import()
		mlr_error_handling(qty, postMS = 0, Z = Z, which = which)
		if qty == 0:
			return float("inf")
		else:
			if which.lower() == "mass":
				return _mlr.vincenzo2016_lifetime(<double> qty, 0.0, <double> Z)
			else:
				return _mlr.vincenzo2016_turnoffmass(<double> qty, 0.0,
					<double> Z)

	def __import(self):
		path = "%ssrc/ssp/mlr/vincenzo2016.dat" % (_DIRECTORY_)
		if _mlr.vincenzo2016_import(path.encode("latin-1")):
			raise SystemError("Internal Error.")
		else:
			self._imported = 1


cdef class _hpt2000:

	r"""
	See mlr.hpt2000 property docstring
	"""

	def __init__(self):
		self._imported = 0

	def __dealloc__(self):
		if self._imported:
			_mlr.hpt2000_free()
		else: pass

	def __call__(self, qty, postMS = 0.1, Z = 0.014, which = "mass"):
		if not self._imported: self.__import()
		mlr_error_handling(qty, postMS = postMS, Z = Z, which = which)
		if qty == 0:
			return float("inf")
		else:
			if which.lower() == "mass":
				return _mlr.hpt2000_lifetime(<double> qty, <double> postMS,
					<double> Z)
			else:
				return _mlr.hpt2000_turnoffmass(<double> qty, <double> postMS,
					<double> Z)

	def __import(self):
		path = "%ssrc/ssp/mlr/hpt2000.dat" % (_DIRECTORY_)
		if _mlr.hpt2000_import(path.encode("latin-1")):
			raise SystemError("Internal Error.")
		else:
			self._imported = 1


cdef class _ka1997:

	r"""
	See mlr.ka1997 property docstring
	"""

	def __init__(self):
		self._imported = 0

	def __dealloc__(self):
		if self._imported:
			_mlr.ka1997_free()
		else: pass

	def __call__(self, qty, Z = 0.014, which = "mass"):
		if not self._imported: self.__import()
		mlr_error_handling(qty, postMS = 0, Z = Z, which = which)
		if qty == 0:
			return float("inf")
		else:
			if which.lower() == "mass":
				return _mlr.ka1997_lifetime(<double> qty, 0.0, <double> Z)
			else:
				return _mlr.ka1997_turnoffmass(<double> qty, 0.0, <double> Z)

	def __import(self):
		path = "%ssrc/ssp/mlr/ka1997.dat" % (_DIRECTORY_)
		if _mlr.ka1997_import(path.encode("latin-1")):
			raise SystemError("Internal Error.")
		else:
			self._imported = 1


cdef class _pm1993:

	r"""
	See mlr.pm1993 property docstring
	"""

	def __call__(self, qty, postMS = 0.1, which = "mass"):
		mlr_error_handling(qty, postMS = postMS, Z = 0.014, which = which)
		if qty == 0:
			return float("inf")
		else:
			if which.lower() == "mass":
				return _mlr.pm1993_lifetime(<double> qty, <double> postMS,
					<double> 0.014)
			else:
				return _mlr.pm1993_turnoffmass(<double> qty, <double> postMS,
					<double> 0.014)

cdef class _mm1989:

	r"""
	See mlr.mm1989 property docstring
	"""

	def __call__(self, qty, postMS = 0.1, which = "mass"):
		mlr_error_handling(qty, postMS = postMS, Z = 0.014, which = which)
		if qty == 0:
			return float("inf")
		else:
			if which.lower() == "mass":
				return _mlr.mm1989_lifetime(<double> qty, <double> postMS,
					0.014)
			else:
				return _mlr.mm1989_turnoffmass(<double> qty, <double> postMS,
					0.014)


cdef class _larson1974:

	r"""
	See mlr.larson1974 property docstring
	"""

	def __call__(self, qty, postMS = 0.1, which = "mass"):
		mlr_error_handling(qty, postMS = postMS, Z = 0.014, which = which)
		if qty == 0:
			return float("inf")
		else:
			if which.lower() == "mass":
				return _mlr.larson1974_lifetime(<double> qty, <double> postMS,
					0.014)
			else:
				return _mlr.larson1974_turnoffmass(<double> qty,
					<double> postMS, 0.014)


def mlr_error_handling(qty, postMS = 0.1, Z = 0.014, which = "mass"):
	r"""
	Error handling for the mass-lifetime relations implemented here.

	Parameters
	----------
	qty : float
		Either the mass of a star in :math:`M_\odot` or the age of a
		stellar population in Gyr. Interpretation set by the keyword
		argument ``which``.
	postMS : float [default : 0.1]
		The ratio of a star's post main sequence to main sequence lifetime.
		Zero to compute the main sequence lifetime alone. Not relevant for the
		Kodama & Arimoto (1997) [1]_ and Vincenzo et al. (2016) [2]_ forms.
	Z : float [default : 0.014]
		The metallicity by mass of the stellar population. Only the Vincenzo et
		al. (2016) [2]_, Hurley, Pols & Tout (2000) [3]_, and Kodama & Arimoto
		(1997) [1]_ formulations are metallicity dependent.
	which : str [case-insensitive] [default : "mass"]
		The interpretation of ``qty``: either ``"mass"`` or ``"age"``. If
		``which == "mass"``, then the user has passed a stellar mass and the
		function will calculate a lifetime, else the mass of a star with the
		specified lifetime will be computed.

	.. [1] Kodama & Arimoto (1997), A&A, 320, 41
	.. [2] Vincenzo et al. (2016), MNRAS, 460, 2238
	.. [3] Hurley, Pols & Tout (2000), MNRAS, 315, 543
	"""
	if not isinstance(qty, numbers.Number):
		raise TypeError("Must be a numerical value. Got: %s" % (type(qty)))
	elif qty < 0:
		raise ValueError("Value must be non-negative.")
	elif not isinstance(postMS, numbers.Number):
		raise TypeError("""Keyword arg 'postMS' must be a numerical value. \
Got: %s""" % (type(postMS)))
	elif postMS < 0:
		raise ValueError("Keyword arg 'postMS' must be non-negative.")
	elif not isinstance(Z, numbers.Number):
		raise TypeError("Keyword arg 'Z' must be a numerical value. Got: %s" % (
			type(Z)))
	elif Z < 0 or Z > 1:
		raise ValueError("Keyword arg 'Z' must be between 0 and 1.")
	elif not isinstance(which, strcomp):
		raise TypeError("Keyword arg 'which' must be of type str. Got: %s" % (
			type(which)))
	elif which.lower() not in ["mass", "age"]:
		raise ValueError("""Keyword arg 'which' must be either 'mass' or 'age'
(case-insensitive). Got: %s""" % (which))
	else:
		pass

