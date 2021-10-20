r"""
This file implements testing of the explodability engines in the parent
directory.
"""

from __future__ import absolute_import
__all__ = ["test"]
from ......_globals import _DIRECTORY_
from ......testing import moduletest
from ......testing import unittest
from ..N20 import N20
from ..S19p8 import S19p8
from ..W15 import W15
from ..W18 import W18
from ..W20 import W20


@moduletest
def test():
	r"""
	Performs a module test on all of the Sukhbold et al. (2016) [1]_ built-in
	explosion engines.

	.. [1] Sukhbold et al. (2016), ApJ, 821, 38
	"""
	return ["vice.yields.ccsne.engines.S16",
		[
			test_engine(N20, "N20"),
			test_engine(S19p8, "S19p8"),
			test_engine(W15, "W15"),
			test_engine(W18, "W18"),
			test_engine(W20, "W20")
		]
	]


@unittest
def test_engine(obj, name):
	r"""
	Performs a unit test on the constructors of each of the Sukhbold et al.
	(2016) [1]_ explosion engines.

	.. [1] Sukhbold et al. (2016), ApJ, 821, 38
	"""
	def test():
		try:
			test_ = obj()
		except:
			return False
		status = isinstance(test_, obj)

		# Base the rest of the test on whether or not the ``masses`` and
		# ``frequencies`` attribute match associated .dat file.
		if status:
			filename = "%syields/ccsne/engines/S16/%s.dat" % (_DIRECTORY_, name)
			with open(filename, 'r') as f:
				while True:
					line = f.readline()
					if line[0] != '#': break
				n = 0
				status = True
				while line != "":
					line = [float(_) for _ in line.split()]
					status &= test_.masses[n] == line[0]
					status &= test_.frequencies[n] == line[1]
					if not status: break
					n += 1
					line = f.readline()
				f.close()
		else: pass
		return status
	return ["vice.yields.ccsne.engines.S16.%s" % (name), test]

