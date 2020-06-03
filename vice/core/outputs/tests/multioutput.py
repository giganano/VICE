
from __future__ import absolute_import 
__all__ = ["test_multioutput"] 
from ....testing import unittest 
from ...dataframe import base as dataframe 
from .. import multioutput 


@unittest 
def test_multioutput(): 
	r""" 
	vice.multioutput unit test 
	""" 
	from ...multizone import multizone 
	def test(): 
		try: 
			multizone(name = "test", n_zones = 3).run(
				[0.01 * i for i in range(1001)], 
				overwrite = True) 
			test_ = multioutput("test") 
		except: 
			return False 
		return (
			isinstance(test_, multioutput) and 
			isinstance(test_.zones, dataframe) and 
			isinstance(test_.stars, dataframe) 
		) 
	return ["vice.multioutput", test] 

