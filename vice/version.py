r""" 
This file implements the version_info class. 
""" 

from __future__ import absolute_import 
from . import version_breakdown 
import sys 
if sys.version_info[:] < tuple(
	[int(_) for _ in version_breakdown.MIN_PYTHON_VERSION.split('.')]): 
	raise RuntimeError("""This version of VICE requires python >= %s. \
Current version: %d.%d.%d""" % (version_breakdown.MIN_PYTHON_VERSION, 
		sys.version_info.major, sys.version_info.minor, 
		sys.version_info.micro)) 
else: pass 


class version_info: 

	r""" 
	VICE's version_info 
	
	- major : The major version number 
	- minor : The minor version number 
	- micro : The micro version number (also known as patch number) 
	- build : The build number 
	- __version__ : The version string <major>.<minor>.<micro> 
	- released : If True, this version of VICE has been released 

	.. note:: This object can be type-cast to a tuple of the form: 
		(major, minor, micro, build). 
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
		yield self.build 

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
	def build(self): 
		r""" 
		The build number 

		This is distinguished from the micro version number in that the build 
		number increases when there are errors associated with the 
		*distribution* of VICE, whereas the minor version number increases 
		when there are errors associated with VICE's code base itself. 
		""" 
		return version_breakdown.BUILD 

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

