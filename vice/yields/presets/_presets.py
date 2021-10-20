
from __future__ import absolute_import

__all__ = ["save", "remove"]

from ..._globals import _VERSION_ERROR_
from ..._globals import _DIRECTORY_
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
	input = raw_input
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError


def save(filename):

	r"""
	Save a permanent copy of yields stored in a given file for loading back
	into VICE at any time via an import statement.

	**Signature**: vice.yields.presets.save(filename)

	.. versionadded:: 1.1.0

	Parameters
	----------
	filename : ``str``
		The full or relative path to the script containing the yields to be
		saved. The name of this file will become the name of the preset to
		use in import statements.

	Raises
	------
	* RuntimeError
		- An exception occurs in attempting to import the file
		- The file is named JW20.py. This will always be the Johnson & Weinberg
		  (2020) preset file.
	* IOError
		- The file does not exist
	* TypeError
		- filename is not of type str

	Example Code
	------------
	The following in a file named "example.py":

	.. code:: python

		import vice
		vice.yields.ccsne.settings['o'] = 0.015
		vice.yields.ccsne.settings['fe'] = 0.0012
		vice.yields.sneia.settings['o'] = 0.0
		vice.yields.sneia.settings['fe'] = 0.0017

	And the following in the same directory as that file:

	>>> import vice
	>>> vice.yields.presets.save("example.py")

	This will enable the following from any directory:

	>>> import vice
	>>> from vice.yields.presets import example
	>>> vice.yields.ccsne.settings['o']
	0.015
	"""

	if isinstance(filename, strcomp):
		if filename.split('/')[-1] in ["__init__.py", "_presets.py"]:
			# Don't allow changing these files -> will break the module
			raise RuntimeError("""Cannot install module of name %s without \
modifying VICE's internal file structure. Please choose an alternate \
name.""" % (filename.split('/')[-1]))
		elif filename.split('/')[-1] == "JW20.py":
			raise RuntimeError("""Cannot overwrite Johnson & Weinberg (2020) \
yield presets. Please choose an alternate name.""")
		elif os.path.exists(filename):
			src_path = os.path.dirname(os.path.abspath(filename))
			old_path = os.getcwd()
			os.chdir(src_path)
			new_name = filename.split('/')[-1]
			if new_name.endswith(".py"): new_name = new_name[:-3]
			try:
				# simply try to import the file
				__import__(new_name)
				os.system("cp %s.py %syields/presets/" % (new_name,
					_DIRECTORY_))
			except Exception as exc:
				raise RuntimeError("""Could not import specified file. \
Error message: %s""" % (str(exc)))
			finally:
				os.chdir(old_path)
		else:
			raise IOError("File not found: %s" % (filename))
	else:
		raise TypeError("Argument must be of type str. Got: %s" % (
			type(filename)))



def remove(name, force = False):

	r"""
	Delete a copy of yield presets previously saved by a call to
	vice.yields.presets.save.

	**Signature** vice.yields.presets.remove(name, force = False)

	.. versionadded:: 1.1.0

	Parameters
	----------
	name : ``str``
		The name of the preset.
	force : ``bool`` [default : ``False``]
		If ``True``, will not stop for user confirmation before removing the
		yield file once it's found.

	Raises
	------
	* RuntimeError
		- The preset module is not found
		- Another exception occurs in attempting to remove the yield file.
	* IOError
		- The file does not exist

	Example Code
	------------
	>>> import vice
	>>> vice.yields.presets.remove("example")
	>>> from vice.yields.presets import example
	Traceback (most recent call last):
		File "<stdin>", line 1, in <module>
	ImportError: cannot import name 'example' from 'vice.yields.presets'
	(/anaconda3/lib/python3.7/site-packages/vice/yields/presets/__init__.py)

	.. seealso:: vice.yields.presets.save
	"""

	if isinstance(name, strcomp):
		forbidden_names = ["__init__.py", "_presets.py", "tests", "__pycache__"]
		if name in forbidden_names:
			"""
			A little smoke and mirrors to not allow the user to break this
			module.
			"""
			raise RuntimeError("Preset yield module not found: %s" % (
				name))
		elif name == "JW20.py":
			raise RuntimeError("""Cannot remove Johnson & Weinberg (2020) \
preset.""")
		else:
			"""
			Simply change into the presets directory, look for the file,
			remove it if it's there, and change one directory back
			"""
			old_path = os.getcwd()
			src_path = "%syields/presets/" % (_DIRECTORY_)
			if not name.endswith(".py"): name += ".py"
			if name in os.listdir(src_path):
				if force:
					# Simply set the confirmation response to yes in this case
					ans = "yes"
				else:
					"""
					Otherwise confirm the user's desire to remove the yield
					file. Show them the full path to be sure
					"""
					ans = input("""Uninstalling yield preset file located at \
%s%s. Continue? (y | n) """ % (src_path, name))
					while ans.lower() not in ["yes", "no", "y", "n"]:
						ans = input("Please enter either 'y' or 'n': ")
				if ans.lower() in ["y", "yes"]:
					os.chdir(src_path)
					try:
						os.system("rm -f %s" % (name))
					except Exception as exc:
						raise RuntimeError("""Could not uninstall yield file. \
Error message: %s""" % (str(exc)))
					finally:
						os.chdir(old_path)
				else:
					return 		# abort mission
			else:
				os.chdir(src_path)
				current_presets = list(filter(lambda x: x not in
					forbidden_names, os.listdir('.')))
				os.chdir(old_path)
				errmsg = """Preset yield module not found: %s. Currently \
installed presets: """ % (name)
				for i in current_presets:
					errmsg += "\n\t\t%s" % (i)
				raise ModuleNotFoundError(errmsg)
	else:
		raise TypeError("Argument must be of type str. Got: %s" % (
			type(name)))

