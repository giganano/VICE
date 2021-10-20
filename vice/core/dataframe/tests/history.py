
from __future__ import absolute_import
__all__ = ["test"]
from ...._globals import _VERSION_ERROR_
from ....testing import moduletest
from ....testing import unittest
from ....src.dataframe.tests.calclookback import calclookback_history
from ....src.dataframe.tests.calclogz import logzscaled_history
from ....src.dataframe.tests.calclogz import calclogz_history
from ....src.dataframe.tests.history import test_history_row
from ....src.dataframe.tests.calcz import zscaled_history
from ....src.dataframe.tests.calcz import calcz_history
from ....yields import agb
from ....yields import ccsne
from ....yields import sneia
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
			test_keys(),
			test_getitem(run = False)
		]
	]


@unittest
def test_initialize():
	r"""
	vice.core.dataframe.history.__init__ unit test
	"""
	def test():
		agb.settings.factory_settings()
		ccsne.settings.factory_settings()
		sneia.settings.factory_settings()
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


@moduletest
def test_getitem():
	r"""
	vice.core.dataframe.history.__getitem__ module test
	"""
	return ["vice.core.dataframe.history.__getitem__",
		[
			test_getitem_builtins(),
			calcz_history(),
			zscaled_history(),
			calclogz_history(),
			logzscaled_history(),
			calclookback_history(),
			test_history_row()
		]
	]


@unittest
def test_getitem_builtins():
	r"""
	vice.core.dataframe.history.__getitem__.builtins unit test
	"""
	def test():
		r"""
		VICE writes each quantity to the output file with 6 significant
		digits. Therefore, due to roundoff error, some quantities that
		should be equal can actually be off by a difference of up to 1e-6.
		This is well within a reasonable tolerance.
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
				assert all(map(lambda x, y: abs(x - y) < 1e-6,
					_TEST_["z_out(%s)" % (i)], _TEST_["z(%s)" % (i)]))
				assert isinstance(_TEST_["mass(%s)" % (i)], list)
				assert all(map(lambda x: isinstance(x, numbers.Number),
					_TEST_["mass(%s)" % (i)]))
				assert all(map(lambda x: x >= 0, _TEST_["mass(%s)" % (i)]))
		except:
			return False
		return True
	return ["vice.core.dataframe.history.__getitem__.builtins", test]

