r""" 
Cristallo et al. (2011), ApJS, 197, 17 Asymptotic Giant Branch (AGB) star 
yields. 

**Signature**: from vice.yields.agb import cristallo11 

Importing this module will set the AGB star yield settings for all elements 
to "cristallo11". 

.. note:: This module is not imported with a simple ``import vice`` statement. 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 
try: 
	__VICE_DOCS__ 
except NameError: 
	__VICE_DOCS__ = False 

if not __VICE_SETUP__: 

	from .. import settings as __settings 
	if not __VICE_DOCS__: 
		for i in __settings.keys(): 
			__settings[i] = "cristallo11" 
	else: pass 

else: 
	pass 

