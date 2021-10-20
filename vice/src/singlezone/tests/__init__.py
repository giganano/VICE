
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from ....testing import moduletest
	from . import _singlezone # import test
	from . import cases

	@moduletest
	def test():
		r"""
		vice.src.singlezone module test
		"""
		return ["vice.src.singlezone",
			[
				_singlezone.test(run = False),
				cases.test(run = False)
			]
		]

else:
	pass
