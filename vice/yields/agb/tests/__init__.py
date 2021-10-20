
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from ....testing import moduletest
	from . import lookup
	from . import imports
	from . import interpolator

	@moduletest
	def test():
		"""
		Run the tests on this module
		"""
		return ["vice.yields.agb",
			[
				lookup.test(run = False),
				imports.test(run = False),
				interpolator.test()
			]
		]

else:
	pass

