r"""
This file implements unit testing of the ``cutoff`` derived class.
"""

from __future__ import absolute_import
from ..cutoff import cutoff
from ..._yield_integrator import _MINIMUM_MASS_
from .....testing import moduletest
from .....testing import unittest
import random


@moduletest
def test():
	r"""
	vice.yields.ccsne.engines.cutoff module test
	"""
	return ["vice.yields.ccsne.engines.cutoff",
		[ 	
			test_initialization(),
			test_call()
		]
	]


@unittest
def test_initialization():
	r"""
	Performs a unit test on the ``cutoff`` constructor.
	"""
	def test():
		try:
			test_ = cutoff()
		except:
			return False
		status = isinstance(test_, cutoff)
		status &= test_.masses == []
		status &= test_.frequencies == []
		return status
	return ["vice.yields.ccsne.engines.cutoff.__init__", test]


@unittest
def test_call():
	r"""
	Performs a unit test on the __call__ function.
	"""
	def test():
		try:
			test_ = cutoff()
		except:
			return None
		random.seed()
		status = True
		for i in range(100):
			new_threshold = _MINIMUM_MASS_ + (100 -
				_MINIMUM_MASS_) * random.random()
			try:
				test_.collapse_mass = new_threshold
			except:
				return None
			for j in range(10):
				test_mass = _MINIMUM_MASS_ + (100 -
					_MINIMUM_MASS_) * random.random()
				try:
					status &= test_(test_mass) == float(
						test_mass <= new_threshold)
				except:
					return False
				if not status: break
			if not status: break
		return status
	return ["vice.yields.ccsne.engines.cutoff.__call__", test]


