r"""
**VICE Developer's Documentation**

Developer's Toolkit

Contents
--------
set_logging_level : ``function``
	Adjust the amount of verbose output from VICE's backend for debugging and
	development purposes.
"""

from __future__ import absolute_import
from ._globals import _VERSION_ERROR_
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()


def set_logging_level(level = None):
	r"""
	Adjust the amount of verbose output from VICE's backend for debuggin and
	development purposes.

	**Signature**: vice._dev.set_logging_level(level = None)

	Parameters
	----------
	level : ``str`` [case-insensitive] or ``None`` [default]
		A string describing the level of output. ``None`` for no output at all.
		Recognized values:

			- "info"
				Print only descriptive statements about the current calculation.
			- "trace"
				Print the names of functions being called and in which file the
				function is implemented.
			- "debug"
				Print the names of functions being called, the files in which
				they are implemented, the line numbers calling the logging print
				statement, and variable states.

	Notes
	-----
	This function works by setting the environment variable "VICE_LOGGING_LEVEL"
	to "1", "2", or "3", integer values for which correspond to "info",
	"trace", and "debug" logging. This environment variable is detected by
	VICE's C library causing various functions to print (depending on the
	logging level) info and/or variable states to stderr.
	"""
	if isinstance(level, strcomp):
		# The values of the environment variables are #define'd in
		# vice/src/debug.h along with other debugging macros.
		if level.lower() == "info":
			os.environ["VICE_LOGGING_LEVEL"] = "1"
		elif level.lower() == "trace":
			os.environ["VICE_LOGGING_LEVEL"] = "2"
		elif level.lower() == "debug":
			os.environ["VICE_LOGGING_LEVEL"] = "3"
		else:
			raise ValueError("Unrecognized logging level: %s" % (level))
	elif level is None:
		if "VICE_LOGGING_LEVEL" in os.environ.keys():
			del os.environ["VICE_LOGGING_LEVEL"]
		else: pass
	else:
		raise TypeError("""Logging level must be either ``str`` or ``None``. \
Got: %s""" % (type(level)))

