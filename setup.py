r""" 
VICE setup.py file 

If building VICE from source, first run ``make`` in this directory before 
running this file. This file should then be ran with the following rule: 

python setup.py build [-j N] install [--user] [-q --quiet] [distutils] 
	[ext=ext1] [ext=ext2] [ext=ext3] [...] 

Install Options 
---------------
-j N        : Run build in parallel across N cores 
--user      : Install to ~/.local directory 
-q --quiet  : Run the installation non-verbosely 
distutils   : Run the installation with distutils rather than setuptools 
ext=        : Build and install specific extension 

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

try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 
import sys 
import os 
if "distutils" in sys.argv: 
	from distutils.core import setup, Extension 
	sys.argv.remove("distutils") 
else: 
	try: 
		from setuptools import setup, Extension 
	except (ImportError, ModuleNotFoundError): 
		from distutils.core import setup, Extension 
if sys.version_info[:2] < (3, 5): 
	raise RuntimeError("""This version of VICE requires python >= 3.5. \
Current version: %d.%d.%d.""" % (sys.version_info.major, 
		sys.version_info.minor, sys.version_info.micro)) 
else: pass  

# partial import 
import builtins 
builtins.__VICE_SETUP__ = True 
import vice 

_CYTHON_MINIMUM_ = "0.28.0" 
vice._check_cython(_CYTHON_MINIMUM_) 
import Cython
from Cython.Build import cythonize 

# ---------------------------- PACKAGE METADATA ---------------------------- # 
package_name = "vice" 
base_url = "http://github.com/giganano/VICE.git"
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
Programming Language :: Python :: 3.5 
Programming Language :: Python :: 3.6 
Programming Language :: Python :: 3.7 
Programming Language :: Python :: 3.8 
Programming Language :: Python :: 3 :: Only 
Programming Language :: Python :: Implementation :: CPython 
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Astronomy 
Topic :: Scientific/Engineering :: Physics
"""

# Version info 
MAJOR 			= 1 
MINOR 			= 5 
MICRO 			= 0 
BUILD 			= 0 
ISRELEASED		= False   
VERSION  		= "%d.%d.%d" % (MAJOR, MINOR, MICRO) 
if BUILD: VERSION += ".%d" % (BUILD) 



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
		A list of strings denoting the names of the extensions to install. 

	Raises 
	------
	* RuntimeError 
		- Invalid extension (file not found) 
	""" 
	specified = list(filter(lambda x: x.startswith("ext="), sys.argv)) 
	extensions = [] 
	if len(specified): 
		# The user has specified a specific extension 
		for i in specified: 
			ext = i.split('=')[1] 
			src = "./%s.pyx" % (ext.replace('.', '/')) 
			if os.path.exists(src): 
				src_files = [src] + vice.find_c_extensions(
					tests = "tests" in src
				)
				extensions.append(Extension(
					# The name of the extension 
					ext, 
					# Its associated file along w/VICE's C library 
					src_files, 
					extra_compile_args = ["-Wno-unreachable-code"] 
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
					src_files = ["%s/%s" % (root[2:], i)] 
					src_files += vice.find_c_extensions(tests = "tests" in root) 
					extensions.append(Extension( 
						# The name of the extension 
						"%s.%s" % (root[2:].replace('/', '.'), i.split('.')[0]), 
						# Its associated file along w/VICE's C library 
						src_files, 
						extra_compile_args = ["-Wno-unreachable-code"] 
					)) 
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
	.obj : a pickled object -> currently the only instance is the pickled 
		dictionary containing version info of build dependencies 
	.so : shared object 
	.o : compiled C code 
	.pdf : documentation 

	VICE's C extensions are compiled individually and wrapped into a 
	shared object using make. All of this output is moved to the install 
	directory to allow forward compatibility with future features that may 
	require it. 
	""" 
	packages = find_packages()
	data = {}
	data_extensions = [".dat", ".so", ".obj", ".o", ".pdf"]  
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
	cnt = """
# This file is generated from vice setup.py %(version)s

MAJOR = %(major)d 
MINOR = %(minor)d 
MICRO = %(micro)d 
BUILD = %(build)d 
RELEASED = %(isreleased)s
"""
	with open(filename, 'w') as f: 
		try:
			f.write(cnt % {
					"version": 		VERSION, 
					"major": 		MAJOR, 
					"minor": 		MINOR, 
					"micro": 		MICRO, 
					"build": 		BUILD, 
					"isreleased": 	str(ISRELEASED)
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

	# Keywords to the setup() call 
	metadata = dict(
		name = package_name, 
		version = VERSION, 
		author = "James W. Johnson", 
		author_email = "giganano9@gmail.com", 
		maintainer = "James W. Johnson", 
		maintainer_email = "giganano9@gmail.com", 
		url = base_url, 
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
		ext_modules = cythonize(find_extensions()), 
		python_requires=">=3.5.*, <4", 
		zip_safe = False, 
		verbose = "-q" not in sys.argv and "--quiet" not in sys.argv 
	)

	try: 
		write_version_info() 	# Write the version file 
		vice._write_build() 	# save version info for packaged used in build 
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

