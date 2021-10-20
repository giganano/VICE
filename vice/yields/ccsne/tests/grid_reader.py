
from __future__ import absolute_import
__all__ = ["test_table"]
from ....core.dataframe._ccsn_yield_table import ccsn_yield_table
from ...._globals import _RECOGNIZED_ELEMENTS_
from ....testing import unittest
from .._errors import _RECOGNIZED_STUDIES_
from .._errors import _MOVERH_
from .._errors import _ROTATION_
from ..grid_reader import table


@unittest
def test_table():
	"""
	vice.yields.ccsne.table unit test
	"""
	def test():
		"""
		Test the table function at vice/yields/ccsne/grid_reader.py
		"""
		try:
			for i in _RECOGNIZED_ELEMENTS_:
				for j in _RECOGNIZED_STUDIES_:
					for k in _MOVERH_[j]:
						for l in _ROTATION_[j]:
							params = dict(
								study = j,
								MoverH = k,
								rotation = l
							)
							"""
							If a LookupError is raised, ensure that its due to
							the current study not reporting yields for the
							specified element.
							"""
							try:
								assert isinstance(table(i, isotopic = True,
									**params), ccsn_yield_table)
							except LookupError as exc:
								if i not in exc.args[0]:
									return False
								else:
									pass
							try:
								assert isinstance(table(i, isotopic = False,
									**params), ccsn_yield_table)
							except LookupError as exc:
								if i not in exc.args[0]:
									return False
								else:
									pass
			return True
		except:
			return False
	return ["vice.yields.ccsne.table", test]

