# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ....._globals import _VERSION_ERROR_
from .....testing import moduletest
from .....testing import unittest
from .separation import stellar_migration
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from . cimport _separation


@moduletest
def separation_test():
	r"""
	Runs a separation test on the multizone object. This runs a case with one
	star-forming and another non-star-forming zone in which all stars move to
	the quiescent zone immediately after formation. In this test, zone 0 is
	the star-forming zone and zone 1 is the quiescent zone.
	"""
	msg = "vice.core.multizone edge case : separation"
	try:
		_TEST_ = separation(n_zones = 2)
		_TEST_.zones[1].tau_star = float("inf")
		_TEST_.migration.stars = stellar_migration
		_TEST_.run()
	except:
		return [msg, None]
	return [msg,
		[
			_TEST_.test_m_AGB(),
			_TEST_.test_update_elements(),
			_TEST_.test_update_zone_evolution(),
			_TEST_.test_tracers_MDF(),
			_TEST_.test_migrate(),
			_TEST_.test_multizone_stellar_mass(),
			_TEST_.test_recycle_metals_from_tracers(),
			_TEST_.test_gas_recycled_in_zones(),
			_TEST_.test_m_sneia()
		]
	]


cdef class separation:

	r"""
	A class intended to run the separation edge-case test on the multizone
	class. This is a case in which there are two zones - one star forming and
	one non-star forming, and all of the stars move to the non-star forming
	zone immediately after formation.
	"""

	@unittest
	def test_m_AGB(self):
		r"""
		vice.src.multizone.agb.m_AGB separation test
		"""
		def test():
			return _separation.separation_test_m_AGB_from_tracers(self._mz)
		return ["vice.src.multizone.agb.m_AGB", test]

	@unittest
	def test_update_elements(self):
		r"""
		vice.src.multizone.element.update_elements separation test
		"""
		def test():
			return _separation.separation_test_update_elements(self._mz)
		return ["vice.src.multizone.element.update_elements", test]

	@unittest
	def test_update_zone_evolution(self):
		r"""
		vice.src.multizone.ism.update_zone_evolution separation test
		"""
		def test():
			return _separation.separation_test_update_zone_evolution(self._mz)
		return ["vice.src.multizone.ism.update_zone_evolution", test]

	@unittest
	def test_tracers_MDF(self):
		r"""
		vice.src.multizone.mdf.tracers_MDF separation test
		"""
		def test():
			return _separation.separation_test_tracers_MDF(self._mz)
		return ["vice.src.multizone.mdf.tracers_MDF", test]

	@unittest
	def test_migrate(self):
		r"""
		vice.src.multizone.migration.migrate separation test
		"""
		def test():
			return _separation.separation_test_migrate(self._mz)
		return ["vice.src.multizone.migration.migrate", test]

	@unittest
	def test_multizone_stellar_mass(self):
		r"""
		vice.src.multizone.multizone.multizone_stellar_mass separation test
		"""
		def test():
			return _separation.separation_test_multizone_stellar_mass(self._mz)
		return ["vice.src.multizone.multizone.multizone_stellar_mass", test]

	@unittest
	def test_recycle_metals_from_tracers(self):
		r"""
		vice.src.multizone.recycling.recycle_metals_from_tracers separation test
		"""
		def test():
			return _separation.separation_test_recycle_metals_from_tracers(
				self._mz)
		return ["vice.src.multizone.recycling.recycle_metals_from_tracers",
			test]

	@unittest
	def test_gas_recycled_in_zones(self):
		r"""
		vice.src.multizone.recycling.gas_recycled_in_zones separation test
		"""
		def test():
			return _separation.separation_test_gas_recycled_in_zones(self._mz)
		return ["vice.src.multizone.recycling.gas_recycled_in_zones", test]

	@unittest
	def test_m_sneia(self):
		r"""
		vice.src.multizone.sneia.m_sneia separation test
		"""
		def test():
			return _separation.separation_test_m_sneia_from_tracers(self._mz)
		return ["vice.src.multizone.sneia.m_sneia", test]

