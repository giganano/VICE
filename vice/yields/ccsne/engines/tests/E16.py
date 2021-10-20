r"""
This file implements unit testing of the ``E16`` derived class.
"""

from __future__ import absolute_import
from ..E16 import E16
from ..._yield_integrator import _MINIMUM_MASS_
from .....testing import moduletest
from .....testing import unittest
import random


@moduletest
def test():
	r"""
	vice.yields.ccsne.engines.E16 module test
	"""
	return ["vice.yields.ccsne.engines.E16",
		[
			test_initialization(),
			test_call(),
			none_explode(),
			all_explode()
		]
	]


@unittest
def test_initialization():
	r"""
	Performs a unit test on the ``E16`` constructor.
	"""
	def test():
		try:
			test_ = E16()
		except:
			return False
		return isinstance(test_, E16)
	return ["vice.yields.ccsne.engines.E16.__init__", test]


@unittest
def test_call():
	r"""
	Performs a unit test on the __call__ function.
	"""
	def test():
		try:
			test_ = E16()
		except:
			return None
		random.seed()
		status = True
		for i in range(1000):
			try:
				x = test_(8 + 92 * random.random())
			except:
				return False
			status &= x == 0.0 or x == 1.0
			if not status: break
		return status
	return ["vice.yields.ccsne.engines.E16.__call__", test]


@unittest
def none_explode():
	r"""
	Performs an edge-case unit test on the ``E16`` object by modifying the
	slope and intercept in such a manner that no massive star should explode.
	"""
	def test():
		try:
			test_ = E16()
			test_.slope = 0
			test_.intercept = -100
		except:
			return None
		random.seed()
		status = True
		for i in range(1000):
			try:
				x = test_(_MINIMUM_MASS_ + (100 - _MINIMUM_MASS_) *
					random.random())
			except:
				return None
			status &= x == 0.0
			if not status: break
		return status
	return ["vice.yields.ccsne.engines.E16 edge case : none explode", test]


@unittest
def all_explode():
	r"""
	Performs an edge-case unit test on the ``E16`` object by modifying the
	slope and intercept in such a manner that all massive stars should explode.
	"""
	def test():
		try:
			test_ = E16()
			test_.slope = 0
			test_.intercept = 100
		except:
			return None
		random.seed()
		status = True
		for i in range(1000):
			try:
				x = test_(_MINIMUM_MASS_ + (100 - _MINIMUM_MASS_) *
					random.random())
			except:
				return None
			status &= x == 1.0
			if not status: break
		return status
	return ["vice.yields.ccsne.engines.E16 edge case : all explode", test]

