
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from ....testing import moduletest
	from ....testing.unittest import _unittest as unittest
	from .. import engines
	from . import grid_reader
	from . import integrator
	from . import imports

	@moduletest
	def test():
		r"""
		Run unit tests on this module
		"""
		tests = [
			grid_reader.test_table(),
			imports.test(run = False),
			engines.test(run = False)
		]
		try:
			from .. import LC18
			tests.append(LC18.test(run = False))
		except:
			# Creates a unittest with a "skipped" message
			tests.append(unittest("vice.yields.ccsne.LC18", lambda: None))
		try:
			from ..S16 import N20
			tests.append(N20.test(run = False))
		except:
			tests.append(unittest("vice.yields.ccsne.S16.N20", lambda: None))
		try:
			from ..S16 import W18
			tests.append(W18.test(run = False))
		except:
			tests.append(unittest("vice.yields.ccsne.S16.W18", lambda: None))
		try:
			from ..S16 import W18F
			tests.append(W18F.test(run = False))
		except:
			tests.append(unittest("vice.yields.ccsne.S16.W18F", lambda: None))
		try:
			from .. import CL13
			tests.append(CL13.test(run = False))
		except:
			tests.append(unittest("vice.yields.ccsne.CL13", lambda: None))
		try:
			from .. import NKT13
			tests.append(NKT13.test(run = False))
		except:
			tests.append(unittest("vice.yields.ccsne.NKT13"), lambda: None)
		try:
			from .. import CL04
			tests.append(CL04.test(run = False))
		except:
			tests.append(unittest("vice.yields.ccsne.CL04", lambda: None))
		try:
			from .. import WW95
			tests.append(WW95.test(run = False))
		except:
			tests.append(unittest("vice.yields.ccsne.WW95", lambda: None))
		tests.append(integrator.test(run = False))
		return ["vice.yields.ccsne", tests]

else:
	pass

