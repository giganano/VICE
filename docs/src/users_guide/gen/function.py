""" 
This file implements the object which generates the latex documentation 
for a function in VICE. 
""" 

import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	raise RuntimeError("Version never supported by VICE: %d.%d.%d" % (
		sys.version_info.major, sys.version_info.minor, sys.version_info.micro))  


class function: 

	""" 
	This class takes in a function and generates the latex documentation for 
	that function based on its docstring. 
	""" 

	def __init__(self, function, name): 
		self.function = function 
		self.name = name 

	@property 
	def function(self): 
		""" 
		Type :: <function> 

		The function whose documentation is to be generated 
		""" 
		return self._function 

	@function.setter 
	def function(self, value): 
		if callable(value): 
			self._function = value 
		else: 
			raise TypeError("Must be callable. Got: %s" % (type(value))) 

	@property 
	def doc(self): 
		""" 
		Type :: str 

		The docstring of the function. 
		""" 
		return self._function.__doc__ 

	@property 
	def name(self): 
		""" 
		Type :: str 

		The name of the function as users see it after running "import vice" 
		""" 
		return self._name 

	@name.setter 
	def name(self, value): 
		if isinstance(value, strcomp): 
			self._name = value 
		else: 
			raise TypeError("Must be of type str. Got: %s" % (type(value))) 
