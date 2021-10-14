# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = ["test", "test_progressbar"] 
from ..._globals import _VERSION_ERROR_ 
from ..._globals import _RECOGNIZED_IMFS_ 
from ...testing import moduletest 
from ...testing import unittest 
from .._cutils import progressbar 
from .utils import dummy1, dummy2, dummy3 
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
			test_progressbar(run = False)
		] 
	] 


@moduletest 
def test_progressbar(): 
	r""" 
	vice.core._cutils.progressbar module test 
	""" 
	return ["vice.core._cutils.progressbar", 
		[ 
			test_progressbar_initialize(), 
			test_progressbar_string(), 
			test_progressbar_maxval(), 
			test_progressbar_left_hand_side(), 
			test_progressbar_right_hand_side(), 
			test_progressbar_start(), 
			test_progressbar_finish(), 
			test_progressbar_update(), 
			test_progressbar_refresh() 
		] 
	] 


@unittest 
def test_progressbar_initialize(): 
	r""" 
	vice.core._cutils.progressbar.__init__ unit test 
	""" 
	def test(): 
		global _TEST_PBAR_ 
		_TEST_PBAR_ = None 
		try: 
			_TEST_PBAR_ = progressbar() 
		except: 
			return False 
		try: 
			_TEST_PBAR_._testing = True 
		except: pass 
		return isinstance(_TEST_PBAR_, progressbar) 
	return ["vice.core._cutils.progressbar.__init__", test] 


@unittest 
def test_progressbar_string(): 
	r""" 
	vice.core._cutils.progressbar.__str__ unit test 
	""" 
	def test(): 
		if not isinstance(_TEST_PBAR_, progressbar): return None 
		try: 
			str(_TEST_PBAR_) 
		except: 
			return False 
		status = True
		# Only compare to terminal size if this isn't GitHub actions
		# GitHub actions has a different ioctl than a Mac OS or Linux desktop,
		# so getting the window width the routine at vice/src/io/progressbar.c
		# doesn't work. Instead, when CI testing with GitHub actions that
		# routine simply assumes a window width of 100.
		if ("GITHUB_ACTIONS" in os.environ.keys() and
			os.environ["GITHUB_ACTIONS"] == "true"):
			status &= len(str(_TEST_PBAR_)) == 100
		else:
			status &= (
				# One space is left for the cursor at the end of the line.
				len(str(_TEST_PBAR_)) == os.get_terminal_size().columns - 1
			)
		status &= str(_TEST_PBAR_).startswith(_TEST_PBAR_.left_hand_side) 
		status &= str(_TEST_PBAR_).endswith(_TEST_PBAR_.right_hand_side) 
		return status 
	return ["vice.core._cutils.progresssbar.__str__", test] 


@unittest 
def test_progressbar_maxval(): 
	r""" 
	vice.core._cutils.progressbar.maxval unit test 
	""" 
	def test(): 
		if not isinstance(_TEST_PBAR_, progressbar): return None 
		status = True 
		try: 
			_TEST_PBAR_.maxval = 50 
		except: 
			return False 
		status &= _TEST_PBAR_.maxval == 50 
		try: 
			_TEST_PBAR_.maxval = 25 
		except: 
			return False 
		status &= _TEST_PBAR_.maxval == 25 
		try: 
			_TEST_PBAR_.maxval = 100 
		except: 
			return False 
		status &= _TEST_PBAR_.maxval == 100 
		return status 
	return ["vice.core._cutils.progressbar.maxval", test] 


@unittest 
def test_progressbar_left_hand_side(): 
	r""" 
	vice.core._cutils.progressbar.left_hand_side unit test 
	""" 
	def test(): 
		if not isinstance(_TEST_PBAR_, progressbar): return None 
		status = isinstance(_TEST_PBAR_.left_hand_side, strcomp) 
		try: 
			_TEST_PBAR_.left_hand_side = "foo" 
		except: 
			return False 
		status &= _TEST_PBAR_.left_hand_side == "foo" 
		status &= str(_TEST_PBAR_).startswith("foo") 
		try: 
			_TEST_PBAR_.left_hand_side = "bar" 
		except: 
			return False 
		status &= _TEST_PBAR_.left_hand_side == "bar" 
		status &= str(_TEST_PBAR_).startswith("bar") 
		try: 
			_TEST_PBAR_.left_hand_side = None 
		except: 
			return False 
		return status 
	return ["vice.core._cutils.progressbar.left_hand_side", test] 


@unittest 
def test_progressbar_right_hand_side(): 
	r""" 
	vice.core._cutils.progressbar.right_hand_side unit test 
	""" 
	def test(): 
		if not isinstance(_TEST_PBAR_, progressbar): return None 
		status = isinstance(_TEST_PBAR_.right_hand_side, strcomp) 
		try: 
			_TEST_PBAR_.right_hand_side = "foo" 
		except: 
			return False 
		status &= _TEST_PBAR_.right_hand_side == "foo" 
		status &= str(_TEST_PBAR_).endswith("foo") 
		try: 
			_TEST_PBAR_.right_hand_side = "bar" 
		except: 
			return False 
		status &= _TEST_PBAR_.right_hand_side == "bar" 
		status &= str(_TEST_PBAR_).endswith("bar") 
		try: 
			_TEST_PBAR_.right_hand_side = None 
		except: 
			return False 
		return status 
	return ["vice.core._cutils.progressbar.right_hand_side", test] 


@unittest 
def test_progressbar_start(): 
	r""" 
	vice.core._cutils.progressbar.start unit test 
	""" 
	def test(): 
		if not isinstance(_TEST_PBAR_, progressbar): return None 
		try: 
			_TEST_PBAR_.start() 
		except: 
			return False 
		status = _TEST_PBAR_.current == 0 
		status &= _TEST_PBAR_.left_hand_side.startswith("0") 
		status &= _TEST_PBAR_.right_hand_side == "ETA: 00h00m00s" 
		return status 
	return ["vice.core._cutils.progressbar.start", test] 


@unittest 
def test_progressbar_finish(): 
	r""" 
	vice.core._cutils.progressbar.finish unit test 
	""" 
	def test(): 
		if not isinstance(_TEST_PBAR_, progressbar): return None 
		try: 
			_TEST_PBAR_.finish() 
		except: 
			return False 
		status = _TEST_PBAR_.current == _TEST_PBAR_.maxval 
		status &= _TEST_PBAR_.left_hand_side == "%d of %d" % (
			_TEST_PBAR_.maxval, _TEST_PBAR_.maxval) 
		status &= _TEST_PBAR_.right_hand_side == "ETA: 00h00m00s" 
		return status 
	return ["vice.core._cutils.progressbar.finish", test] 


@unittest 
def test_progressbar_update(): 
	r""" 
	vice.core._cutils.progressbar.update unit test 
	""" 
	def test(): 
		if not isinstance(_TEST_PBAR_, progressbar): return None 
		try: 
			_TEST_PBAR_.start() 
		except: 
			return None 
		status = _TEST_PBAR_.current == 0 
		try: 
			_TEST_PBAR_.update(1) 
		except: 
			return False 
		status &= _TEST_PBAR_.current == 1 
		try: 
			_TEST_PBAR_.update(2) 
		except: 
			return False 
		status &= _TEST_PBAR_.current == 2 
		try: 
			_TEST_PBAR_.current = 3 
		except: 
			return False 
		status &= _TEST_PBAR_.current == 3 
		try: 
			_TEST_PBAR_.current = 4 
		except: 
			return False 
		status &= _TEST_PBAR_.current == 4 
		return status 
	return ["vice.core._cutils.progressbar.update", test] 


@unittest 
def test_progressbar_refresh(): 
	r""" 
	vice.core._cutils.progressbar.refresh unit test 
	""" 
	def test(): 
		if not isinstance(_TEST_PBAR_, progressbar): return None 
		try: 
			_TEST_PBAR_.refresh() 
		except: 
			return False 
		return True 
	return ["vice.core._cutils.progressbar.refresh", test] 


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

