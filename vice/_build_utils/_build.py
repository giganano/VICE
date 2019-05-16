"""
This file handles writing build parameters upon installation and reading them 
upon call from the user. 
"""

from __future__ import absolute_import
import Cython
import distutils 
import ctypes
import sys 
import pickle 




#------------------------------- BUILD WRITER -------------------------------# 
def write_build(): 
	"""
	Writes the version info for all packages that built the installed 
	version of VICE. 
	"""
	modules = [i for i in set(sys.modules) & set(globals())]
	modules.remove("sys")
	modules.remove("pickle")
	metadata = {}
	for i in modules: 
		metadata[sys.modules[i].__name__] = sys.modules[i].__version__
	metadata["python"] = "%d.%d.%d" % (sys.version_info[0], 
		sys.version_info[1], sys.version_info[2])
	pickle.dump(metadata, open("vice/_build_utils/build_data.obj", "wb"))




#------------------------------- BUILD READER -------------------------------# 
def read_build(): 
	"""
	Returns a dictionary showing the version info for the packages used to 
	build VICE at the time of installation. 
	"""
	from ..core._globals import _DIRECTORY
	return pickle.load(open("%s_build_utils/build_data.obj" % (_DIRECTORY), 
		"rb"))



