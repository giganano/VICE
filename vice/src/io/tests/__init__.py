
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from ....testing import moduletest
	from . import _agb
	from . import _ccsne
	from . import _sneia
	from . import _utils
	from . import singlezone

	@moduletest
	def test():
		"""
		Run the tests on this module
		"""
		return ["vice.core.io.tests",
			[
				_agb.test(run = False),
				_ccsne.test(run = False),
				singlezone.test(run = False),
				_sneia.test(run = False),
				_utils.test(run = False)
			]
		]

else:
	pass

