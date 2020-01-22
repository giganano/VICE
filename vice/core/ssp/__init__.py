
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = [
		"single_stellar_population", 
		"cumulative_return_fraction", 
		"main_sequence_mass_fraction" 
	] 
	from ._ssp import single_stellar_population 
	from ._crf import cumulative_return_fraction 
	from ._msmf import main_sequence_mass_fraction 
else: 
	pass 


