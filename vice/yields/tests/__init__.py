
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from ...testing import moduletest
	from . import _integral as integral
	from . import functional_yields

	@moduletest
	def test():
		"""
		Run the tests on this module
		"""
		return ["vice.src.yields",
			[
				integral.test(run = False),
				functional_yields.equivalence_test()
			]
		]

else:
	pass

