"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
"""

from __future__ import absolute_import
from .yield_integrator import integrate as fractional_cc_yield

__all__ = ["fractional_cc_yield"]
__all__ = [str(i) for i in __all__] # appease python 2 strings 
