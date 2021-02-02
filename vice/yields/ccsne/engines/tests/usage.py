r""" 
This file implements usage tests of all of the explodability engines - by using 
them in a single call to vice.yields.ccsne.fractional, they assess whether or 
not they perform this primary functionality. 
""" 

from __future__ import absolute_import 
__all__ = ["test"] 
from ..E16 import E16 
from ..cutoff import cutoff 
from ..S16.W18 import W18 
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
			test_cutoff(), 
			test_E16(), 
			test_W18() 
		] 
	] 


@unittest 
def test_cutoff(): 
	r""" 
	vice.yields.ccsne.engines.cutoff usage test 
	""" 
	def test(): 
		try: 
			cutoff_ = cutoff() 
		except: 
			return None 
		try: 
			fractional('o', explodability = cutoff_) 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.engines.cutoff", test] 


@unittest 
def test_E16(): 
	r""" 
	vice.yields.ccsne.engines.E16 usage test 
	""" 
	def test(): 
		try: 
			E16_ = E16() 
		except: 
			return None 
		try: 
			fractional('o', explodability = E16_) 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.engines.E16", test] 


@unittest 
def test_W18(): 
	r""" 
	vice.yields.ccsne.engines.S16.W18 usage test 
	""" 
	def test(): 
		try: 
			W18_ = W18() 
		except: 
			return None 
		try: 
			fractional('o', explodability = W18_) 
		except: 
			return False 
		return True 
	return ["vice.yields.ccsne.engines.S16.W18", test] 

