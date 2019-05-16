"""
Asymptotic Giant Branch Star Nucleosynthetic Yield Tools 
========================================================
In the current version of VICE, users are allowed to select 
between two tables of nucleosynthetic yields from asymptotic 
giant branch stars - those published by the Karakas (2010) and 
Cristallo et al. (2011) studies.  

Included Features 
================= 
grid :: <function> 
	Return the stellar mass-metallicity grid of fractional nucleosynethetic 
	yields for a given element and study to the user. 

References 
========== 
Cristallo (2011), ApJS, 197, 17 
Karakas (2010), MNRAS, 403, 1413 
"""

from __future__ import absolute_import
from .grid import yield_grid as grid
import sys 

__all__ = ["grid"]

del absolute_import 
if sys.version_info[0] < 3: 
	__all__ = [str(i) for i in __all__]
	del i 
else:
	pass 
del sys 


