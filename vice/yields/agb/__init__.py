"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
"""

from __future__ import absolute_import
from .grid import yield_grid as grid

__all__ = ["grid"]
__all__ = [str(i) for i in __all__] # appease python 2 strings 


del absolute_import 
del i 


