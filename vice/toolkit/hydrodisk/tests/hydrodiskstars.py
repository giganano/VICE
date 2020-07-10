
from __future__ import absolute_import 
__all__ = ["test_linear", "test_sudden", "test_diffusion"] 
from .._hydrodiskstars import c_linear 
from .._hydrodiskstars import c_sudden 
from .._hydrodiskstars import c_diffusion 
from .._hydrodiskstars import _END_TIME_ 
from ....testing import moduletest 
from ....testing import unittest 
import sys 

_RAD_BINS_ = [0.25 * i for i in range(121)] 
_TEST_TIMES_ = [0.05 * i for i in range(257)] 


@moduletest 
def test_linear(): 
	r""" 
	vice.toolkit.hydrodisk.linear module test 
	""" 
	name = "vice.toolkit.hydrodisk.linear" 
	try: 
		_TEST_ = c_linear(_RAD_BINS_) 
	except: 
		return [name, None]
	return [name, 
		[ 
			test_hydrodata_import(_TEST_, "linear"), 
			test_call(_TEST_, "linear") 
		] 
	] 


@moduletest 
def test_sudden(): 
	r""" 
	vice.toolkit.hydrodisk.sudden module test 
	""" 
	name = "vice.toolkit.hydrodisk.sudden"
	try: 
		_TEST_ = c_sudden(_RAD_BINS_) 
	except: 
		return [name, None] 
	return ["vice.toolkit.hydrodisk.sudden", 
		[ 
			test_hydrodata_import(_TEST_, "sudden"), 
			test_call(_TEST_, "sudden") 
		] 
	] 


@moduletest 
def test_diffusion(): 
	r""" 
	vice.toolkit.hydrodisk.diffusion module test 
	""" 
	name = "vice.toolkit.hydrodisk.diffusion" 
	try: 
		_TEST_ = c_diffusion(_RAD_BINS_) 
	except: 
		return [name, None] 
	return [name, 
		[ 
			test_hydrodata_import(_TEST_, "diffusion"), 
			test_call(_TEST_, "diffusion") 
		] 
	] 


@unittest 
def test_hydrodata_import(obj, name): 
	r""" 
	The hydrodata import test function 

	Parameters 
	----------
	obj : c_hydrodiskstars 
		The hydrodiskstars object to test the import on 
	name : str 
		The name of the object within the API 
	""" 
	def test(): 
		try: 
			assert all([0 <= i <= _END_TIME_ for i in obj.analog_data["tform"]]) 
			assert all([0 <= i <= 30 for i in obj.analog_data["rform"]]) 
			assert all([0 <= i <= 30 for i in obj.analog_data["rfinal"]]) 
			assert all([isinstance(i, int) for i in obj.analog_data["id"]]) 
			assert all([i > 0 for i in obj.analog_data["id"]]) 
			assert all([isinstance(i, float) for i in obj.analog_data["zfinal"]]) 
			assert all([isinstance(i, float) for i in obj.analog_data["vrad"]]) 
			assert all([isinstance(i, float) for i in obj.analog_data["vphi"]]) 
			assert all([isinstance(i, float) for i in obj.analog_data["vz"]]) 
		except: 
			return False 
		return True 
	return ["vice.toolkit.hydrodisk.%s.import" % (name), test] 


@unittest 
def test_call(obj, name): 
	r""" 
	The hydrodisk object call tester 

	Parameters 
	----------
	obj : c_hydrodiskstars 
		The hydrodiskstars object to test the call on 
	name : str 
		The name of the object within the API 
	""" 
	def test(): 
		try: 
			status = True 
			for i in range(len(_RAD_BINS_) - 1): 
				for j in range(len(_TEST_TIMES_)): 
					x = obj(i, _TEST_TIMES_[j], _TEST_TIMES_[j]) 
					status &= isinstance(x, int) 
					status &= x == i 
					for k in range(j + 1, len(_TEST_TIMES_)): 
						x = obj(i, _TEST_TIMES_[j], _TEST_TIMES_[k]) 
						status &= isinstance(x, int) 
						status &= 0 <= x < len(_RAD_BINS_) or x == -1 
						if not status: break 
					if not status: break 
				if not status: break 
				sys.stdout.write("""\
\r\tvice.toolkit.hydrodisk.%s.call :: Progress: %.2f%%\
""" % (name, 100 * (i + 1) / (len(_RAD_BINS_) - 1))) 
			sys.stdout.write("""\
\r\tvice.toolkit.hydrodisk.%s.call ::                           """ % (name)) 
			sys.stdout.write("\r") 
		except: 
			return False 
		return True 
	return ["vice.toolkit.hydrodisk.%s.call" % (name), test] 

