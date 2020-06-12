r""" 
This file implements the version_info class. 
""" 

from __future__ import absolute_import 
from . import version_breakdown 


class version_info: 

	r""" 
	VICE's version_info 
	
	- major : The major version number 
	- minor : The minor version number 
	- micro : The micro version number (also known as patch number) 
	- post : The post number 
	- __version__ : The version string <major>.<minor>.<micro> 
	- released : If True, this version of VICE has been released 
	""" 

	def __repr__(self): 
		return "%d.%d.%d" % (
			self.major, 
			self.minor, 
			self.micro 
		)  

	def __str__(self): 
		return self.__repr__() 

	def __iter__(self): 
		yield self.major 
		yield self.minor 
		yield self.micro 
		yield self.post 

	def __getitem__(self, key): 
		return tuple(self).__getitem__(key) 

	@property 
	def major(self): 
		r""" 
		The major version number. 
		""" 
		return version_breakdown.MAJOR 

	@property 
	def minor(self): 
		r""" 
		The minor version number. 
		""" 
		return version_breakdown.MINOR 

	@property 
	def micro(self): 
		r""" 
		The micro version number (also known as patch number). 
		""" 
		return version_breakdown.MICRO 

	@property 
	def post(self): 
		r""" 
		The post version number 
		""" 
		return version_breakdown.POST 

	@property 
	def __version__(self): 
		r""" 
		The version string <major>.<minor>.<micro> 
		""" 
		return self.__repr__() 

	@property 
	def released(self): 
		r""" 
		If True, this version of VICE has been released. 
		""" 
		return version_breakdown.RELEASED 


version = version_info() 

