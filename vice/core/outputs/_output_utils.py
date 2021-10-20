"""
This file implements utility functions for handling simulation outputs. User
access or use of these functions is discouraged.
"""

from __future__ import absolute_import
from ..._globals import _VERSION_ERROR_
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()


def _get_name(name):
	"""
	Gets the name of a VICE output from the name that the user-specified.
	This takes into account whether or not they added the ".vice" extension.

	Args
	====
	name :: str
		The name the user specified

	Returns
	=======
	The name of the simulation as VICE would recognize it (i.e. the proper
	relative path from the current working directory).

	Raises
	======
	TypeError ::
		::	name is not a string
	"""
	if isinstance(name, strcomp):
		while name[-1] == '/':
			# Remove the '/' at the end of a directory name
			name = name[:-1]
		# Recognize the forced '.vice' extension
		if name.lower().endswith(".vice"):
			name = "%s.vice" % (name[:-5])
		else:
			name = "%s.vice" % (name)
		return name
	else:
		raise TypeError("'name' must be of type string. Got: %s" % (
			type(name)))


def _check_singlezone_output(name):
	"""
	Checks the output from a singlezone object to ensure that all files are
	there.

	Raises
	======
	IOError ::
		::	Output not found
		:: 	Files are missing
	"""
	singlezone_output_files = [
		"history.out",
		"mdf.out",
		"attributes",
		"yields"
	]
	name = _get_name(name)
	if not os.path.exists(name): # outputs not even there
		raise IOError("VICE output not found: %s" % (name))
	elif not all(list(map(lambda x: x in os.listdir(name),
		singlezone_output_files))):
		# certain files aren't there
		raise IOError("VICE output missing files: %s" % (name))
	else:
		# all good, proceed
		pass


def _is_multizone(filename):
	"""
	Determines if a path corresponds to the output from a multizone object.

	Args
	====
	filename :: str
		The user-specified path to the directory

	Returns
	=======
	True if the path contains output from a multizone object. False otherwise.

	Notes
	=====
	This function simply returns False in the event that a specified path is
	not a multizone object. It may instead be a singlezone object or some
	other file - this function does not determine that.
	"""
	name = _get_name(filename)
	if os.path.exists(filename):
		if os.path.isdir(filename):
			zones = list(filter(lambda x: x.endswith(".vice"),
				os.listdir(filename)))
			expected_files = [
				# "attributes", # removed for ``pickle`` keyword funcitonality
				# "migration",
				"tracers.out"
			]
			return (len(zones) >= 2 and
				all([i in os.listdir(filename) for i in expected_files]))
		else:
			return False
	else:
		return False


def _load_column_labels_from_file_header(filename):
	"""
	A subroutine used in initialization of both history and multioutput
	objects. Obtains the column labels from the header of a file in the
	appropriate format.

	Args
	====
	filename :: str
		The absolute or relative path to the file

	Raises
	======
	IOError ::
		::	file is not found
		::	file is not formatted correctly
	"""
	with open(filename, 'r') as f:
		line = f.readline()
		while line[0] == '#':
			if line.startswith("# COLUMN NUMBERS:"): break
			line = f.readline()
		if line[0] == '#':
			labels = []
			while line[0] == '#':
				line = f.readline().split()
				labels.append(line[2].lower())
			f.close()
			return tuple(labels[:-1])
		else:
			# bad formatting
			f.close()
			raise IOError("Output file not formatted correctly: %s" % (
				filename))

