"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
"""

_MIN_CYTHON_MAJOR_ = 0
_MIN_CYTHON_MINOR_ = 25 
_MIN_CYTHON_MICRO_ = 2 

try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 
try: 
	import Cython 
	from Cython.Build import cythonize 
except (ImportError, ModuleNotFoundError): 
	message = "Please install Cython >= %d.%d.%d before installing VICE." % (
		_MIN_CYTHON_MAJOR_, _MIN_CYTHON_MINOR_, _MIN_CYTHON_MICRO_) 
	raise RuntimeError(message) 
if tuple([int(i) for i in Cython.__version__.split('.')]) < tuple([
	_MIN_CYTHON_MAJOR_, _MIN_CYTHON_MINOR_, _MIN_CYTHON_MICRO_]): 
	message = "Building VICE requires Cython >= %d.%d.%d. Current version: %s" % (
		_MIN_CYTHON_MAJOR_, _MIN_CYTHON_MINOR_, _MIN_CYTHON_MICRO_, 
		Cython.__version__)  
	raise RuntimeError(message) 
else:
	pass 

try:
	from setuptools import setup, Extension 
except: 
	from distutils.core import setup, Extension 
import sys
import os

if sys.version_info[0] < 3: 
	import __builtin__ as builtins
else:
	import builtins

if sys.version_info[:2] < (3, 5) and sys.version_info[:2] != (2, 7): 
	raise RuntimeError("VICE requires python version 2.7 or >= 3.5.")
else:
	pass

# We do not support windows
if os.name != "posix": 
	raise OSError("VICE does not support Windows.")
else:
	pass

package_name = "VICE" 
base_url = "http://github.com/giganano/VICE"

# partial import 
builtins.__VICE_SETUP__ = True
import vice 

CLASSIFIERS = """
Development Status :: 4 - Beta 
Intended Audience :: Developers 
Intended Audience :: Science/Research 
License :: OSI Approved :: MIT License 
Natural Language :: English 
Operating System :: POSIX 
Operating System :: Mac OS 
Operating System :: Mac OS :: Mac OS X 
Operating System :: Unix 
Programming Language :: C 
Programming Language :: Cython 
Programming Language :: Python 
Programming Language :: Python :: 2 
Programming Language :: Python :: 2.7 
Programming Language :: Python :: 3  
Programming Language :: Python :: 3.5 
Programming Language :: Python :: 3.6 
Programming Language :: Python :: 3.7 
Programming Language :: Python :: Implementation :: CPython 
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Astronomy 
Topic :: Scientific/Engineering :: Physics
"""

MAJOR 			= 1
MINOR 			= 0
MICRO 			= 0
ISRELEASED		= True
VERSION 		= "%d.%d.%d" % (MAJOR, MINOR, MICRO)

def compile_extensions(): # Compiles each Cython extension 
	# Each C extension lives in vice/src/ ---> find the *.c files 
	c_extensions = list(filter(lambda x: x[-2:] == ".c", 
		["vice/src/%s" % (i) for i in os.listdir("vice/src/")]))
	for root, dirs, files in os.walk('.'): 
		for i in files: 
			# If this is Cython code
			if i[-4:] == ".pyx": 
				# Produce the extension linked with the C extensions 
				ext = "%s.%s" % (root[2:].replace('/', '.'), i.split('.')[0])
				files = ["%s/%s" % (root[2:], i)] + c_extensions
				setup(ext_modules = cythonize([Extension(ext, files)]))
			else:
				continue

def find_packages(path = '.'):
	"""
	# Finds each subpackage given the presence of an __init__.py file 
	
	path: 			The relative patch to the directory 
	"""
	packages = []
	for root, dirs, files in os.walk(path):
		if "__init__.py" in files:
			packages.append(root[2:].replace('/', '.'))
		else:
			continue
	return packages

def find_package_data(): # Finds data files associated with each package 
	packages = find_packages()
	data = {}
	for i in packages: 
		"""
		C library stored in a shared object ---> moving .so files with data 
		ensures that it will be moved to the install directory as well. Build 
		data is stored in a .obj output file ---> moving that allows the 
		show_build() function to work properly. 
		"""
		if any(map(lambda x: x.split('.')[-1] in ["dat", "so", "obj"], 
			os.listdir(i.replace('.', '/')))): 
			data[i] = ["*.dat", "*.so", "*.obj"]
		else:
			continue
	return data

def write_version_info(filename = "vice/version.py"): 
	"""
	Writes the version info to filename
	"""
	cnt = """
# This file is generated from vice setup.py %(version)s

version = '%(version)s'
release = %(isreleased)s
"""
	with open(filename, 'w') as f: 
		try:
			f.write(cnt % {
					"version": 		VERSION, 
					"isreleased": 	str(ISRELEASED)
				})
		finally: 
			f.close()

def set_path_variable(filename = "~/.bash_profile"):
	"""
	Permanently adds ~/.local/bin/ to the user's $PATH if they are installing 
	via --user, allowing them to run vice from the command line without having 
	to set this environment variable themselves.
	"""
	if ("--user" in sys.argv and "%s/.local/bin" % (os.environ["HOME"]) not in 
		os.environ["PATH"].split(':')): 
		cnt = """

# This line added by vice setup.py %(version)s
export PATH=$PATH:$HOME/.local/bin

"""
		cmd = "echo \'%s\' >> %s" % (cnt % {"version": VERSION}, filename)
		os.system(cmd)
	else:
		pass

def setup_package(): 
	src_path = os.path.dirname(os.path.abspath(sys.argv[0])) 
	old_path = os.getcwd() 
	os.chdir(src_path)
	sys.path.insert(0, src_path)

	write_version_info()	# Write the version file 
	vice._write_build() 	# Save version info for packages used to build VICE 
	compile_extensions()	# Compile Cython extensions

	# Keywords to the setup() call 
	metadata = dict(
		name = package_name, 
		version = VERSION, 
		author = "James W. Johnson", 
		author_email = "giganano9@gmail.com", 
		maintainer = "James W. Johnson", 
		maintainer_email = "giganano9@gmail.com", 
		url = base_url, 
		description = "Single-Zone Galactic Chemical Evolution Integrator", 
		long_description = vice._LONG_DESCRIPTION_, 
		classifiers = CLASSIFIERS, 
		license = "MIT", 
		platforms = ["Linux", "Mac OS X", "Unix"], 
		keywords = ["galaxies", "simulations", "abundances"], 
		provides = [package_name], 
		packages = find_packages(), 
		package_data = find_package_data(), 
		install_requires = ["Cython>=%d.%d.%d" % (
			_MIN_CYTHON_MAJOR_, _MIN_CYTHON_MINOR_, _MIN_CYTHON_MICRO_)], 
		python_requires = ">=2.7, !=3.0.*, !=3.1.*, !=3.3.*, !=3.4.*, <4", 
		zip_safe = False, 
		scripts = ["bin/%s" % (i) for i in os.listdir("./bin/")]
	)

	try:
		setup(**metadata)
		set_path_variable()
	finally: 
		del sys.path[0]
		os.system("rm -f vice/version.py")
		os.chdir(old_path)
	return 

if __name__ == "__main__":
	setup_package()
	del builtins.__VICE_SETUP__

	# tell them if dill isn't installed 
	try: 
		import dill 
	except (ImportError, ModuleNotFoundError): 
		print("""\
================================================================================
Package 'dill' not found. This package is required for encoding functional 
attributes with VICE outputs. It is recommended that VICE users install this 
package to make use of these features. This can be done via 'pip install dill'. 
================================================================================\
""")

