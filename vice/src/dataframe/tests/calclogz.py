
from __future__ import absolute_import 
__all__ = [
	"calclogz_history", 
	"logzscaled_history" 
] 
from ....testing import unittest 
from ....core.outputs import history 
from ....core.dataframe._builtin_dataframes import solar_z 
import math as m 
import numbers 

r""" 
Notes 
-----
VICE writes each quantity to the output file with 7 significant digits, 
meaning quantities that should be equal may be off by 1e-7 due to 
roundoff error. 
""" 


@unittest 
def calclogz_history(): 
	r""" 
	vice.core.dataframe.history.__getitem__.calclogz unit test 
	""" 
	def test(): 
		r""" 
		This function will only be called after the test.vice singlezone 
		output has been produced by the module test which calls this. 
		""" 
		from ....core.dataframe.tests.history import _ELEMENTS_ 
		try: 
			_TEST_ = history("test") 
			for i in _ELEMENTS_: 
				assert isinstance(_TEST_["[%s/h]" % (i)], list) 
				assert all(map(lambda x: isinstance(x, numbers.Number), 
					_TEST_["[%s/h]" % (i)])) 
				assert all(map(lambda x, y: 
					abs(x - m.log10(y / solar_z[i])) <= 1.e-7, 
					_TEST_["[%s/h]" % (i)][1:], _TEST_["z(%s)" % (i)][1:])) 
				for j in _ELEMENTS_: 
					assert isinstance(_TEST_["[%s/%s]" % (i, j)], list) 
					assert all(map(lambda x: isinstance(x, numbers.Number), 
						_TEST_["[%s/%s]" % (i, j)])) 
					assert all(map(lambda x, y, z: abs(x - (y - z)) <= 1.e-7, 
						_TEST_["[%s/%s]" % (i, j)][1:], 
						_TEST_["[%s/h]" % (i)][1:], 
						_TEST_["[%s/h]" % (j)][1:])) 
		except: 
			return False 
		return True 
	return ["vice.core.dataframe.history.__getitem__.calclogz", test] 


@unittest 
def logzscaled_history(): 
	r""" 
	vice.core.dataframe.history.__getitem__.logzscaled unittest 
	""" 
	def test(): 
		r""" 
		This function will only be called after the test.vice singlezone 
		output has been produced by the module test which calls this. 
		""" 
		from ....core.dataframe.tests.history import _ELEMENTS_ 
		try: 
			_TEST_ = history("test") 
			assert isinstance(_TEST_["[m/h]"], list) 
			assert all(map(lambda x: isinstance(x, numbers.Number), 
				_TEST_["[m/h]"])) 
			assert all(map(lambda x, y: abs(x - m.log10(y / 0.014)) <= 1.e-7, 
				_TEST_["[m/h]"][1:], _TEST_["z"][1:])) 
		except: 
			return False 
		return True 
	return ["vice.core.dataframe.history.__getitem__.logzscaled", test] 

