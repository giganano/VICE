r"""
VICE Statistical Modeling Module

**Signature**: vice.modeling

.. versionadded:: 1.X.0

Contains
--------
matrix : ``object``
	Generic matrices for linear algebra operations.
vector : ``object`` [inherits from ``matrix``]
	Generic row vectors for linear algebra operations.
"""

try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["matrix", "vector", "test"]
	from ._matrix import matrix
	from ._vector import vector
	from .tests import test

else:
	pass

