r"""
This file implements usage tests of all of the explodability engines - by using
them in a single call to vice.yields.ccsne.fractional, they assess whether or
not they perform this primary functionality.
"""

from __future__ import absolute_import
__all__ = ["test"]
from ..E16 import E16
from ..cutoff import cutoff
from ..S16.N20 import N20
from ..S16.S19p8 import S19p8
from ..S16.W15 import W15
from ..S16.W18 import W18
from ..S16.W20 import W20
from ..._yield_integrator import integrate as fractional
from .....testing import moduletest
from .....testing import unittest


@moduletest
def test():
	r"""
	vice.yields.ccsne.engines built-in objects usage tests
	"""
	return ["vice.yields.ccsne.engines usage tests",
		[
			test_engine(cutoff, "cutoff"),
			test_engine(E16, "E16"),
			test_engine(N20, "S16.N20"),
			test_engine(S19p8, "S16.S19p8"),
			test_engine(W15, "S16.W15"),
			test_engine(W18, "S16.W18"),
			test_engine(W20, "S16.W20")
		]
	]


@unittest
def test_engine(obj, name):
	r"""
	vice.yields.ccsne.engines derived class usage test
	"""
	def test():
		try:
			test_ = obj()
		except:
			return None
		try:
			fractional('o', explodability = test_)
		except:
			return False
		return True
	return ["vice.yields.ccsne.engines.%s" % (name), test]

