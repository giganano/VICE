r"""
VICE Interpolation Schema : Internal utilities for interpolation.

.. versionadded:: 1.2.0

Contents
--------
interp_scheme_1d : object
	A 1-D linear interpolation scheme given a list of (x, y) points.
interp_scheme_2d : object
	A 2-D linear interpolation scheme given lists of x- and y-coordinates and a
	2-D list of z-coordinates.
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["interp_scheme_1d", "interp_scheme_2d", "test"]
	from .interp_scheme_1d import interp_scheme_1d
	from .interp_scheme_2d import interp_scheme_2d
	from .tests import test

else: pass
