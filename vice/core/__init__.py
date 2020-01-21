
from __future__ import absolute_import 

try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = ["dataframe", "singlezone", "multizone", "mirror"]    
	from ._single_stellar_population import * 
	# from ._dataframe import base as dataframe 
	# from ._builtin_dataframes import * 
	from .dataframe import base as dataframe 
	from .dataframe._builtin_dataframes import * 
	from ._output import * 
	# from ._pysinglezone import singlezone 
	from .singlezone import singlezone 
	from ._pymultizone import multizone 
	from ._mirror import mirror 

	__all__.extend(_single_stellar_population.__all__) 
	__all__.extend(_builtin_dataframes.__all__) 
	__all__.extend(_output.__all__) 
	__all__ = [str(i) for i in __all__] 	# appease python 2 strings 
else: 
	pass 
