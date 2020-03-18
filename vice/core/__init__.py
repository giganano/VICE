
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = [
		"dataframe", 
		"singlezone", 
		"multizone", 
		"mirror", 
		"test" 
	] 

	from .singlezone import singlezone 
	from .mirror import mirror 
	from .multizone import multizone 
	from .outputs import * 
	from .ssp import * 
	from .dataframe._builtin_dataframes import * 
	__all__.extend(dataframe._builtin_dataframes.__all__) 
	from .dataframe import base as dataframe 
	__all__.extend(outputs.__all__) 
	__all__.extend(ssp.__all__) 

	from ..testing import moduletest 
	from .dataframe import test as test_dataframe 
	from .io import test as test_io 
	from .objects import test as test_objects 
	from .outputs import test as test_outputs 
	from .singlezone import test as test_singlezone 
	from .ssp import test as test_ssp 
	from . import tests 

	@moduletest 
	def test(): 
		return ["vice.core", 
			[ 
				test_dataframe(run = False), 
				test_io(run = False), 
				test_objects(run = False), 
				test_outputs(run = False), 
				test_singlezone(run = False), 
				test_ssp(run = False), 
				tests.test(run = False) 
			] 
		] 

else: 
	pass 
