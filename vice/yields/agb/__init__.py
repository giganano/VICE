r"""
Asymptotic Giant Branch (AGB) Star Nucleosynthetic Yield Tools 

Analyze built-in yield tables and modify yield settings for use in simulations. 
This package provides tables from the following nucleosynthetic yield studies: 

	- Cristallo et al. (2011) [1]_ 
	- Karakas (2010) [2]_ 
	- Ventura et al. (2013) [3]_ 

Contents 
--------
grid : <function> 
	Return the stellar mass-metallicity grid of fractional nucleosynthetic 
	yields for given element and study 
interpolator : ``object`` 
	Linearly interpolates on the stellar mass-metallicity grid of yields for 
	use in the global yield settings. 
settings : ``dataframe`` 
	Stores current settings for these yields 
cristallo11 : yield preset 
	Sets the yields according to the Cristallo et al. (2011, 2015) studies. 
karakas10 : yield preset 
	Sets the yields according to the Karakas (2010) study 

Notes 
-----
The data stored in this module are reported for each corresponding study 
*as published*. With the exception of converting the values to *fractional* 
yields (i.e. by dividing by progenitor initial mass), they were not modified in 
any way. 

.. [1] Cristallo et al. (2011), ApJS, 197, 17 
.. [2] Karakas (2010), MNRAS, 403, 1413 
.. [3] Ventura et al. (2013), MNRAS, 431, 3642 
"""

from __future__ import absolute_import
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = ["grid", "interpolator", "settings", "test"] 
	__all__ = [str(i) for i in __all__] 	# appease python 2 strings 

	from ._grid_reader import yield_grid as grid 
	from .interpolator import interpolator 
	from .settings import settings 
	from .tests import test 

else: 
	pass 

