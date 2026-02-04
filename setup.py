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


if __name__ == "__main__": setup(
	ext_modules = discovery.build_extensions(),
	packages = discovery.packages(),
	package_data = discovery.data())

