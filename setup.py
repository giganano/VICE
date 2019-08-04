
try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 
from distutils.core import setup, Extension 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	import __builtin__ as builtins 
elif sys.version_info[:2] >= (3, 5): 
	import builtins 
else: 
	raise RuntimeError("VICE requires python version 2.7 or >= 3.5") 

# partial import 
builtins.__VICE_SETUP__ = True 
import vice 

_CYTHON_MINIMUM_ = "0.28.0" 
vice._check_cython(_CYTHON_MINIMUM_) 
import Cython
from Cython.Build import cythonize 

# ---------------------------- PACKAGE METADATA ---------------------------- # 
package_name = "VICE" 
base_url = "http://github.com/giganano/VICE"
CLASSIFIERS = """\
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
MINOR 			= 1 
MICRO 			= 0
ISRELEASED		= False  
VERSION 		= "%d.%d.%d" % (MAJOR, MINOR, MICRO)

def compile_extensions(): 
	# compile each Cython extension 
	c_extensions = list(filter(lambda x: x.endswith(".c"), 
		["vice/src/%s" % (i) for i in os.listdir("./vice/src/")])) 
	for root, dirs, files in os.walk('.'): 
		if "v0p0p0" not in root: 
			for i in files: 
				if i.endswith(".pyx"): 		# if it's cython code 
					ext = "%s.%s" % (root[2:].replace('/', '.'), 
						i.split('.')[0]) 
					files = ["%s/%s" % (root[2:], i)] + c_extensions 
					setup(ext_modules = cythonize([Extension(ext, files,
						extra_compile_args = ["-Wno-unreachable-code"])])) 
				else: 
					continue 
		else: 
			continue 

def find_packages(path = '.'):
	"""
	Finds each subpackage given the presence of an __init__.py file 
	
	path: 			The relative patch to the directory 
	"""
	packages = []
	for root, dirs, files in os.walk(path):
		if "__init__.py" in files:
			packages.append(root[2:].replace('/', '.'))
		else:
			continue
	return packages

def find_package_data(): 
	# Finds data files associated with each package 
	packages = find_packages()
	data = {}
	data_extensions = [".dat", ".so", ".obj", ".o"]  
	for i in packages: 
		""" 
		Extensions 
		========== 
		.dat :: files holding built-in data 
		.obj :: a pickled object -> currently the only instance is the pickled 
			dictionary containing version info of build dependencies 
		.so :: shared object 
		.o :: compiled C code 

		VICE's C extensions are compiled individually and wrapped into a 
		shared object using make. All of this output is moved to the install 
		directory to allow forward compatibility with future features that may 
		require it. 
		""" 
		data[i] = [] 
		for j in os.listdir(i.replace('.', '/')): 
			# look at each files extension 
			for k in data_extensions: 
				if j.endswith(k): 
					data[i].append(j) 
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
		cnt = """\

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
		scripts = ["bin/%s" % (i) for i in os.listdir("./bin/")]
	)

	try: 
		write_version_info() 	# Write the version file 
		vice._write_build() 	# save version info for packaged used in build 
		compile_extensions()	
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

