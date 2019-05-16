"""
This module handles pure systematics within VICE. 
"""

from __future__ import absolute_import 

try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if __VICE_SETUP__: 
	from ._build import write_build as _write_build
	__all__ = ["_write_build"] 
else:
	from ._build import read_build as _show_build
	__all__ = ["_show_build"]


