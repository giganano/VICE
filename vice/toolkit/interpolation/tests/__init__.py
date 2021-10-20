
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from ....testing import moduletest
	from . import interp_scheme_1d
	from . import interp_scheme_2d

	@moduletest
	def test():
		r"""
		vice.toolkit.interpolation module test
		"""
		return ["vice.toolkit.interpolation",
			[
				interp_scheme_1d.test(run = False),
				interp_scheme_2d.test(run = False)
			]
		]

else: pass
