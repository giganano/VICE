r"""
Nucleosynthetic Yield Presets

.. versionadded:: 1.1.0

Save copies of user-constructed yield settings for loading into VICE. Users
can create external yield scripts which modify VICE's nucleosynthetic yield
settings, then make these settings available to import statements.

.. note:: These features may not function properly if VICE is installed
	locally (i.e. if it was installed with a ``--user`` flag). Please speak
	with your administrator about installing VICE globally if this is an
	issue.

Contents
--------
save : <function>
	Save a copy of the yield settings declared in external python code. This
	will make the yield settings available to import statements for future
	simulations.
remove : <function>
	Remove a copy of yield presets previously saved.
JW20 : yield preset
	The yield presets associated with Johnson & Weinberg (2020) [1]_.

.. [1] Johnson & Weinberg (2020), MNRAS, 498, 1364
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:
	__all__ = ["test"]
	from ._presets import *
	from .tests import test
	__all__.extend(_presets.__all__)
else:
	pass

