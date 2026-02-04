#!/usr/bin/env python
#
# This file is part of the VICE package.
# Copyright (C) 2019 James W. Johnson (giganano9@gmail.com)
# License: MIT License. See LICENSE in top-level directory
# at https://github.com/giganano/VICE.git.
r"""
This setup script should not be called directly. Instead, one should run

$ python -m pip install [--editable] .

which will invoke the ``pyproject.toml`` file in this directory, which in turn
runs this script as needed.

How to Link OpenMP
------------------
A few simple steps can link VICE with the OpenMP library to enable
multithreading. If you are a Mac OS user, you should first install OpenMP using
Homebrew (see https://vice-astro.readthedocs.io/en/latest/install.html for
guidance). Then, simply assign the environment variable

$ export VICE_ENABLE_OPENMP=true

and run the ``pip install`` command above as usual.

For Developers
--------------
VICE developers can set an environment variable that allows individual
extensions to be recompiled without recompiling the whole package. This
approach can minimize compile time when working on modifications that get
compiled into only one or a few Cython extensions, since recompiling all
extensions can take several minutes. To specify these extensions, simply
specify a comma-separated list of the extension names to be recompiled as an
environment variable named ``VICE_SETUP_EXTENSIONS``. For example:

$ export VICE_SETUP_EXTENSIONS=vice.core.ssp._ssp

or

$ export VICE_SETUP_EXTENSIONS=vice.core.ssp._ssp,vice.core._cutils

To disable this behavior, simply remove the environment variable:

$ unset VICE_SETUP_EXTENSIONS

If the source file to a given extension is not found, a ``RuntimeError``
will be raised.
"""

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext
from subprocess import Popen, PIPE
import json
import os
if os.name != "posix": raise OSError("""\
Sorry, Windows is not supported. Please install and run VICE from within the \
Windows Subsystem for Linux.""")


class discovery:

	r"""
	A class that traverses the VICE source tree and compiles the required or
	specified Cython extensions. The function ``build_extensions`` should be
	called as the "main" method of this class.
	"""

	@staticmethod
	def build_extensions(path = './vice'):
		r"""
		Constructs each of the Cython ``Extension`` objects to be compiled.

		Parameters
		----------
		path : str [default : './vice']
			The path to the package directory

		Returns
		-------
		exts : list
			A list of ``Extension`` objects to build.

		Raises
		------
		* RuntimeError
			- Invalid extension (file not found)
		"""
		kwargs = {
			"include_dirs": ["%s/src" % (path)],
			"library_dirs": [],
			"extra_compile_args": ["-Wno-unreachable-code"],
			"extra_link_args": []
		}
		for root, dirs, files in os.walk(kwargs["include_dirs"][0]):
			for d in dirs:
				kwargs["include_dirs"].append("%s/%s" % (root, d))
		if openmp.link_openmp():
			# more compiler flags necessary if enabling multithreading
			compile_args, link_args = openmp.compiler_flags()
			kwargs["extra_compile_args"] = []
			kwargs["extra_link_args"] = []
			if openmp.compiler().startswith("clang"):
				# openmp.compiler() finds the necessary library and include
				# directory directly for clang. This is not necessary for gcc
				# because it comes with OpenMP comes with OpenMP linked out of
				# the box.
				libomp_include, libomp_library = openmp.find_openmp_clang()
				kwargs["include_dirs"].append(libomp_include)
				kwargs["library_dirs"].append(libomp_library)
			else: pass
		else: pass

		extensions = []
		names = discovery.get_extensions(path = path)
		for name in names:
			srcfile = "%s.pyx" % (name.replace('.', '/'))
			extensions.append(
				Extension(name, [srcfile] + discovery.get_c_srcfiles(
					name, path = path), **kwargs)
			)
		return extensions


	@staticmethod
	def get_extensions(path = "./vice"):
		r"""
		Determine the names of the extensions to compile.

		.. tip::

			You can specify specific packages to install by setting the
			environment variable ``VICE_SETUP_EXTENSIONS`` to a comma-separated
			list of the extension names to be recompiled. All others will be
			skipped.

		Parameters
		----------
		path : ``str`` [default : "./vice"]
			The path to the package directory.

		Returns
		-------
		extensions : ``list``
			All of the names of individual Cython extensions, as a list of
			strings.

		Raises
		------
		* RuntimeError
			- The user specified an extension to be compiled whose source
			  file was not found.
		"""
		env_variable = "VICE_SETUP_EXTENSIONS"
		if env_variable in os.environ.keys():
			extensions = os.environ[env_variable].split(',')
			for ext in extensions:
				srcfilename = "%s.pyx" % (ext.replace('.', '/'))
				if not os.path.exists(srcfilename): raise RuntimeError("""\
Source file not found for extension: %s""" % (ext))
		else:
			extensions = []
			for root, dirs, files in os.walk(path):
				for f in files:
					if f.endswith(".pyx"):
						name = "%s.%s" % (root[2:].replace('/', '.'),
							f.split('.')[0])
						extensions.append(name)
					else: pass
		return extensions


	@staticmethod
	def get_c_srcfiles(name, path = "./vice"):
		r"""
		Find the paths to the C files required for the specified extension
		based on the mapping in vice/_build_utils/c_extensions.json.

		Parameters
		----------
		name : ``str``
			The name of the extension to compile.

		Returns
		-------
		ext : ``list``
			A list of the relative paths to all C extensions.

		Notes
		-----
		If the extension does not have an entry in the c_extensions.json file,
		VICE will compile it along with ALL C files in it's C library, omitting
		those under a directory named "tests" if "tests" is not in the name of
		the extension itself.
		"""
		extensions = []
		mapping = json.load(
			open("%s/_build_utils/c_extensions.json" % (path), 'r'))
		if name in mapping.keys():
			for item in mapping[name]:
				if os.path.exists(item) and item.endswith(".c"):
					extensions.append(item)
				elif os.path.isdir(item):
					for i in os.listdir(item):
						if i.endswith(".c"): extensions.append("%s/%s" % (
							item, i))
				else:
					raise SystemError("""Internal Error. Invalid C source code \
listing for extension %s: %s""" % (name, item))
		else:
			csrctree = "%s/src" % (path)
			for root, dirs, files in os.walk(csrctree):
				for i in files:
					if i.endswith(".c"):
						if "tests" in root and "tests" not in name:
							continue
						else:
							extensions.append(
								("%s/%s" % (root, i)).replace(os.getcwd(), '.')
							)
					else: pass
		return extensions


	@staticmethod
	def packages(path = "./vice"):
		r"""
		Finds each subpackage given the presence of an __init__.py file

		Parameters
		----------
		path : str [default : './vice']
			The path to the package directory

		Returns
		-------
		pkgs : list
			The names of all sub-packages, determined from the names of
			directories containing an __init__.py file.
		"""
		packages = []
		for root, dirs, files in os.walk(path):
			if "__init__.py" in files:
				packages.append(root[2:].replace('/', '.'))
			else:
				continue
		return packages


	@staticmethod
	def data(path = "./vice"):
		r"""
		Finds the data files to install based on a given extension

		Extensions
		----------
		.dat : files holding built-in data
		"""
		packages = discovery.packages(path = path)
		data = {}
		data_extensions = [".dat"]
		for i in packages:
			data[i] = []
			for j in os.listdir(i.replace('.', '/')):
				# look at each files extension
				for k in data_extensions:
					if j.endswith(k):
						data[i].append(j)
					else:
						continue
		return data


class openmp(Command):

	r"""
	A ``setuptools`` command that links VICE with the OpenMP library at compile
	time to enable parallel processing.
	"""

	_SUPPORTED_COMPILERS_ = {"gcc", "clang"}
	_CLANG_OPENMP_COMPILE_FLAGS_ = ["-Xpreprocessor", "-fopenmp"]
	_CLANG_OPENMP_LINK_FLAGS_ = ["-Xpreprocessor", "fopenmp", "-lomp"]
	_GCC_OPENMP_COMPILE_FLAGS_ = ["-fopenmp"]
	_GCC_OPENMP_LINK_FLAGS_ = ["-fopenmp"]

	@staticmethod
	def comiler_flags():
		r"""
		Determine the flags to pass to the C compiler for both compiling and
		linking. Returns the compiler and linker args, in that order, as lists
		of strings, which will be empty in the event that multithreading is not
		to be enabled.
		"""
		compile_args = []
		link_args = []
		if openmp.link_openmp():
			compiler = openmp.compiler()
			if compiler.startswith("clang"):
				compile_args.extend(openmp._CLANG_OPENMP_COMPILE_FLAGS_)
				link_args.extend(openmp._CLANG_OPENMP_LINK_FLAGS_)
			else:
				compile_args.extend(openmp._GCC_OPENMP_COMPILE_FLAGS_)
				link_args.extend(openmp._GCC_OPENMP_LINK_FLAGS_)
		else: pass
		return [compile_args, link_args]


	@staticmethod
	def compiler():
		r"""
		Determine the compiler to be used. Responds to a user specification
		through the environment variable ``CC`` and assumes the system default
		(i.e., clang for Mac OS, gcc for Linux) if no such environment variable
		is found. Returns the appropriate compile name as a string.
		"""
		if "CC" in os.environ.keys():
			check = openmp.check_compiler(os.environ["CC"])
			if check:
				return os.environ["CC"]
			elif check is None:
				raise RuntimeError("""\
Compiler from environment variable \"CC\" is not recognized: %s. \
Must be either gcc or clang.""" % (os.environ["CC"]))
			else:
				raise RuntimeError("""\
Unsupported compiler from environment variable \"CC\": %s. \
Must be either gcc or clang.""" % (os.environ["CC"]))
		else:
			# assume system default
			if sys.platform == "darwin":
				return "clang"
			else:
				return "gcc"

	@staticmethod
	def link_openmp():
		r"""
		Determine if the current installation is to be linked with OpenMP or
		not based on the presence and value of the environment variable
		``VICE_ENABLE_OPENMP``. Returns the corresponding boolean value.
		"""
		return ("VICE_ENABLE_OPENMP" in os.environ.keys() and
			os.environ["VICE_ENABLE_OPENMP"].lower() == "true")


	@staticmethod
	def check_compiler(compiler):
		r"""
		Determine which compiler was specified and whether or not it is
		supported.

		Parameters
		----------
		compiler : ``str``
			The compiler that the user has specified.

		Returns
		-------
		allowed : ``bool``
			``True`` if the compiler is supported and installation can proceed
			and ``False`` otherwise. If the specified compiler is recognized
			but not found on the user's system, or some error arises in trying
			to call on it with the ``which`` BASH command or with the
			``--version`` flag, then a value of ``None`` will be returned.
		"""
		assert isinstance(compiler, str), "Internal Error."
		allowed_compiler = False
		for test in openmp._SUPPORTED_COMPILERS_:
			# use startswith as opposed to == to catch, e.g., "gcc-10"
			allowed_compiler |= compiler.startswith(test)
		if not allowed_compiler: return False
		kwargs = {
			"stdout": PIPE,
			"stderr": PIPE,
			"shell": True,
			"text": True
		}

		# first check if the system even recognizes the compiler
		with Popen("which %s" % (compiler), **kwargs) as proc:
			out, err = proc.communicate()
			if sys.platform == "darwin":
				if out == "" and err == "": return None
			else:
				if "no %s" % (compiler) in err: return None

		# Now check that ``compiler --version`` runs properly and has either
		# "gcc" or "clang" along with a version number.
		def is_version_number(word):
			r"""
			Determine if a string could be interpreted as a version number of
			a stable release of a compiler by determining if it is composed of
			digits separated by decimals. Returns the corresponding boolean
			value.
			"""
			assert isinstance(word, str), "Internal Error."
			if '.' in word:
				_is_version_number = True
				for item in word.split('.'): _is_version_number &= item.isdigit()
				return _is_version_number
			else:
				return False

		with Popen("%s --version" % (compiler), **kwargs) as proc:
			out, err = proc.communicate()
			# should catch all typos that didn't already cause an error
			if err != "" and "command not found" in err: return None
			# should catch anything that isn't a command-line entry
			if err != "" and "illegal" in err: return None

			recognized = False
			has_version_number = False
			for word in out.split():
				for test in openmp._SUPPORTED_COMPILERS_:
					if word.startswith(test):
						compiler = word
						recognized = True
					else: pass
					has_version_number &= is_version_number(word)
			return recognized and has_version_number

	@staticmethod
	def find_openmp_clang():
		r"""
		Determine the path to the OpenMP library, header files, and linker
		file on Mac OS using Homebrew.

		Returns
		-------
		libomp_include_dir : ``str``
			The absolute path to the directory containing the omp.h header file.
		libomp_library_dir: ``str``
			The absolute path to the directory containing the libomp.dylib
			library for linking at compile time.

		Notes
		-----
		This function first runs ``brew`` to determine if Homebrew is installed.
		Users who have not done so will be directed accordingly. It then runs
		``brew list libomp`` to list the files associated with OpenMP, if any.
		If the necessary files are found, their directories are returned as
		strings. If the OpenMP files are not found, then the user is directed
		to run ``brew install libomp`` or ``brew reinstall libomp`` before
		reattempting their VICE installation.
		"""
		kwargs = {
			"stdout": PIPE,
			"stderr": PIPE,
			"shell": True,
			"text": True
		}

		with Popen("brew", **kwargs) as proc:
			out, err = proc.communicate()
			if err != "" and "command not found" in err: raise RuntimeError("""\
It appears that Homebrew is either not installed or not on your PATH. Please \
install Homebrew by following the instructions at https://brew.sh/ and then \
install OpenMP by running

$ brew install libomp

from your Unix command line before reattempting your VICE installation.""")

		with Popen("brew list libomp", **kwargs) as proc:
			msg = """\
Homebrew is installed, but the OpenMP header and library files were not found. \
To install OpenMP, please run

$ brew install libomp

from your Unix command line. If you have installed OpenMP, try reinstalling it \
by running

$ brew reinstall libomp

and then reattempt your VICE installation. If this does not solve your issue, \
then you may need to update to a newer version of Homebrew (see \
https://brew.sh/). If you continue to have trouble linking VICE with OpenMP, \
then please open an issue at https://github.com/giganano/VICE/issues."""

			out, err = proc.communicate()
			if err.startswith("Error:"):
				raise RuntimeError(msg)
			else:
				out = out.split("\n")
				if (any([_.endswith("omp.h") for _ in out]) and
					any([_.endswith("libomp.dylib") for _ in out])):
					# found header and library files
					idx = -1
					for i in range(len(out)):
						if out[i].endswith("omp.h"):
							idx = i
							break
						else: continue
					if idx == -1: raise RuntimeError(msg)
					libomp_include_dir = os.sep.join(
						out[idx].split(os.sep)[:-1])
					idx = -1
					for i in range(len(out)):
						if out[i].endswith("libomp.dylib"):
							idx = -1
							break
						else: continue
					if idx == -1: raise RuntimeError(msg)
					libomp_library_dir = os.sep.join(
						out[idx].split(os.sep)[:-1])
					return [libomp_include_dir, libomp_library_dir]
				else:
					return RuntimeError(msg)


if __name__ == "__main__": setup(
	ext_modules = discovery.build_extensions(),
	packages = discovery.packages(),
	package_data = discovery.data())

