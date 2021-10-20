
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:
	__all__ = [
		"crf",
		"msmf",
		"test"
	]
	from ....testing import moduletest
	from . import _crf as crf
	from . import _msmf as msmf
	from . import _remnants as remnants
	from . import ssp

	@moduletest
	def test():
		"""
		Run all test functions in this module
		"""
		return ["vice.core.ssp",
			[
				remnants.test_kalirai08(),
				crf.test(run = False),
				msmf.test(run = False),
				ssp.test(run = False)
			]
		]

else:
	pass

