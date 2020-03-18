
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["test"] 
	from ...tests._test_utils import moduletest 
	from ..dataframe import test as dataframe 
	from ..io import test as io 
	from ..objects import test as objects 
	from ..outputs import test as outputs 
	from ..singlezone import test as singlezone 
	from ..ssp import test as ssp 
	from .pickles import test as pickles 

	@moduletest 
	def test(): 
		""" 
		Run the tests on this module 
		""" 
		return ["vice.core", 
			[
				dataframe(run = False), 
				io(run = False), 
				objects(run = False), 
				outputs(run = False), 
				pickles(run = False), 
				singlezone(run = False), 
				ssp(run = False) 
			] 
		] 

else: 
	pass 

