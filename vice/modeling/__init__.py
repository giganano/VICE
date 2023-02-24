r"""
VICE Statistical Modeling Module

**Signature**: vice.modeling

Contains
--------
matrix : ``object``
	Generic matrices for linear algebra operations.
"""

try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["matrix", "test"]
	from .matrix import matrix
	from .tests import test

else:
	pass

