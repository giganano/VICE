
from __future__ import absolute_import
__all__ = ["test"]
from ...._globals import _VERSION_ERROR_
from ....testing import moduletest
from ....testing import unittest
from ....src.dataframe.tests.calclookback import calclookback_tracers
from ....src.dataframe.tests.calclogz import logzscaled_tracers
from ....src.dataframe.tests.calclogz import calclogz_tracers
from ....src.dataframe.tests.tracers import test_tracers_row
from ....src.dataframe.tests.calcz import zscaled_tracers
from ....src.dataframe.tests.calcz import calcz_tracers
from ....yields import agb
from ....yields import ccsne
from ....yields import sneia
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
			test_keys(),
			test_getitem(run = False)
		]
	]


@unittest
def test_initialize():
	r"""
	vice.core.dataframe.tracers.__init__ unit test
	"""
	from ...multizone import multizone
	def test():
		agb.settings.factory_settings()
		ccsne.settings.factory_settings()
		sneia.settings.factory_settings()
		mz = multizone(name = "test", n_zones = 3)
		for i in mz.zones:
			i.elements = _ELEMENTS_ + ["he"]
			i.dt = 0.05
		mz.run([0.05 * i for i in range(201)], overwrite = True)
		global _TEST_
		try:
			_TEST_ = tracers(filename = "test.vice/tracers.out",
				adopted_solar_z = 0.014)
		except:
			return False
		return isinstance(_TEST_, tracers)
	return ["vice.core.dataframe.tracers.__init__", test]


@moduletest
def test_getitem():
	r"""
	vice.core.dataframe.tracers.__getitem__ module test
	"""
	return ["vice.core.dataframe.tracers.__getitem__",
		[
			test_getitem_builtins(),
			calcz_tracers(),
			zscaled_tracers(),
			calclogz_tracers(),
			logzscaled_tracers(),
			calclookback_tracers(),
			test_tracers_row()
		]
	]

@unittest
def test_getitem_builtins():
	r"""
	vice.core.dataframe.stars.__getitem__.builtins unit test
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
		except:
			return False
		return True
	return ["vice.core.dataframe.tracers.__getitem__.builtins", test]


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

