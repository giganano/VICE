r"""
This file implements unit testing of the ``engine`` base class.
"""

from __future__ import absolute_import
from ..engine import engine
from ..._yield_integrator import _MINIMUM_MASS_
from .....testing import moduletest
from .....testing import unittest
import random


@moduletest
def test():
	r"""
	vice.yields.ccsne.engines.engine module test
	"""
	return ["vice.yields.ccsne.engines.engine",
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
	Performs a unit test on the ``engine`` constructor.
	"""
	def test():
		masses = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
		frequencies = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
		try:
			test_ = engine(masses, frequencies)
		except:
			return False
		status = isinstance(test_.masses, list)
		status &= test_.masses == masses
		status &= isinstance(test_.frequencies, list)
		status &= test_.frequencies == frequencies
		return status
	return ["vice.yields.ccsne.engines.engine.__init__", test]


@unittest
def test_call():
	r"""
	Performs a unit test on the __call__ function.
	"""
	def test():
		masses = [10, 20, 30, 40]
		frequencies = [0.0, 1.0, 0.0, 1.0]
		try:
			test_ = engine(masses, frequencies)
		except:
			return None
		status = test_(10) == 0.0
		status &= test_(20) == 1.0
		status &= test_(30) == 0.0
		status &= test_(40) == 1.0
		status &= test_(50) == 1.0
		status &= test_(9) == 0.0
		status &= test_(15) == 0.5
		status &= test_(25) == 0.5
		status &= test_(12) == 0.2
		status &= test_(38) == 0.8
		return status
	return ["vice.yields.ccsne.engines.engine.__call__", test]


@unittest
def none_explode():
	r"""
	Performs an edge-case unit test on the ``engine`` class by constructing one
	in which no stars explode.
	"""
	def test():
		try:
			test_ = engine([_MINIMUM_MASS_, 100], [0, 0])
		except:
			return None
		random.seed()
		status = True
		for i in range(100):
			mass = _MINIMUM_MASS_ + (100 - _MINIMUM_MASS_) * random.random()
			status &= test_(mass) == 0.0
			if not status: break
		return status
	return ["vice.yields.ccsne.engines.engine edge case : none explode", test]


@unittest
def all_explode():
	r"""
	Performs an edge-case unit test on the ``engine`` class by constructing one
	in which all stars explode.
	"""
	def test():
		try:
			test_ = engine([_MINIMUM_MASS_, 100], [1, 1])
		except:
			return None
		random.seed()
		status = True
		for i in range(1000):
			mass = _MINIMUM_MASS_ + (100 - _MINIMUM_MASS_) * random.random()
			status &= test_(mass) == 1.0
			if not status: break
		return status
	return ["vice.yields.ccsne.engines.engine edge case : all explode", test]

