
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from ....testing import moduletest
	from . import presets

	@moduletest
	def test():
		"""
		Run the tests on this module
		"""
		return ["vice.yields.presets",
			[
				presets.test_save(),
				presets.test_preset_import(),
				presets.test_remove()
			]
		]

else:
	pass

