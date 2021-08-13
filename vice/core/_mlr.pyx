# cython: language_level = 3, boundscheck = False 
r""" 
This file implements the user's global setting for the mass-lifetime relation 
and provides their functional forms for calling from python. 
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


class mlr: 

	def __init__(self): 
		self._vincenzo2016 = _vincenzo2016() 
		self._hpt2000 = _hpt2000() 
		self._ka1997 = _ka1997() 
		self._pm1993 = _pm1993() 
		self._mm1989 = _mm1989() 
		self._larson1974 = _larson1974() 

	@property 
	def vincenzo2016(self): 
		return self._vincenzo2016 

	@property 
	def hpt2000(self): 
		return self._hpt2000 

	@property 
	def ka1997(self): 
		return self._ka1997 

	@property 
	def pm1993(self): 
		return self._pm1993 

	@property 
	def mm1989(self): 
		return self._mm1989 

	@property 
	def larson1974(self): 
		return self._larson1974 


mlr = mlr() 


cdef class _vincenzo2016: 

	def __init__(self): 
		self._imported = 0 

	def __dealloc__(self): 
		if self._imported: 
			_mlr.vincenzo2016_free() 
		else: pass 

	def __call__(self, qty, postMS = 0.1, Z = 0.014, which = "mass"): 
		if not self._imported: self.__import() 
		mlr_error_handling(qty, postMS = postMS, Z = Z, which = which) 
		if qty == 0: 
			return float("inf") 
		else: 
			if which.lower() == "mass": 
				return _mlr.vincenzo2016_lifetime(<double> qty, <double> postMS, 
					<double> Z) 
			else: 
				return _mlr.vincenzo2016_turnoffmass(<double> qty, 
					<double> postMS, <double> Z) 

	def __import(self): 
		path = "%ssrc/ssp/mlr/vincenzo2016.dat" % (_DIRECTORY_) 
		if _mlr.vincenzo2016_import(path.encode("latin-1")): 
			raise SystemError("Internal Error.") 
		else: 
			self._imported = 1  


cdef class _hpt2000: 

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

	def __init__(self): 
		self._imported = 0 

	def __dealloc__(self): 
		if self._imported: 
			_mlr.ka1997_free() 
		else: pass 

	def __call__(self, qty, postMS = 0.1, Z = 0.014, which = "mass"): 
		if not self._imported: self.__import() 
		mlr_error_handling(qty, postMS = postMS, Z = Z, which = which) 
		if qty == 0: 
			return float("inf") 
		else: 
			if which.lower() == "mass": 
				return _mlr.ka1997_lifetime(<double> qty, <double> postMS, 
					<double> Z) 
			else: 
				return _mlr.ka1997_turnoffmass(<double> qty, <double> postMS, 
					<double> Z) 

	def __import(self): 
		path = "%ssrc/ssp/mlr/ka1997.dat" % (_DIRECTORY_) 
		if _mlr.ka1997_import(path.encode("latin-1")): 
			raise SystemError("Internal Error.") 
		else: 
			self._imported = 1 


cdef class _pm1993: 

	def __call__(self, qty, postMS = 0.1, Z = 0.014, which = "mass"): 
		mlr_error_handling(qty, postMS = postMS, Z = Z, which = which) 
		if qty == 0: 
			return float("inf") 
		else: 
			if which.lower() == "mass": 
				return _mlr.pm1993_lifetime(<double> qty, <double> postMS, 
					<double> Z) 
			else: 
				return _mlr.pm1993_turnoffmass(<double> qty, <double> postMS, 
					<double> Z) 

cdef class _mm1989: 

	def __call__(self, qty, postMS = 0.1, Z = 0.014, which = "mass"): 
		mlr_error_handling(qty, postMS = postMS, Z = Z, which = which) 
		if qty == 0: 
			return float("inf") 
		else: 
			if which.lower() == "mass": 
				return _mlr.mm1989_lifetime(<double> qty, <double> postMS, 
					<double> Z) 
			else: 
				return _mlr.mm1989_turnoffmass(<double> qty, <double> postMS, 
					<double> Z) 


cdef class _larson1974: 

	def __call__(self, qty, postMS = 0.1, Z = 0.014, which = "mass"): 
		mlr_error_handling(qty, postMS = postMS, Z = Z, which = which) 
		if qty == 0: 
			return float("inf") 
		else: 
			if which.lower() == "mass": 
				return _mlr.larson1974_lifetime(<double> qty, <double> postMS, 
					<double> Z) 
			else: 
				return _mlr.larson1974_turnoffmass(<double> qty, 
					<double> postMS, <double> Z) 


def mlr_error_handling(qty, postMS = 0.1, Z = 0.014, which = "mass"): 
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

