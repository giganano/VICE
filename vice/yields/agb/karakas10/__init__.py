r"""
Karakas (2010), MNRAS, 403, 1413 Asymptotic Giant Branch (AGB) star yields. 

**Signature**: from vice.yields.agb import karakas10 

Importing this module will set the AGB star yield setting for all elements up 
to nickel to "karakas10". 

Raises 
------
* ScienceWarning 
	The Karakas (2010) study did not report yields for elements heavier than 
	nickel. The settings for these elements will not be modified. 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	from ...._globals import ScienceWarning 
	from ....core.dataframe._builtin_dataframes import atomic_number 
	from .. import settings as __settings 
	import warnings 
	for i in __settings.keys(): 
		if atomic_number[i] <= 28: __settings[i] = "karakas10" 

	warnings.warn("""\
The Karakas (2010) study did not report yields for elements heavier than \
nickel. AGB star yield settings for these elements will not be modified.""", 
		ScienceWarning)  

else: 
	pass 

