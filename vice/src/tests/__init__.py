
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False


if not __VICE_SETUP__:

	__all__ = [
		"callback",
		"imf",
		"stats",
		"test",
		"utils"
	]
	from ...testing import moduletest
	from . import _callback as callback
	from . import _imf as imf
	from . import _stats as stats
	from . import _utils as utils

	@moduletest
	def test():
		r"""
		vice.src.tests module test
		"""
		return ["vice.src.tests",
			[
				callback.test(run = False),
				imf.test(run = False),
				stats.test(run = False),
				utils.test(run = False)
			]
		]

else:
	pass

