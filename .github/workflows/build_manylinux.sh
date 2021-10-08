#!/bin/sh -l

# This script builds a manylinux wheel within a docker image provided at
# quay.io from PyPA.

# The python executable for the proper version of python. The directory under
# /opt/python to take the executable from is taken as a command line argument.
python="/opt/python/$1/bin/python"

# Display environment variables 
echo "PATH: "$PATH
echo "COMPILER: " `which gcc` # linux distro's always built with gcc
echo "COMPILER VERSION: " `gcc --version`
echo "PYTHON: " $python
echo "PYTHON VERSION: " `$python --version`
echo "MAKE: " `which make`
echo "MAKE VERSION: " `make --version`

# Install build time dependencies
$python -m pip install --upgrade pip
$python -m pip install Cython>=0.29.21
$python -m pip install wheel>=0.33.0
$python -m pip install auditwheel

# Compile the code
make
$python setup.py bdist_wheel --quiet
make clean

# Repair the wheel. The output manylinux wheel will be under ./wheelhouse/.
auditwheel repair ./dist/*.whl

