"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import sys
import os

def find_c_extensions(subdir, base):
	sub = "vice/%s/" % (subdir)
	contents = os.listdir(sub)
	ext = [base]
	for i in os.listdir(sub):
		if i.split('.')[-1] == "c" and i.split('.')[0] not in [
			"_data_management", "_wrapper", "_mpl"]:
			ext.append("%s%s" % (sub, i))
		else:
			continue
	return ext

def compile_extensions():
	setup(ext_modules = cythonize([Extension(
		"vice.core._data_management", 
		find_c_extensions("core", "vice/core/_data_management.pyx"))]))
	setup(ext_modules = cythonize([Extension(
		"vice.core._wrapper", 
		find_c_extensions("core", "vice/core/_wrapper.pyx")
	)]))
	setup(ext_modules = cythonize("./vice/core/_mpl.pyx"))
	setup(ext_modules = cythonize([Extension(
		"vice.data._ccsne_yields.yield_integrator", 
		find_c_extensions("data/_ccsne_yields", 
			"vice/data/_ccsne_yields/yield_integrator.pyx")
	)]))

def find_packages(path = '.'):
	packages = []
	for root, dirs, files in os.walk(path):
		if "__init__.py" in files:
			packages.append(root[2:].replace('/', '.'))
		else:
			continue
	return packages

def find_directories(packages):
	dirs = len(packages) * [None]
	for i in range(len(packages)):
		dirs[i] = packages[i].replace('.', '/')
	return dirs

def find_package_data(packdirs):
	data = {}
	for i in packdirs:
		if i == "vice/core":
			# Copy the enrichment.so shared object file for integrator class
			data["vice.core"] = ["enrichment.so"] 
		elif any(map(lambda x: x.split('.')[-1] == "dat", os.listdir(i))):
			data[i.replace('/', '.')] = ["*.dat"]
		else:
			continue
	return data

if __name__ == "__main__":

	# We do not support windows
	if os.name != "posix": 
		raise OSError("VICE does not support Windows.")
	else:
		pass

	# Install python extensions
	compile_extensions()
	packages = find_packages()
	packdirs = find_directories(packages)
	setup(
		name = "VICE", 
		version = "1.0.0", 
		description = "Single-Zone Galactic Chemical Evolution Integrator", 
		author = "James W. Johnson", 
		author_email = "giganano9@gmail.com", 
		packages = packages, 
		package_dir = dict(zip(packages, packdirs)), 
		package_data = find_package_data(packdirs)
	)

