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
	from ._build import check_cython as _check_cython 
	from ._copy_docs import copy_docs as _copy_docs
	__all__ = ["_write_build", "_check_cython", "_copy_docs"]  
else:
	from ._build import read_build as _show_build
	__all__ = ["_show_build"]


