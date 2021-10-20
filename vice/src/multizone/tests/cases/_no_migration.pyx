# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ....._globals import _VERSION_ERROR_
from .....testing import moduletest
from .....testing import unittest
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from . cimport _no_migration

_TIMES_ = [0.05 * i for i in range(201)]


@moduletest
def no_migration_test():
	r"""
	No migration edge-case test on multizone object.
	"""
	msg = "vice.core.multizone edge case : no migration"
	try:
		_TEST_ = no_migration(n_zones = 5)
		_TEST_.run()
	except:
		[msg, None]
	return [msg,
		[
			_TEST_.test_m_agb(),
			_TEST_.test_multizone_unretained(),
			_TEST_.test_migrate(),
			_TEST_.test_multizone_stellar_mass(),
			_TEST_.test_recycle_metals_from_tracers(),
			_TEST_.test_gas_recycled_in_zones(),
			_TEST_.test_m_sneia(),
		]
	]


cdef class no_migration:

	r"""
	A class intended to run unit tests for no migration multizone cases. These
	are cases which should always produce no stellar migration between zones.
	"""
	
	@unittest
	def test_m_agb(self):
		r"""
		vice.src.multizone.agb.m_AGB_from_tracers no migration test
		"""
		def test():
			return _no_migration.no_migration_test_m_AGB_from_tracers(self._mz)
		return ["vice.src.multizone.agb.m_agb", test]

	@unittest
	def test_multizone_unretained(self):
		r"""
		vice.src.multizone.ism.multizone_unretained no migration test
		"""
		def test():
			return _no_migration.no_migration_test_multizone_unretained(
				self._mz)
		return ["vice.src.multizone.ism.multizone_unretained", test]

	@unittest
	def test_migrate(self):
		r"""
		vice.src.multizone.migration.migrate no migration test
		"""
		def test():
			return _no_migration.no_migration_test_migrate(self._mz)
		return ["vice.src.multizone.migration.migrate", test]

	@unittest
	def test_multizone_stellar_mass(self):
		r"""
		vice.src.multizone.multizone.multizone_stellar_mass no migration test
		"""
		def test():
			return _no_migration.no_migration_test_multizone_stellar_mass(
				self._mz)
		return ["vice.src.multizone.multizone.multizone_stellar_mass", test]

	@unittest
	def test_recycle_metals_from_tracers(self):
		r"""
		vice.src.multizone.recycling.recycle_metals_from_tracers no migration
		test
		"""
		def test():
			return _no_migration.no_migration_test_recycle_metals_from_tracers(
				self._mz)
		return ["vice.src.multizone.recycling.recycle_metals_from_tracers",
			test]

	@unittest
	def test_gas_recycled_in_zones(self):
		r"""
		vice.src.multizone.recycling.gas_recycled_in_zones no migration test
		"""
		def test():
			return _no_migration.no_migration_test_gas_recycled_in_zones(
				self._mz)
		return ["vice.src.multizone.recycling.gas_recycled_in_zones", test]

	@unittest
	def test_m_sneia(self):
		r"""
		vice.src.multizone.sneia.m_sneia_from_tracers no migration test
		"""
		def test():
			return _no_migration.no_migration_test_m_sneia_from_tracers(
				self._mz)
		return ["vice.src.multizone.sneia.m_sneia", test]

