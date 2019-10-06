"""
Nucleosynthetic Yield Tools 
=========================== 
Each module stores built-in yield tables and user-presets for different 
enrichment channels. 

agb :: asymptotic giant branch stars 
ccsne :: core collapse supernovae 
sneia :: type Ia supernovae 
"""

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = ["agb", "ccsne", "sneia", "presets"]  
	from . import agb 
	from . import ccsne 
	from . import sneia 
	from . import presets 
else: 
	pass 

