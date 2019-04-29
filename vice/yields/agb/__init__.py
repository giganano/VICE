# This file, included with the VICE package, is protected under the terms of the 
# associated MIT License, and any use or redistribution of this file in original 
# or altered form is subject to the copyright terms therein. 

"""
Asymptotic Giant Branch Star Nucleosynthetic Yield Tools 
========================================================
In the current version of VICE, nucleosynthetic yields from AGB stars allows 
users to select between the tables published in the Karakas (2010) and the 
Cristallo et al. (2011) studies. 

Included Features 
================= 
grid :: <function> 
	Return the stellar mass-metallicity grid of fractional nucleosynethetic 
	yields for a given element and study to the user. 

References 
========== 
Karakas (2010), MNRAS, 403, 1413 
Cristallo (2011), ApJS, 197, 17 
"""

from __future__ import absolute_import
from .grid import yield_grid as grid
import sys 

__all__ = ["grid"]
__all__ = [str(i) for i in __all__] # appease python 2 strings 

del absolute_import 
if sys.version_info[0] < 3: 
	del i 
else:
	pass 
del sys 


