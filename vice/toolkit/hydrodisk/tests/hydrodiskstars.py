
from __future__ import absolute_import 
__all__ = ["test"] 
from ..hydrodiskstars import hydrodiskstars 
from .._hydrodiskstars import _END_TIME_ 
from ....testing import moduletest 
from ....testing import unittest 
import sys 

_RAD_BINS_ = [0.25 * i for i in range(81)] 
_TEST_TIMES_ = [0.05 * i for i in range(245)] 


@moduletest 
def test(): 
	r""" 
	The hydrodiskstars object module test 
	""" 
	return ["vice.toolkit.hydrodisk.hydrodiskstars", 
		[ 
			test_initialize(), 
			test_import(), 
			test_radial_bins_setter(), 
			test_call("linear"), 
			test_call("sudden"), 
			test_call("diffusion") 
		] 
	] 


@unittest 
def test_initialize(): 
	r""" 
	The initialization unit test 
	""" 
	def test(): 
		global _TEST_ 
		try: 
			_TEST_ = hydrodiskstars(_RAD_BINS_) 
		except: 
			return False 
		return isinstance(_TEST_, hydrodiskstars) 
	return ["vice.toolkit.hydrodisk.hydrodiskstars.init", test] 


@unittest 
def test_import(): 
	r""" 
	The hydrodata import test function 
	""" 
	def test(): 
		try: 
			# _END_TIME_ = 13.2, and max tform is 13.23xyz... so the +0.04 
			# merely accounts for the trailing digits on the max tform. 
			assert all([0 <= i <= _END_TIME_ + 0.04 for i in 
				_TEST_.analog_data["tform"]]) 
			assert all([0 <= i <= 20 for i in _TEST_.analog_data["rform"]]) 
			assert all([0 <= i <= 20 for i in _TEST_.analog_data["rfinal"]]) 
			assert all([isinstance(i, int) for i in _TEST_.analog_data["id"]]) 
			assert all([i > 0 for i in _TEST_.analog_data["id"]]) 
			assert all([isinstance(i, float)] for i in 
				_TEST_.analog_data["zform"]) 
			assert all([-3 <= i <= 3 for i in _TEST_.analog_data["zform"]]) 
			assert all([isinstance(i, float) for i in 
				_TEST_.analog_data["zfinal"]]) 
			assert all([isinstance(i, float) for i in 
				_TEST_.analog_data["vrad"]]) 
			assert all([isinstance(i, float) for i in 
				_TEST_.analog_data["vphi"]]) 
			assert all([isinstance(i, float) for i in 
				_TEST_.analog_data["vz"]]) 
			assert all([isinstance(_, int) for _ in 
				_TEST_.analog_data["decomp"]]) 
			assert all([_ in [1, 2, 3, 4] for _ in _TEST_.analog_data["decomp"]]) 
		except: 
			return False 
		return True 
	return ["vice.toolkit.hydrodisk.hydrodiskstars.import", test] 


@unittest 
def test_radial_bins_setter(): 
	r""" 
	The radial_bins.setter unit test 
	""" 
	def test(): 
		try: 
			test1 = [0.5 * i for i in range(61)] 
			_TEST_.radial_bins = test1 
			assert _TEST_.radial_bins == test1 
			test2 = list(range(31)) 
			_TEST_.radial_bins = test2 
			assert _TEST_.radial_bins == test2 
			_TEST_.radial_bins = _RAD_BINS_ 
			assert _TEST_.radial_bins == _RAD_BINS_ 
		except: 
			return False 
		return True 
	return ["vice.toolkit.hydrodisk.hydrodiskstars.radial_bins.setter", test] 


@unittest 
def test_call(mode): 
	r""" 
	The hydrodisk object call tester 

	Parameters 
	----------
	mode : str 
		The mode under which to test the hydrodiskstars object under 
	""" 
	msg = "vice.toolkit.hydrodisk.hydrodiskstars.call [%s]" % (mode) 
	def test(): 
		try: 
			_TEST_.mode = mode 
		except: 
			return None 
		try: 
			status = True 
			for i in range(len(_RAD_BINS_) - 1): 
				for j in range(len(_TEST_TIMES_)): 
					x = _TEST_(i, _TEST_TIMES_[j], _TEST_TIMES_[j]) 
					status &= isinstance(x, int) 
					status &= x == i 
					for k in range(j + 1, len(_TEST_TIMES_)): 
						x = _TEST_(i, _TEST_TIMES_[j], _TEST_TIMES_[k]) 
						status &= isinstance(x, int) 
						status &= 0 <= x < len(_RAD_BINS_) 
						if not status: 
							print('a') 
							break 
					if not status: 
						print('b') 
						break 
				if not status: 
					print('c') 
					break 
				sys.stdout.write("\r\t%s :: Progress: %.2f%%" % (msg, 
					100 * (i + 1) / (len(_RAD_BINS_) - 1))) 
			sys.stdout.write("\r\t%s ::                      " % (msg)) 
			sys.stdout.write("\r") 
		except: 
			return False 
		return True 
	return [msg, test] 

