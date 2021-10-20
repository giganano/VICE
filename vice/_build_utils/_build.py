"""
This file handles writing build parameters upon installation and reading them
upon call from the user.
"""

from __future__ import absolute_import
try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError
try:
	import Cython
except (ModuleNotFoundError, NameError):
	# This exception will be handled in the setup file
	pass
import distutils
import sys
import os
import pickle
if sys.version_info[:2] == (2, 7):
	input = raw_input
else:
	pass


#------------------------------- BUILD WRITER -------------------------------#
def write_build():
	"""
	Writes the version info for all packages that built the installed
	version of VICE.
	"""
	modules = [i for i in set(sys.modules) & set(globals())]
	modules.remove("os")
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
	from .._globals import _DIRECTORY_
	return pickle.load(open("%s_build_utils/build_data.obj" % (_DIRECTORY_),
		"rb"))





#--------------------------- CHECK CYTHON FUNCTION ---------------------------#
def check_cython(minimum = "0.28.0"):
	"""
	Checks the user's version of Cython (or lackthereof) and raise a
	RuntimError if it's not >= the minimum.
	"""
	try:
		import Cython
	except (ModuleNotFoundError, ImportError):
		raise RuntimeError("""Please install Cython >= %s before installing \
VICE.""" % (minimum))
	if len([int(i) for i in Cython.__version__.split('.')]) == 2:
		Cython.__version__ += ".0"
	else:
		pass
	if (tuple([int(i) for i in Cython.__version__.split('.')]) <
		tuple([int(i) for i in minimum.split('.')])):
		raise RuntimeError("""Please update Cython to version >= %s before \
installing VICE. Current version: %s""" % (minimum, Cython.__version__))
	else:
		pass

