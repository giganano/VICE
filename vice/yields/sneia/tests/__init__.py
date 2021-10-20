
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

	@moduletest
	def test():
		"""
		Run the tests on this module
		"""
		tests = [
			lookup.test_single(),
			lookup.test_fractional(),
			imports.test(run = False)
		]
		try:
			from .. import iwamoto99
			tests.append(iwamoto99.test(run = False))
		except: pass # import tests will show their failure
		try:
			from .. import seitenzahl13
			tests.append(seitenzahl13.test(run = False))
		except: pass
		try:
			from .. import gronow21
			tests.append(gronow21.test(run = False))
		except: pass
		return ["vice.yields.sneia", tests]

else:
	pass

