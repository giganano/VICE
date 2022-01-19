r"""
VICE setup.py file

If building VICE from source, first run ``make`` in this directory before
running this file, after which VICE can be installed with the conventional
``python setup.py install``.

This ``setup.py`` file offers the following command-line options in addition
to those provided by ``setuptools``:

- ``--ext`` : Compile the specified extension(s) only.
- ``--compiler`` : Specify which Unix C compiler to use.
- ``--openmp`` : Link with the openMP library to enable multithreading.

Run ``python setup.py --help`` for more information on the additional
command-line options provided by this file, and
``python setup.py --help-commands`` for more information on those provided
by ``setuptools``.

Individual extensions should be rebuilt and reinstalled only after the entire
body of VICE has been installed. This allows slight modifications to be
installed with ease.

After running this file, ``make clean`` will remove all of the Cython and
compiler outputs from the source tree.

Raises
------
* RuntimeError
	- The minimum version of Python is not satisfied (3.7.0)
	- The specified Unix C compiler is not 'gcc' or 'clang'
	- Invalid name for a specified extension to reinstall
* OSError
	- This file is being ran from within a Windows OS (POSIX is required)
"""

# this version requires python >= 3.7.0
MIN_PYTHON_VERSION = "3.7.0"
import argparse
import sys
import os
if sys.version_info[:] < tuple(
	[int(_) for _ in MIN_PYTHON_VERSION.split('.')]):
	raise RuntimeError("""This version of VICE requires python >= %s. \
Current version: %d.%d.%d.""" % (MIN_PYTHON_VERSION, sys.version_info.major,
	sys.version_info.minor, sys.version_info.micro))
try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext

# partial import
import builtins
builtins.__VICE_SETUP__ = True
import vice

# ---------------------------- PACKAGE METADATA ---------------------------- #
package_name = "vice"
repo_url = "https://github.com/giganano/VICE.git"
pypi_url = "https://pypi.org/project/vice/"
docs_url = "https://vice-astro.readthedocs.io/"
bugs_url = "https://github.com/giganano/VICE/issues"

CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Natural Language :: English
Operating System :: MacOS
Operating System :: POSIX
Operating System :: Unix
Programming Language :: C
Programming Language :: Cython
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Astronomy
Topic :: Scientific/Engineering :: Physics
"""

# Version info
# Note that only one of DEV, ALPHA, BETA, RC, and POST can be anything other
# than None, in which case it must be an ``int``.
# Changes to these numbers also require changes to ./docs/src/index.rst and
# ./docs/src/cover.tex
MAJOR			= 1
MINOR			= 4
MICRO			= 0
DEV				= 0
ALPHA			= None
BETA			= None
RC				= None
POST			= None
ISRELEASED		= False
VERSION			= "%d.%d.%d" % (MAJOR, MINOR, MICRO)
if DEV is not None:
	assert isinstance(DEV, int), "Invalid version information"
	VERSION += ".dev%d" % (DEV)
elif ALPHA is not None:
	assert isinstance(ALPHA, int), "Invalid version information"
	VERSION += "a%d" % (ALPHA)
elif BETA is not None:
	assert isinstance(BETA, int), "Invalid version information"
	VERSION += "b%d" % (BETA)
elif RC is not None:
	assert isinstance(RC, int), "Invalid version information"
	VERSION += "rc%d" % (RC)
elif POST is not None:
	assert isinstance(POST, int), "Invalid version information"
	VERSION += ".post%d" % (POST)
else: pass


def parse():
	r"""
	Parse the command-line arguments passed by the user that need to be
	processed before any calls to setup(...). This enables ``python setup.py
	--help`` to display only these command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description = """Command-line arguments accepted by this script in \
addition to those recognized by setuptools.""",
		epilog = """\
Run python setup.py --help-commands for additional setuptools options.""")
	parser.add_argument("--ext", action = "append", nargs = 1, type = str,
		help = "Individual extensions to compile and reinstall.")
	parser.add_argument("--compiler", type = str,
		help = """\
The Unix C compiler to use (either 'gcc' or 'clang'). Can also be specified \
via the environment variable 'CC'. Defaults to 'gcc' for Linux platforms and \
to 'clang' on Mac OS.""")
	parser.add_argument("--openmp", action = "store_true",
		help = """\
Link this installation to the openMP library to enable multithreading. \
Can also be accomplished by assigning the environment variable \
'VICE_ENABLE_OPENMP' a value of \"true\"""")

	# Leave the setuptools options out of this argparse and remove command
	# line arguments it won't recognize
	args, _ = parser.parse_known_args()
	sys.argv = list(filter(lambda x: not x.startswith("--ext"), sys.argv))
	sys.argv = list(filter(lambda x: not x.startswith("--compiler"), sys.argv))
	sys.argv = list(filter(lambda x: x != "--openmp", sys.argv))

	# Collect the specified extensions to compile as a list. If empty, this
	# script will compile all of them.
	extensions = []
	if args.ext is not None:
		for _ in args.ext: extensions.append(_[0])

	# Determine the compiler to use and set it as the environment variable 'CC'
	supported_compilers = set(["gcc", "clang"])
	if args.compiler is not None:
		if args.compiler in supported_compilers:
			os.environ["CC"] = args.compiler
		else:
			raise RuntimeError("""\
Unix C compiler must be either 'gcc' or 'clang'. Got: %s""" % (args.compiler))
	elif "CC" in os.environ.keys():
		if os.environ["CC"] not in supported_compilers:
			raise RuntimeError("""\
Unix C compiler must be either 'gcc' or 'clang'. Got %s from environment \
variable 'CC'.""" % (os.environ["CC"]))
	else:
		if sys.platform == "linux":
			os.environ["CC"] = "gcc"
		elif sys.platform == "darwin":
			os.environ["CC"] = "clang"
		else:
			raise OSError("""\
Sorry, Windows is not supported. Please install and use VICE within the \
Windows Subsystem for Linux.""")

	# For linking with openMP at compile time
	if args.openmp: os.environ["VICE_ENABLE_OPENMP"] = "true"
	return extensions


class build_ext(_build_ext):

	r"""
	Extends the ``build_ext`` base class provided by ``setuptools`` to
	determine compiler flags on a case-by-case basis.

	Although ``setuptools`` does not differentiate between Unix C compilers
	(gcc and clang), this difference is important for linking with the openMP
	library to enable multithreading. With gcc, simply passing the flag
	"-fopenmp" for compiling and linking sufficies. With clang, "-fopenmp"
	must be preceeded by "-Xpreprocessor" and when linking, the "-lomp" flag
	is also required.
	"""

	def build_extensions(self):

		compile_args = ["-fPIC", "-Wsign-conversion", "-Wsign-compare"]
		link_args = []

		if os.environ["VICE_ENABLE_OPENMP"] == "true":
			if os.environ["CC"] == "gcc":
				compile_args.append("-fopenmp")
				link_args.append("-fopenmp")
			else: # guaranteed to be clang by this point
				compile_args.append("-Xpreprocessor")
				compile_args.append("-fopenmp")
				link_args.append("-Xpreprocessor")
				link_args.append("-fopenmp")
				link_args.append("-lomp")
		else: pass

		for ext in self.extensions:
			for flag in compile_args: ext.extra_compile_args.append(flag)
			for flag in link_args: ext.extra_link_args.append(flag)

		_build_ext.build_extensions(self)


def find_extensions(specified, path = './vice'):
	r"""
	Finds each extension to install

	.. tip:: Install a specific with the ext=<name of extension> command-line
		argument at runtime.

	Parameters
	----------
	specified : list [elements of type ``str``]
		The specified extensions to compile. If this is an empty list, all of
		them will be compiled.
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
	extensions = []
	if len(specified):
		# The user has specified a specific extension(s)
		for ext in specified:
			src = "./%s.pyx" % (ext.replace('.', '/'))
			if os.path.exists(src):
				# The associated source files in the C library
				src_files = [src] + vice.find_c_extensions(ext)
				extensions.append(Extension(ext, src_files))
			else:
				raise RuntimeError("Source file for extension not found: %s" % (
					ext))
	else:
		# User hasn't specified any extensions -> install all of them
		for root, dirs, files in os.walk(path):
			for i in files:
				if i.endswith(".pyx"):
					# The name of the extension
					name = "%s.%s" % (root[2:].replace('/', '.'),
						i.split('.')[0])
					# The source files in the C library
					src_files = ["%s/%s" % (root[2:], i)]
					src_files += vice.find_c_extensions(name)
					extensions.append(Extension(name, src_files))
				else: continue
	return extensions


def find_packages(path = './vice'):
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


def find_package_data():
	r"""
	Finds the data files to install based on a given extension

	Extensions
	----------
	.dat : files holding built-in data
	"""
	packages = find_packages()
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


def write_version_info(filename = "./vice/version_breakdown.py"):
	r"""
	Writes the version info to disk within the source tree

	Parameters
	----------
	filename : str [default : "./vice/version_breakdown.py"]
		The file to write the version info to.

	.. note:: vice/version.py depends on the file produced by this function.
	"""
	cnt = """\
# This file is generated from vice setup.py %(version)s

MAJOR = %(major)d
MINOR = %(minor)d
MICRO = %(micro)d
DEV = %(dev)s
ALPHA = %(alpha)s
BETA = %(beta)s
RC = %(rc)s
POST = %(post)s
ISRELEASED = %(isreleased)s
MIN_PYTHON_VERSION = \"%(minversion)s\"
"""
	with open(filename, 'w') as f:
		try:
			f.write(cnt % {
					"version":		VERSION,
					"major":		MAJOR,
					"minor":		MINOR,
					"micro":		MICRO,
					"dev":			str(DEV),
					"alpha":		str(ALPHA),
					"beta":			str(BETA),
					"rc":			str(RC),
					"post":			str(POST),
					"isreleased":	str(ISRELEASED),
					"minversion":	MIN_PYTHON_VERSION
				})
		finally:
			f.close()


def set_path_variable(filename = "~/.bash_profile"):
	r"""
	Permanently adds ~/.local/bin/ to the user's $PATH for local
	installations (i.e. with [--user] directive).

	Parameters
	----------
	filename : str [default : "~/.bash_profile"]
		The filename to put the PATH modification in.
	"""
	if ("--user" in sys.argv and "%s/.local/bin" % (os.environ["HOME"]) not in
		os.environ["PATH"].split(':')):
		cnt = """\

# This line added by vice setup.py %(version)s
export PATH=$HOME/.local/bin:$PATH

"""
		cmd = "echo \'%s\' >> %s" % (cnt % {"version": VERSION}, filename)
		os.system(cmd)
	else:
		pass


def setup_package():
	r"""
	Build and install VICE.
	"""
	src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
	old_path = os.getcwd()
	os.chdir(src_path)
	sys.path.insert(0, src_path)

	# directories with .h header files, req'd by setup
	include_dirs = []
	for root, dirs, files in os.walk("./vice/src"):
		if "__pycache__" not in root: include_dirs.append(root)

	# Keywords to the setup() call
	metadata = dict(
		name = package_name,
		version = VERSION,
		author = "James W. Johnson",
		author_email = "giganano9@gmail.com",
		maintainer = "James W. Johnson",
		maintainer_email = "giganano9@gmail.com",
		url = repo_url,
		project_urls = {
			"Bug Tracker": bugs_url,
			"Documentation": docs_url,
			"Source Code": repo_url
		},
		description = "Galactic Chemical Evolution Integrator",
		long_description = vice._LONG_DESCRIPTION_,
		classifiers = CLASSIFIERS.split('\n'),
		license = "MIT",
		platforms = ["Linux", "Mac OS X", "Unix"],
		keywords = ["galaxies", "simulations", "abundances"],
		provides = [package_name],
		cmdclass = {"build_ext": build_ext},
		packages = find_packages(),
		package_data = find_package_data(),
		scripts = ["bin/%s" % (i) for i in os.listdir("./bin/")],
		ext_modules = find_extensions(parse()),
		include_dirs = include_dirs,
		setup_requires = [
			"setuptools>=18.0", # automatically handles Cython extensions
			"Cython>=0.29.0"
		],
		python_requires=">=3.7.*, <4",
		zip_safe = False,
		verbose = "-q" not in sys.argv and "--quiet" not in sys.argv
	)

	try:
		write_version_info() 	# Write the version file
		setup(**metadata)
		set_path_variable()
	finally:
		del sys.path[0]
		os.chdir(old_path)
	return


if __name__ == "__main__":
	setup_package()
	del builtins.__VICE_SETUP__

	# tell them if dill isn't installed if they're doing a source install
	try:
		import dill
	except (ImportError, ModuleNotFoundError):
		print("""\
===============================================================================
Package 'dill' not found. This package is required for encoding functional
attributes with VICE outputs. It is recommended that VICE users install this
package to make use of these features. This can be done via 'pip install dill'.
===============================================================================\
""")

