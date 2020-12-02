
from __future__ import absolute_import 
__all__ = ["test"] 
from ....core.singlezone.singlezone import singlezone 
from ....testing import unittest 
from ..repair_function import repair_function 


@unittest 
def test_repair_function(): 
	r""" 
	vice.toolkit.repair_function unit test 
	""" 
	def test(): 
		try: 
			out = singlezone(name = "test").run([0.01 * i for i in range(1001)], 
				overwrite = True, capture = True) 
		except: 
			return None 
		status = True 
		keys = ["sfr", "ifr", "mgas", "eta", "tau_star"] 
		try: 
			for i in keys: 
				test_ = repair_function("test", i) 
				status &= test_.xcoords == out.history["time"] 
				if i == "eta": 
					status &= test_.ycoords == out.history["eta_0"] 
				elif i == "tau_star": 
					status &= test_.ycoords == [1.e-9 * a / b if b else float(
						"inf") for a, b in zip(
							out.history["mgas"], out.history["sfr"])] 
				else: 
					status &= test_.ycoords == out.history[i] 
				if not status: break 
			for i in out.elements: 
				test_ = repair_function("test", "z_in(%s)" % (i)) 
				status &= test_.ycoords == out.history["z_in(%s)" % (i)] 
				if not status: break 
		except: 
			return False 
		return status 
	return ["vice.toolkit.repair_function", test] 

