
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from ....testing import moduletest 
	from ....testing import unittest 
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
			imports.test(run = False) 
		] 
		try: 
			from .. import LC18 
			tests.append(LC18.test(run = False)) 
		except: pass 
		try: 
			from .. import CL13 
			tests.append(CL13.test(run = False)) 
		except: pass 
		try: 
			from .. import CL04 
			tests.append(CL04.test(run = False)) 
		except: pass 
		try: 
			from .. import WW95 
			tests.append(WW95.test(run = False)) 
		except: pass 
		try: 
			from .. import NKT13 
			tests.append(NKT13.test(run = False)) 
		except: pass 
		tests.append(integrator.test(run = False)) 
		return ["vice.yields.ccsne", tests] 

else: 
	pass 

