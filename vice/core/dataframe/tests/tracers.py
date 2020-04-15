
from __future__ import absolute_import 
__all__ = ["test"] 
from ...._globals import _VERSION_ERROR_ 
from ....testing import moduletest 
from ....testing import unittest 
from ...dataframe._builtin_dataframes import solar_z 
from .._tracers import tracers 
import math as m 
import numbers 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 

_ELEMENTS_ = ["fe", "sr", "o"] 

@moduletest 
def test(): 
	r""" 
	vice.core.dataframe.tracers unit test 
	""" 
	return ["vice.core.dataframe.tracers", 
		[ 
			test_initialize(), 
			test_getitem() 
		] 
	] 


@unittest 
def test_initialize(): 
	r""" 
	vice.core.dataframe.tracers.__init__ unit test 
	""" 
	from ...multizone import multizone 
	def test(): 
		mz = multizone(name = "test", n_zones = 3) 
		for i in mz.zones: 
			i.elements = _ELEMENTS_ + ["he"] 
			i.dt = 0.05 
		mz.run([0.01 * i for i in range(1001)], overwrite = True) 
		global _TEST_ 
		try: 
			_TEST_ = tracers(filename = "test.vice/tracers.out", 
				adopted_solar_z = 0.014) 
		except: 
			return False 
		return isinstance(_TEST_, tracers) 
	return ["vice.core.dataframe.tracers.__init__", test] 


@unittest 
def test_getitem(): 
	r""" 
	vice.core.dataframe.stars.__getitem__ unit test 
	""" 
	def test(): 
		r""" 
		VICE writes each quantity to the output file with 7 significant 
		digits. Therefore, due to roundoff error, some quantities that 
		should be equal can actually be off by a difference of up to 1e-7. 
		This is will within a reasonable tolerance. 
		""" 
		try: 
			for i in ["formation_time", "zone_origin", "zone_final", "mass"]: 
				assert isinstance(_TEST_[i], list) 
				assert all(map(lambda x: isinstance(x, numbers.Number), 
					_TEST_[i])) 
				assert all(map(lambda x: x >= 0, _TEST_[i])) 
			first_nonzero_idx = 0 
			while _TEST_["z(fe)"][first_nonzero_idx] == 0: 
				first_nonzero_idx += 1 
			for i in _ELEMENTS_: 
				assert isinstance(_TEST_["z(%s)" % (i)], list) 
				assert all(map(lambda x: isinstance(x, numbers.Number), 
					_TEST_["z(%s)" % (i)])) 
				assert all(map(lambda x: x >= 0, _TEST_["z(%s)" % (i)])) 
				assert isinstance(_TEST_["[%s/h]" % (i)], list) 
				assert all(map(lambda x: isinstance(x, numbers.Number), 
					_TEST_["[%s/h]" % (i)])) 
				assert all(map(lambda x, y: 
					abs(x - m.log10(y / solar_z[i])) < 1e-7, 
					_TEST_["[%s/h]" % (i)][first_nonzero_idx:], 
					_TEST_["z(%s)" % (i)][first_nonzero_idx:])) 
				for j in _ELEMENTS_: 
					assert isinstance(_TEST_["[%s/%s]" % (i, j)], list) 
					assert all(map(lambda x: isinstance(x, numbers.Number), 
						_TEST_["[%s/%s]" % (i, j)])) 
					assert all(map(lambda x, y, z: abs(x - (y - z)) < 1e-7, 
						_TEST_["[%s/%s]" % (i, j)][first_nonzero_idx:], 
						_TEST_["[%s/h]" % (i)][first_nonzero_idx:], 
						_TEST_["[%s/h]" % (j)][first_nonzero_idx:])) 
			assert isinstance(_TEST_["age"], list) 
			assert all(map(lambda x: isinstance(x, numbers.Number), 
				_TEST_["age"])) 
			assert all(map(lambda x, y: 
				abs(x - (max(_TEST_["formation_time"]) - y)) < 1e-7, 
				_TEST_["age"], _TEST_["formation_time"])) 
			assert isinstance(_TEST_["z"], list) 
			assert all(map(lambda x: isinstance(x, numbers.Number), 
				_TEST_["z"])) 
			for i in range(len(_TEST_["z"])): 
				assert abs(_TEST_["z"][i] - 0.014 * sum(
					[_TEST_["z(%s)" % (j)][i] for j in _ELEMENTS_]) / sum(
					[solar_z[j] for j in _ELEMENTS_])) < 1e-7 
			assert isinstance(_TEST_["[m/h]"], list) 
			assert all(map(lambda x: isinstance(x, numbers.Number), 
				_TEST_["[m/h]"])) 
			assert all(map(lambda x, y: abs(x - m.log10(y / 0.014)) < 1e-7, 
				_TEST_["[m/h]"][first_nonzero_idx:], 
				_TEST_["z"][first_nonzero_idx:])) 
			assert isinstance(_TEST_["y"], list) 
			assert all(map(lambda x: isinstance(x, numbers.Number), 
				_TEST_["y"]))  
			assert all(map(lambda x, y: x == y, 
				_TEST_["y"], _TEST_["z(he)"])) 
		except: 
			return False 
		return True 
	return ["vice.core.dataframe.tracers.__getitem__", test] 


@unittest 
def test_keys(): 
	r""" 
	vice.core.dataframe.tracers.keys unit test 
	""" 
	def test(): 
		try: 
			assert isinstance(_TEST_.keys(), list) 
			assert all(map(lambda x: isinstance(x, strcomp) , _TEST_.keys())) 
			[_TEST_.__getitem__(i) for i in _TEST_.keys()] 
		except: 
			return False 
		return True 
	return ["vice.core.dataframe.tracers.keys", test] 

