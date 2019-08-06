""" 
Nucleosynthetic Yield Presets 
============================= 
Save copies of user-constructed yield settings for loading into VICE. Users 
can create external yield scripts which modify VICE's nucleosynthetic yield 
settings, then make these settings available to import statements. 

Included Features 
================= 
save :: <function> 
	Save a copy of the yield settings declared in external python code. This 
	will make the yield settings available to import statements for future 
	simulations. 
remove :: <function> 
	Remove a copy of yield presets previously installed. 
starburst19 :: yield preset  
	The yield presets associated with Johnson & Weinberg (2019). 

Example 
======= 
>>> from vice.yields.presets import starburst19 

References 
========== 
Johnson & Weinberg (2019, in prep) 
""" 

from __future__ import absolute_import 

__all__ = [] 
from ._presets import * 
__all__.extend(_presets.__all__) 

del absolute_import 
del _presets 
