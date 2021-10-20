
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from ...testing import moduletest
	from . import callback
	from . import mlr
	from . import pickles
	from . import _pyutils
	from . import _cutils

	@moduletest
	def test():
		"""
		Run the tests on this module
		"""
		return ["vice.core.tests",
			[
				callback.test(run = False),
				mlr.test(run = False),
				pickles.test(run = False),
				_pyutils.test(run = False),
				_cutils.test(run = False)
			]
		]

else:
	pass

