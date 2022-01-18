r"""
VICE setup.py file

If building VICE from source, first run ``make`` in this directory before
running this file. This file should then be ran with the following rule:

python setup.py build [-j N] install [--user] [-q --quiet] [distutils]
	[ext=ext1] [ext=ext2] [ext=ext3] [...]

Install Options
---------------
-j N             : Run build in parallel across N cores
--user           : Install to ~/.local directory
-q --quiet       : Run the installation non-verbosely
ext=             : Build and install specific extension
--enbable-openmp : Link VICE's compiled outputs to the openMP library to enable
                   multithreaded calculations. Alternatively, this can be
                   achieved by setting the environment variable
                   ``VICE_ENABLE_OPENMP`` to "true".

Individual extensions should be rebuilt and reinstalled only after the entire
body of VICE has been installed. This allows slight modifications to be
installed with ease.

After running this file, ``make clean`` will remove all of the Cython and
compiler outputs from the source tree.

Raises
------
* RuntimeError
	- The name of the extension to reinstall is invalid
"""

# this version requires python >= 3.7.0
MIN_PYTHON_VERSION = "3.7.0"
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

# Determine if we need to link to the openMP library
if "--enable-openmp" in sys.argv or ("VICE_ENABLE_OPENMP" in os.environ.keys()
	and os.environ["VICE_ENABLE_OPENMP"] == "true"):
	ENABLE_OPENMP = True
	if "--enable-openmp" in sys.argv: sys.argv.remove("--enable-openmp")
else:
	ENABLE_OPENMP = False

# Determine if we'll be using gcc or clang
_SUPPORTED_COMPILERS_ = set(["gcc", "clang"])
_CC_ = list(filter(lambda x: x.startswith("CC="), sys.argv))
if len(_CC_): # they specified one on the command line
	if len(_CC_) == 1:
		_CC_ = _CC_.split('=')[-1]
	else:
		raise RuntimeError("Got multiple values for C compiler.")
else: # they did not specify one on the command line
	if "CC" in os.environ.keys(): # check for environment variable spec
		_CC_ = os.environ["CC"]
	else:
		# no command-line or environment variable spec, use platform default
		if sys.platform == "linux":
			_CC_ = "gcc"
		elif sys.platform == "darwin":
			_CC_ = "clang"
		else:
			raise OSError("""\
Sorry, Windows is not supported. Please install and use VICE within the \
Windows Subsystem for Linux.""")
if _CC_ in _SUPPORTED_COMPILERS_:
	os.environ["CC"] = _CC_
else:
	raise RuntimeError("Sorry, only gcc and clang are supported. Got: %s" % (
		_CC_))

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


def find_extensions(path = './vice'):
	r"""
	Finds each extension to install

	.. tip:: Install a specific with the ext=<name of extension> command-line
		argument at runtime.

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
	specified = list(filter(lambda x: x.startswith("ext="), sys.argv))
	extensions = []
	if len(specified):
		# The user has specified a specific extension(s)
		for i in specified:
			ext = i.split('=')[1] # The name of the extension
			src = "./%s.pyx" % (ext.replace('.', '/'))
			if os.path.exists(src):
				# The associated source files in the C library
				src_files = [src] + vice.find_c_extensions(ext)
				extensions.append(Extension(ext, src_files,
					extra_compile_args = compiler_flags(which = "compile"),
					extra_link_args = compiler_flags(which = "link")
				))
				sys.argv.remove(i) # get rid of this for setup install
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
					extensions.append(Extension(name, src_files,
						extra_compile_args = compiler_flags(which = "compile"),
						extra_link_args = compiler_flags(which = "link")
					))
				else: continue
	return extensions


def compiler_flags(which = "compile"):
	r"""
	Determine the list of compiler flags for Cython to pass to the compiler at
	either compile or link time.

	Parameters
	----------
	which : ``str``
		Either "compile" or "link", depending on which action is being
		taken by the compiler.

	Returns
	-------
	flags : ``list``
		A list of flags to pass to the C compiler

	Notes
	-----
	Regardless of whether or not openMP is being linked, VICE will always
	compile with "-fPIC -Wsign-conversion -Wsign-compare" flags.

	When using the ``gcc`` compiler and linking with openMP, the script
	compiles and links using the "-fopenmp" flag. When using the ``clang``
	compiler and link with openMP, it compiles using "-Xpreprocessor -fopenmp"
	and links using "-Xpreprocessor -fopenmp -lomp".
	"""
	if which == "compile":
		flags = ["-fPIC", "-Wsign-conversion", "-Wsign-compare"]
	elif which == "link":
		flags = []
	else:
		raise RuntimeError("Invalid value for which': %s" % (which))

	if ENABLE_OPENMP:
		if _CC_ == "gcc":
			flags.append("-fopenmp")
		else: #clang
			flags.append("-Xpreprocessor")
			flags.append("-fopenmp")
			if which == "link": flags.append("-lomp")
	else: pass
	return flags


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
		packages = find_packages(),
		package_data = find_package_data(),
		scripts = ["bin/%s" % (i) for i in os.listdir("./bin/")],
		ext_modules = find_extensions(),
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

