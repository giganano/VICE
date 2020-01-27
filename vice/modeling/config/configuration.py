
from __future__ import absolute_import 
from ...core.dataframe._configuration import c_configuration 


class configuration: 

	def __init__(self, settings, allowed_types, blockname): 
		self.__c_version = c_configuration(settings, allowed_types, blockname) 

	def __setitem__(self, key, value): 
		self.__c_version[key] = value 

	def __getitem__(self, key): 
		return self.__c_version[key] 

	def __repr__(self): 
		return self.__c_version.__repr__() 

	def __str__(self): 
		return self.__repr__() 

	def __enter__(self): 
		return self 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		return exc_value is None 	



