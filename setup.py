r"""
VICE setup.py file

If building VICE from source, first run ``make`` in this directory before
installing VICE with the conventional command ``python setup.py install``.

In addition to the command-line utilities provided by ``setuptools``, this file
also provides

$ python setup.py [openmp] [extensions]

Users should invoke ``python setup.py install openmp`` when they want to link
VICE with the openMP library to enable multithreading. This can also be
achieved by setting the environment variable "VICE_ENABLE_OPENMP" to "true".

``python setup.py install extensions`` should be invoked only after running
``python setup.py install`` as this will re-compile only the specified
extensions. As such, this utility is most useful to users who are modifying
VICE's source code and therefore in practice, it is most often invoked
alongside ``python setup.py develop``. The same effect as
``python setup.py extensions`` can also be achieved by setting the environment
variable "VICE_SETUP_EXTENSIONS" to the same comma-separated list of extensions
to recompile.

For additional information, run ``python setup.py openmp --help`` and
``python setup.py extensions --help``. For information on the command-line
utilities provided by ``setuptools``, run ``python setup.py --help-commands``.

After running this file, ``make clean`` will remove all of the Cython and
compiler outputs from the source tree. Note however that this defeats the
purpose of ``python setup.py develop``, so if VICE is being installed in
developer's mode, ``make clean`` should only be ran after running
``python setup.py develop --uninstall``.

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
from subprocess import Popen, PIPE
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
from setuptools import setup, Extension, Command
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


class build_ext(_build_ext):

	r"""
	Extends the ``build_ext`` base class provided by ``setuptools`` to
	determine compiler flags on a case-by-case basis and filter the extensions
	to be (re-)compiled.

	Run 'python setup.py openmp --help' and 'python setup.py extensions --help'
	for more info.
	"""

	def build_extensions(self):

		# Determine compiler and linker flags, some of which are always
		# included and others of which are only included when linking to
		# openMP to enable multithreading.
		if sys.platform in ["linux", "darwin"]:
			compile_args = ["-fPIC", "-Wsign-conversion", "-Wsign-compare"]
		elif sys.platform == "win32":
			compile_args = ["/w34287", "/w44365", "/w44388", "/w24826",
				   "/w44389", "/w44245", "/w44365", "/w34018", "/w34267"]
		link_args = []
		if "VICE_ENABLE_OPENMP" in os.environ.keys():
			if os.environ["VICE_ENABLE_OPENMP"] == "true":
				if "CC" in os.environ.keys():
					# Some steps here duplicated because this environment
					# variable may be set without invoking ``setup.py openmp``.
					os.environ["CC"] = openmp.check_compiler(os.environ["CC"])
					# don't use == because it could be, e.g., gcc-10
					if os.environ["CC"].startswith("gcc"):
						compile_args.append("-fopenmp")
						link_args.append("-fopenmp")
					elif os.environ["CC"].startswith("clang"):
						compile_args.append("-Xpreprocessor")
						compile_args.append("-fopenmp")
						link_args.append("-Xpreprocessor")
						link_args.append("-fopenmp")
						link_args.append("-lomp")
					elif os.environ["CC"].startswith("cl"):
						# TODO openMP flags
						pass
					else:
						raise RuntimeError("""\
C compiler must be either 'gcc' or 'clang' on Unix or 'cl' on Windows. \
Got %s from environment variable 'CC'.""" % (os.environ["CC"]))
				else:
					# environment variable assigned but no CC, so
					# ``setup.py openmp`` definitely wasn't invoked -> assume
					# system default and expand compiler flags accordingly.
					if sys.platform == "linux":
						os.environ["CC"] = "gcc"
						compile_args.append("-fopenmp")
						link_args.append("-fopenmp")
					elif sys.platform == "darwin":
						os.environ["CC"] = "clang"
						compile_args.append("-Xpreprocessor")
						compile_args.append("-fopenmp")
						link_args.append("-Xpreprocessor")
						link_args.append("-fopenmp")
						link_args.append("-lomp")
					elif sys.platform == "win32":
						os.environ["CC"] = "cl"
						# TODO openMP flags flags
					else:
						raise OSError("Sorry, this operating system is not supported.")
			else: pass
		else: pass

		# Determine which extensions to rebuild -> all unless the user has
		# specified specific ones.
		if "VICE_SETUP_EXTENSIONS" in os.environ.keys():
			specified = os.environ["VICE_SETUP_EXTENSIONS"].split(',')
			self.extensions = list(filter(lambda x: x.name in specified,
				self.extensions))
		else: pass

		for ext in self.extensions:
			for flag in compile_args: ext.extra_compile_args.append(flag)
			for flag in link_args: ext.extra_link_args.append(flag)

		_build_ext.build_extensions(self)


	def run(self):
		# If the user has ran 'setup.py extensions' or 'setup.py openmp', those
		# commands needs to run *before* build_ext otherwise the necessary
		# environment variables will not be set and their specification(s) will
		# not be reflected.
		if "extensions" in sys.argv: self.run_command("extensions")
		if "openmp" in sys.argv: self.run_command("openmp")
		super().run()


class extensions(Command):

	r"""
	A ``setuptools`` command that allows the user to specify which extensions
	should be compiled.

	Run ``python setup.py extensions --help`` for more info.
	"""

	description = "Compile and (re-)install specific VICE extensions."

	user_options = [
		("ext=", "e", """\
The extension to rebuild. If multiple extensions should be compiled, they can \
be passed as a comma-separated list (no spaces!). The name of an extension can \
be determined by the relative path to a .pyx file by changing each separator \
to a '.' (e.g. vice/core/singlezone/_singlezone.pyx -> \
vice.core.singlezone._singlezone). The extension(s) to build can also be set \
by assigning the environment variable 'VICE_SETUP_EXTENSIONS' to the same \
value. In the event that this environment variable exists and 'setup.py \
extensions' is also ran, the value passed to 'setup.py extensions' will take \
precedent. Users may also override the environment variable \
'VICE_SETUP_EXTENSIONS' to build all of them with '--ext=all' or '-e all'.""")
	]

	def initialize_options(self):
		self.ext = None

	def finalize_options(self):
		# No error handling necessary as unrecognized extensions will have no
		# impact. This feature works by *filtering out* from the list of all
		# extensions determined by the ``find_extensions`` function.
		pass

	def run(self):
		if self.ext is not None:
			if self.ext != "all":
				os.environ["VICE_SETUP_EXTENSIONS"] = self.ext
			else:
				if "VICE_SETUP_EXTENSIONS" in os.environ.keys():
					del os.environ["VICE_SETUP_EXTENSIONS"]
				else: pass
		else: pass


class openmp(Command):

	r"""
	A ``setuptools`` command that sets the environment variable
	``VICE_ENABLE_OPENMP`` to "true", which is used by the sub-classed
	``build_ext`` object here to link VICE with the openMP library to enable
	multithreading.

	Run ``python setup.py openmp --help`` for more info.
	"""

	description = "Link VICE with the openMP library to enable multithreading."

	user_options = [
		("compiler=", "c", """\
The C Compiler to use. Must be either 'gcc' or 'clang' on Unix or 'cl' on \
Windows. If not specified, \
the environment variable "CC" will be used. If no such environment variable \
has been assigned, the system default will be used. Although setuptools does \
not differentiate between the three, the three require different compiler flags \
for linking with the openMP library. As with any other compilation process, \
the environment variable "CC" can be used to specify the C compiler even when \
not running 'setup.py openmp'.""")
	]

	supported_compilers = set(["gcc", "clang", "cl"])

	def initialize_options(self):
		self.compiler = None

	def finalize_options(self):
		if self.compiler is not None:
			if not openmp.check_compiler(self.compiler):
				raise RuntimeError("""\
C compiler must be either 'gcc' or 'clang' for Unix or 'cl' for Windows. \
Got: %s""" % (self.compiler))
		elif "CC" in os.environ.keys():
			if not openmp.check_compiler(os.environ["CC"]):
				raise RuntimeError("""\
C compiler must be either 'gcc' or 'clang' for Unix or 'cl' for Windows. \
Got %s from environment variable 'CC'.""" % (os.environ["CC"]))
		else: pass

	def run(self):
		os.environ["VICE_ENABLE_OPENMP"] = "true"
		if self.compiler is not None:
			os.environ["CC"] = self.check_compiler(self.compiler)
		elif "CC" in os.environ.keys():
			self.compiler = os.environ["CC"]
		else:
			if sys.platform == "linux":
				self.compiler = "gcc"
			elif sys.platform == "darwin":
				self.compiler = "clang"
			elif sys.platform == "win32":
				self.compiler = "cl"
			else:
				raise OSError("""\
Sorry, this operating system is not supported.""")
			os.environ["CC"] = self.compiler

	@staticmethod
	def check_compiler(compiler):
		r"""
		Determine if the specified compiler is supported and whether or not
		it corresponds to gcc or clang.

		Parameters
		----------
		compiler : ``str``
			The compiler that may or may not be supported.

		Returns
		-------
		The plain name of the compiler (i.e. "gcc" or "clang" as opposed to,
		e.g., "gcc-10" or "clang-11") if it is supported. ``None`` if the
		compiler is not found on the user's PATH, and ``False`` if it is
		outrightly not supported.

		Notes
		-----
		This test determines whether to compiler corresponds to a version of
		gcc or clang by using the `which` bash command and the `--version`
		flag the compiler should accept on the command-line, then looking for
		the strings "gcc" and "clang" in the output string. This allows a
		compiler invoked with a version number (e.g. gcc-10, clang-11) to work
		with this function.
		"""
		kwargs = {
			"stdout": PIPE,
			"stderr": PIPE,
			"shell": True,
			"text": True
		}

		# First check if the system if even recognizes the compiler
		if sys.platform in ["linux", "darwin"]:
			with Popen("which %s" % (compiler), **kwargs) as proc:
				out, err = proc.communicate()
				if sys.platform == "linux":
					# The error message printed on Linux `which`
					if "no %s" % (compiler) in err: return None
				elif sys.platform == "darwin":
					# On Mac OS, `which` prints nothing on error
					if out == "" and err == "": return None
		elif sys.platform == "win32":
			# The error message printed on Windows `where`
			with Popen("where %s" % (compiler), **kwargs) as proc:
				out, err = proc.communicate()
				if "INFO:" in err: return None
		else:
			raise OSError("Sorry, this operating system is not supported.")

		def is_version_number(word):
			r"""
			Looks for what could be a version number in a single string by
			determining if it is simply numbers separated by decimals.
			Returns ``True`` if the string could be interpreted as a version
			number and ``False`` otherwise.
			"""
			if '.' in word:
				_is_version_number = True
				for item in word.split('.'): _is_version_number &= item.isdigit()
				return _is_version_number
			else:
				return False

		# Then check if the command `$compiler --version` runs properly and
		# has either "gcc" or "clang" in the output along with a version number
		if sys.platform in ["linux", "darwin"]:
			_command = "%s --version" % compiler
		elif sys.platform == "win32":
			_command = compiler
		
		with Popen(_command, **kwargs) as proc:
			out, err = proc.communicate()
			# Should catch all typos
			if err != "" and "command not found" in err: return None
			# Should catch anything that isn't a compiler
			if err != "" and "illegal" in err: return False
			recognized = False
			contains_version_number = False
			for word in out.split():
				for test in openmp.supported_compilers:
					# startswith as opposed to == works with, e.g., gcc-10
					if word.startswith(test):
						compiler = word # catches gcc -> clang alias on Mac OS
						recognized = True
					else: pass
					contains_version_number |= is_version_number(word)
			if recognized and contains_version_number: return compiler
			return False


def find_extensions(path = './vice'):
	r"""
	Finds all of VICE's extensions. If the user is either running
	``setup.py extensions`` or has (equivalently) assigned the environment
	variable "VICE_SETUP_EXTENSIONS"", then this list will be filtered down
	later when ``setuptools`` runs the ``build_extensions`` function.

	Parameters
	----------
	path : str [default : './vice']
		The path to the package directory

	Returns
	-------
	exts : list
		A list of ``Extension`` objects to build.
	"""
	extensions = []
	for root, dirs, files in os.walk(os.path.normpath(path)):
		for i in files:
			if i.endswith(".pyx"):
				# The name of the extension
				name = "%s.%s" % (
					'.'.join(os.path.join(root, i).split(os.sep)[:-1]),
					i.split('.')[0]
				)
				# The source files in the C library
				src_files = [os.path.join(root, i)]
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
	for root, dirs, files in os.walk(os.path.normpath(path)):
		if "__init__.py" in files:
			packages.append(root.replace(os.sep, '.'))
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
		for j in os.listdir(i.replace('.', os.sep)):
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
	with open(os.path.normpath(filename), 'w') as f:
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
    TODO not sure about local installation on Windows.

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
	for root, dirs, files in os.walk(os.path.normpath("./vice/src")):
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
		cmdclass = {
			"build_ext": build_ext,
			"extensions": extensions,
			"openmp": openmp
		},
		packages = find_packages(),
		package_data = find_package_data(),
		scripts = [os.path.join("bin", i) for i in os.listdir("./bin/")],
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

