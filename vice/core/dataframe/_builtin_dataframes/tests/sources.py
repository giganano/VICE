
from __future__ import absolute_import
__all__ = ["test_sources"]
from ....._globals import _RECOGNIZED_ELEMENTS_
from ....._globals import _VERSION_ERROR_
from .....testing import unittest
from ..sources import sources
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()


@unittest
def test_sources():
	"""
	Sources built-in dataframe unit test
	"""
	def test():
		"""
		Test the sources dataframe
		"""
		try:
			for i in _RECOGNIZED_ELEMENTS_:
				assert isinstance(sources[i], list)
				assert all(map(lambda x: isinstance(x, strcomp), sources[i]))
		except:
			return False
		return True
	return ["vice.core.dataframe._builtin_dataframes.sources", test]

