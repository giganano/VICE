
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from ....testing import moduletest
	from . import hydrodiskstars
	from ..data.tests import test_download

	@moduletest
	def test():
		r"""
		vice.toolkit.hydrodisk module test
		"""
		return ["vice.toolkit.hydrodisk",
			[
				test_download(),
				hydrodiskstars.test(run = False)
			]
		]

else:
	pass
