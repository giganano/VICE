
from __future__ import absolute_import 
__all__ = ["test"] 
from ...._globals import _VERSION_ERROR_ 
from ....testing import moduletest 
from ....testing import unittest 
from ...dataframe._builtin_dataframes import solar_z 
from ...singlezone import singlezone 
from .._history import history 
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
	vice.core.dataframe.history module test 
	""" 
	return ["vice.core.dataframe.history", 
		[ 
			test_initialize(), 
			test_getitem(), 
			test_keys() 
		] 
	] 


@unittest 
def test_initialize(): 
	r""" 
	vice.core.dataframe.history.__init__ unit test 
	""" 
	def test(): 
		singlezone.singlezone(name = "test", 
			elements = _ELEMENTS_ + ["he"]).run(
			[0.01 * i for i in range(1001)], overwrite = True) 
		global _TEST_ 
		try: 
			_TEST_ = history(filename = "test.vice/history.out", 
				adopted_solar_z = 0.014) 
		except: 
			return False 
		return isinstance(_TEST_, history) 
	return ["vice.core.dataframe.history.__init__", test] 


@unittest 
def test_getitem(): 
	r""" 
	vice.core.dataframe.history.__getitem__ unit test 
	""" 
	def test(): 
		r""" 
		VICE writes each quantity to the output file with 7 significant 
		digits. Therefore, due to roundoff error, some quantities that 
		should be equal can actually be off by a difference of up to 1e-7. 
		This is will within a reasonable tolerance. 
		""" 
		try: 
			for i in ["time", "mgas", "mstar", "sfr", "ifr", "ofr", 
				"eta_0", "r_eff"]: 
				assert isinstance(_TEST_[i], list) 
				assert all(map(lambda x: isinstance(x, numbers.Number), 
					_TEST_[i])) 
				assert all(map(lambda x: x >= 0, _TEST_[i])) 
			for i in _ELEMENTS_: 
				assert isinstance(_TEST_["z_in(%s)" % (i)], list) 
				assert all(map(lambda x: isinstance(x, numbers.Number), 
					_TEST_["z_in(%s)" % (i)])) 
				assert all(map(lambda x: x == 0, _TEST_["z_in(%s)" % (i)])) 
				assert isinstance(_TEST_["z_out(%s)" % (i)], list) 
				assert all(map(lambda x: isinstance(x, numbers.Number), 
					_TEST_["z_out(%s)" % (i)])) 
				assert all(map(lambda x, y: abs(x - y) < 1e-7, 
					_TEST_["z_out(%s)" % (i)], _TEST_["z(%s)" % (i)])) 
				assert isinstance(_TEST_["mass(%s)" % (i)], list) 
				assert all(map(lambda x: isinstance(x, numbers.Number), 
					_TEST_["mass(%s)" % (i)])) 
				assert all(map(lambda x: x >= 0, _TEST_["mass(%s)" % (i)])) 
				assert isinstance(_TEST_["z(%s)" % (i)], list) 
				assert all(map(lambda x: isinstance(x, numbers.Number), 
					_TEST_["z(%s)" % (i)])) 
				assert all(map(lambda x, y, z: abs(x - y / z) < 1e-7, 
					_TEST_["z(%s)" % (i)], _TEST_["mass(%s)" % (i)], 
					_TEST_["mgas"] 
				))
				assert isinstance(_TEST_["[%s/h]" % (i)], list) 
				assert all(map(lambda x: isinstance(x, numbers.Number), 
					_TEST_["[%s/h]" % (i)])) 
				assert all(map(lambda x, y: 
					abs(x - m.log10(y / solar_z[i])) < 1e-7, 
					_TEST_["[%s/h]" % (i)][1:], _TEST_["z(%s)" % (i)][1:])) 
				for j in _ELEMENTS_: 
					assert isinstance(_TEST_["[%s/%s]" % (i, j)], list) 
					assert all(map(lambda x: isinstance(x, numbers.Number), 
						_TEST_["[%s/%s]" % (i, j)])) 
					assert all(map(lambda x, y, z: abs(x - (y - z)) < 1e-7, 
						_TEST_["[%s/%s]" % (i, j)][1:], 
						_TEST_["[%s/h]" % (i)][1:], 
						_TEST_["[%s/h]" % (j)][1:])) 
			assert isinstance(_TEST_["lookback"], list) 
			assert all(map(lambda x: isinstance(x, numbers.Number), 
				_TEST_["lookback"])) 
			assert all(map(lambda x, y: 
				abs(x - (max(_TEST_["time"]) - y)) < 1e-7, 
				_TEST_["lookback"], _TEST_["time"])) 
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
				_TEST_["[m/h]"][1:], _TEST_["z"][1:])) 
			assert isinstance(_TEST_["y"], list) 
			assert all(map(lambda x: isinstance(x, numbers.Number), 
				_TEST_["y"]))  
			assert all(map(lambda x, y: x == y, 
				_TEST_["y"], _TEST_["z(he)"])) 
		except: 
			return False 
		return True 
	return ["vice.core.dataframe.history.__getitem__", test] 


@unittest 
def test_keys(): 
	r""" 
	vice.core.dataframe.history.keys unit test 
	""" 
	def test(): 
		try: 
			assert isinstance(_TEST_.keys(), list) 
			assert all(map(lambda x: isinstance(x, strcomp), _TEST_.keys())) 
			[_TEST_.__getitem__(i) for i in _TEST_.keys()] 
		except: 
			return False 
		return True 
	return ["vice.core.dataframe.history.keys", test] 

