# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = ["test"]
from ..._globals import _VERSION_ERROR_
from ..._globals import _RECOGNIZED_IMFS_
from ...testing import moduletest
from ...testing import unittest
from .._cutils import progressbar
from .utils import dummy1, dummy2, dummy3
from .progressbar import test_progressbar
import random
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()

from .._cutils cimport callback_1arg_setup
from .._cutils cimport callback_2arg_setup
from .._cutils cimport callback_1arg
from .._cutils cimport callback_2arg
from .._cutils cimport setup_imf
from .._cutils cimport set_string
from .._cutils cimport ordinals
from .._cutils cimport copy_pylist
from .._cutils cimport copy_2Dpylist
from .._cutils cimport map_pyfunc_over_array
from ..objects._callback_1arg cimport CALLBACK_1ARG
from ..objects._callback_2arg cimport CALLBACK_2ARG
from ..objects._imf cimport IMF_
from libc.stdlib cimport malloc, free
from libc.string cimport strcmp
from . cimport _cutils


@moduletest
def test():
	r"""
	vice.core._cutils module test
	"""
	return ["vice.core._cutils",
		[
			test_callback_1arg_setup(),
			test_callback_2arg_setup(),
			test_setup_imf(),
			test_set_string(),
			test_ordinals(),
			test_copy_pylist(),
			test_copy_2Dpylist(),
			test_map_pyfunc_over_array(),
			test_progressbar()(run = False)
		]
	]


@unittest
def test_callback_1arg_setup():
	r"""
	vice.core._cutils.callback_1arg_setup unit test
	"""
	cdef CALLBACK_1ARG *cb
	def test():
		cb = _cutils.callback_1arg_initialize()
		try:
			callback_1arg_setup(cb, dummy1)
		except:
			_cutils.callback_1arg_free(cb)
			return False
		status = True
		for i in range(100):
			status &= callback_1arg(<double> i, cb[0].user_func) == <double> i
		try:
			callback_1arg_setup(cb, 1)
		except:
			_cutils.callback_1arg_free(cb)
			return False
		status &= cb[0].user_func is NULL
		status &= cb[0].assumed_constant == 1
		_cutils.callback_1arg_free(cb)
		return status
	return ["vice.core._cutils.callback_1arg_setup", test]


@unittest
def test_callback_2arg_setup():
	r"""
	vice.core._cutils.callback_2arg_setup unit test
	"""
	cdef CALLBACK_2ARG *cb
	def test():
		cb = _cutils.callback_2arg_initialize()
		try:
			callback_2arg_setup(cb, dummy2)
		except:
			_cutils.callback_2arg_free(cb)
			return False
		status = True
		for i in range(100):
			for j in range(100):
				status &= (
					callback_2arg(<double> i, <double> j, cb[0].user_func) ==
					<double> (i * j)
				)
		try:
			callback_2arg_setup(cb, 1)
		except:
			_cutils.callback_2arg_free(cb)
			return False
		status &= cb[0].user_func is NULL
		status &= cb[0].assumed_constant == 1
		_cutils.callback_2arg_free(cb)
		return status
	return ["vice.core._cutils.callback_2arg_setup", test]


@unittest
def test_setup_imf():
	r"""
	vice.core._cutils.setup_imf unit test
	"""
	cdef IMF_ *imf
	def test():
		imf = _cutils.imf_initialize(0.08, 100)
		status = True
		for i in _RECOGNIZED_IMFS_:
			try:
				setup_imf(imf, i)
			except:
				_cutils.imf_free(imf)
				return False
			status &= not strcmp(imf[0].spec, i.encode())
		try:
			setup_imf(imf, dummy1)
		except:
			_cutils.imf_free(imf)
			return False
		status &= not strcmp(imf[0].spec, "custom".encode())
		_cutils.imf_free(imf)
		return status
	return ["vice.core._cutils.setup_imf", test]


@unittest
def test_set_string():
	r"""
	vice.core._cutils.set_string unit test
	"""
	cdef char *cstring
	def test():
		pystr = "This is a test string."
		cstring = <char *> malloc ((len(pystr) + 1) * sizeof(char))
		try:
			set_string(cstring, pystr)
		except:
			free(cstring)
			return False
		status = not strcmp(cstring, pystr.encode())
		free(cstring)
		return status
	return ["vice.core._cutils.set_string", test]


@unittest
def test_ordinals():
	r"""
	vice.core._cutils.ordinals unit test
	"""
	cdef int *ords
	def test():
		pystr = "This is a test string."
		try:
			ords = ordinals(pystr)
		except:
			return False
		if ords is not NULL:
			status = True
			for i in range(len(pystr)):
				status &= ords[i] == ord(pystr[i])
			free(ords)
			return status
		else:
			return False
	return ["vice.core._cutils.ordinals", test]


@unittest
def test_copy_pylist():
	r"""
	vice.core._cutils.copy_pylist unit test
	"""
	cdef double *copy
	def test():
		test_ = 1000 * [0.]
		for i in range(len(test_)):
			test_[i] = random.random()
		try:
			copy = copy_pylist(test_)
		except:
			return False
		if copy is not NULL:
			status = True
			for i in range(len(test_)):
				status &= copy[i] == test_[i]
			free(copy)
			return status
		else:
			return False
	return ["vice.core._cutils.copy_pylist", test]


@unittest
def test_copy_2Dpylist():
	r"""
	vice.core._cutils.copy_2Dpylist unit test
	"""
	cdef double **copy
	def test():
		test_ = 1000 * [None]
		for i in range(len(test_)):
			test_[i] = 1000 * [0.]
			for j in range(len(test_[i])):
				test_[i][j] = random.random()
		try:
			copy = copy_2Dpylist(test_)
		except:
			return False
		if copy is not NULL:
			status = True
			for i in range(len(test_)):
				for j in range(len(test_[i])):
					status &= copy[i][j] == test_[i][j]
			free(copy)
			return status
		else:
			return False
	return ["vice.core._cutils.copy_2Dpylist", test]


@unittest
def test_map_pyfunc_over_array():
	r"""
	vice.core._cutils.copy_2Dpylist unit test
	"""
	cdef double *mapped
	def test():
		n = 100
		try:
			mapped = map_pyfunc_over_array(dummy3, list(range(n)))
		except:
			return False
		if mapped is not NULL:
			status = True
			for i in range(n):
				status &= mapped[i] == dummy3(i)
			free(mapped)
			return status
		else:
			return False
	return ["vice.core._cutils.map_pyfunc_over_array", test]

