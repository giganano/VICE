r"""
VICE Milky Way Tools
====================
Provides tools for use in modeling the chemical evolution of Milky Way-like
galaxies.

Contents
--------
milkyway : ``object``
	The object accessible after import as ``vice.milkyway``.
test : ``<function>``
	Run unit tests on the ``milkyway`` object.
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["milkyway", "test"]
	from .milkyway import milkyway
	from .tests import test

else: pass

