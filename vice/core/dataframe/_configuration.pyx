# cython: language_level = 3, boundscheck = False 
""" 
This file implements the base class for a configuration object, which 
stores settings from a block of input from a vice-mc config file. 
""" 

from __future__ import absolute_import 
from ..._globals import _VERSION_ERROR_ 
import numbers 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from . cimport _configuration 


cdef class c_configuration(base): 


	def __init__(self, settings, allowed_types, blockname): 
		if self.__subinit__type_value_checks(settings, allowed_types, 
			blockname): 
			super().__init__(settings) 
			self._blockname = blockname.lower() 
			self._allowed_types = dict(zip(
				[i.lower() for i in allowed_types.keys()], 
				[allowed_types[i] for i in allowed_types.keys()] 
			)) 
		else: 
			raise SystemError("Internal Error.") 


	def __subinit__type_value_checks(self, settings, allowed_types, 
		blockname): 

		settings_errmsg = """\
Configuration object can only be instantiated from dictionary whose keys are \
of type str. \
""" 
		allowed_types_errmsg = """\
Allowed types must be a dictionary whose keys are the same as settings and \
the stored data must be lists of types. \
""" 
		if isinstance(blockname, strcomp): 
			if isinstance(settings, dict): 
				if all(map(lambda x: isinstance(x, strcomp), settings.keys())): 
					if isinstance(allowed_types, dict): 
						if all(map(lambda x: isinstance(x, strcomp), 
							allowed_types.keys())): 
							if list(set(allowed_types.keys())) == list(set(
								settings.keys())): 
								return True 
							else: 
								raise ValueError("""Keys between the two \
dataframes must match.""") 
				else: 
					raise TypeError(settings_errmsg) 
			else: 
				raise TypeError(settings_errmsg) 
		else: 
			raise TypeError("""Attribute 'blockname' must be of type str. \
Got: %s.""" % (type(blockname))) 

		return False 


	def __setitem__(self, key, value): 
		""" 
		Don't allow new keys, and the assigned value has to be in the allowed \
		types for that key. 
		""" 
		if self.__subset_type_value_checks(key, value): 
			if isinstance(value, strcomp): 
				self._frame[key.lower()] = value.lower() 
			elif isinstance(value, numbers.Number): 
				if value % 1 == 0: 
					self._frame[key.lower()] = int(value) 
				else: 
					self._frame[key.lower()] = float(value) 
			else: 
				self._frame[key.lower()] = value 
		else: 
			raise SystemError("Internal Error.") 
		

	def __subset_type_value_checks(self, key, value): 
		value_errmsg = """\
Unallowed type for setting '%s' in block '%s'. Got: %s. Allowed: \
""" % (key.lower(), self._blockname, type(value)) 
		if isinstance(key, strcomp): 
			if key.lower() in self.keys(): 
				for i in self._allowed_types[key.lower()]: 
					if isinstance(value, i): 
						return True 
					else: 
						continue 
				# if the code reaches here, a TypeError should be raised 
				value_errmsg += self._allowed_types[key.lower()][0] 
				for i in self._allowed_types[key.lower()][1:]: 
					value_errmsg += ", %s" % (i) 
				value_errmsg += "." 
				raise TypeError(value_errmsg) 
			else: 
				msg = """\
Unrecognized setting in block '%s'. Got: %s. Allowed: \
""" % (self._blockname, key.lower()) 
				msg += self.keys()[0] 
				for i in self.keys()[1:]: 
					msg += ", %s" % (i) 
				msg += "." 
				raise ValueError(msg) 
		else: 
			raise TypeError("""Item assignment must be done via type str. \
Got: %s.""" % (type(key))) 

		return False 


	def __repr__(self): 
		return super().__repr__().replace("dataframe", "configuration") 

	def __str__(self): 
		return super().__str__() 






