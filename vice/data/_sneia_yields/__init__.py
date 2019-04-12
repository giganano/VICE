"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
"""

from __future__ import absolute_import
from .yield_calculations import single_detonation as single_ia_yield
from .yield_calculations import integrated_yield as fractional_ia_yield

__all__ = ["single_ia_yield", "fractional_ia_yield"]
__all__ = [str(i) for i in __all__] # appease python 2 strings 
