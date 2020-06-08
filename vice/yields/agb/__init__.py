r"""
Asymptotic Giant Branch (AGB) Star Nucleosynthetic Yield Tools 

Analyze built-in yield tables and modify yield settings for use in simulations. 
This package provides tables from the following nucleosynthetic yield studies: 

	- Cristallo et al. (2011) [1]_ 
	- Karakas (2010) [2]_ 

Contents 
--------
grid : <function> 
	Return the stellar mass-metallicity grid of fractional nucleosynthetic 
	yields for given element and study 

.. [1] Cristallo et al. (2011), ApJS, 197, 17 
.. [2] Karakas (2010), MNRAS, 403, 1413 
"""

from __future__ import absolute_import
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = ["grid", "test"] 
	__all__ = [str(i) for i in __all__] 	# appease python 2 strings 

	from ._grid_reader import yield_grid as grid 
	from .tests import test 

else: 
	pass 

