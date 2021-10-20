
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from .....testing import moduletest
	from .atomic_number import test_atomic_number
	from .primordial import test_primordial
	from .solar_z import test_solar_z
	from .sources import test_sources
	from .stable_isotopes import test_stable_isotopes

	@moduletest
	def test():
		"""
		Run the tests on this module
		"""
		return ["vice.core.dataframe._builtin_dataframes.tests",
			[
				test_atomic_number(),
				test_primordial(),
				test_solar_z(),
				test_sources(),
				test_stable_isotopes()
			]
		]

else:
	pass

