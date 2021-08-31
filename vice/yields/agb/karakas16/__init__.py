r""" 
Karakas & Lugaro (2016), ApJ, 825, 26 Asymptotic Giant Branch (AGB) star yields 

**Signature**: from vice.yields.agb import karakas16 

.. versionadded:: 1.3.0 

Importing this module will set the AGB star yield setting for all elements to 
"karakas16". 

.. note:: This module is not imported with a simple ``import vice`` statement. 

Along with the yields published in Karakas & Lugaro (2016), this module also 
includes those from Karakas et al. (2018) [1]_, which extends the earlier set 
to lower metallicity (Z = 0.0028, characteristic of stars in the Small 
Magellanic Cloud). 

.. [1] Karakas et al. (2018), MNRAS, 477, 421 
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
		for i in __settings.keys(): __settings[i] = "karakas16" 
	else: pass 

else: pass 

