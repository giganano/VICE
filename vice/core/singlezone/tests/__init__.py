
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test", "trials"]
	from ....testing import moduletest
	from . import _singlezone
	from . import trials
	from .from_output import test_from_output
	from ....src.singlezone.tests import test as src_test

	@moduletest
	def test():
		r"""
		vice.singlezone module test
		"""
		return ["vice.singlezone",
			[
				test_from_output(),
				_singlezone.test(run = False),
				trials.test(run = False),
				src_test(run = False)
			]
		]
		
else:
	pass
