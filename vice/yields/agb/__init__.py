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

__all__ = ["grid"]
__all__ = [str(i) for i in __all__] 	# appease python 2 strings 

from ._grid_reader import yield_grid as grid 

