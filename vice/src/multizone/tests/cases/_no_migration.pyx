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
from libc.stdlib cimport malloc, free 
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
	except: 
		[msg, None] 
	return [msg, 
		[ 
			_TEST_.test_m_agb(), 
			_TEST_.test_multizone_unretained() 
		] 
	] 


cdef class no_migration: 

	r""" 
	A class intended to run unit tests for no migration multizone cases. These 
	are cases which should always produce no stellar migration between zones. 
	""" 

	def __init__(self, **kwargs): 
		if "name" in kwargs.keys(): del kwargs["name"] 
		super().__init__(name = "test", **kwargs) 
		self.align_name_attributes() 
		self.prep(_TIMES_) 
		self.outfile_check(True) 
		os.system("mkdir %s.vice" % (self.name)) 
		for i in range(self._mz[0].mig[0].n_zones): 
			os.system("mkdir %s.vice" % (self._zones[i].name)) 
		self.setup_migration() 
		_no_migration.multizone_setup(self._mz) 
		_no_migration.multizone_evolve_full(self._mz) 
		_no_migration.tracers_MDF(self._mz) 
		_no_migration.write_multizone_mdf(self._mz[0]) 
		if not _no_migration.multizone_open_tracer_file(self._mz): 
			_no_migration.write_tracers_header(self._mz[0]) 
			_no_migration.write_tracers_output(self._mz[0]) 
			_no_migration.multizone_close_tracer_file(self._mz) 
		else: 
			raise Exception 

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

