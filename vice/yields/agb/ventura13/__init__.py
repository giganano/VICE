r""" 
Ventura et al. (2013), MNRAS, 431, 3642 Asymptotic Giant Branch (AGB) Star 
yields. 

**Signature**: from vice.yields.agb import ventura13 

.. versionadded:: 1.3.0 

Importing this module will set the AGB star yield settings for all elements 
where yield tables are available to "ventura13". 

.. note:: This module is not imported with a simple ``import vice`` statement. 

Raises 
------
* ScienceWarning 
	This module only provides tables for the following elements: he, c, n, o, 
	ne, na, mg, al, si. The settings for other elements will not be modified. 
""" 

try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	from ...._globals import ScienceWarning 
	from .._grid_reader import _VENTURA13_ELEMENTS_ 
	from .. import settings as __settings 
	import warnings 
	for elem in _VENTURA13_ELEMENTS_: __settings[elem] = "ventura13" 

	warnings.warn("""\
The Ventura (2013) study reported yields only for the following elements: %s. \
AGB star yield settings for other elements will not be modified.""" % (
		str(_VENTURA13_ELEMENTS_)), ScienceWarning) 

else: pass 

