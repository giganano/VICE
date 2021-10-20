r"""
Sukhbold et al. (2016), ApJ, 821, 38 core collapse supernova yields

**Signature**: from vice.yields.ccsne import S16

.. versionadded:: 1.2.0

This yield module provides a number of sub-modules with which to update CCSN
yield settings according to the Sukhbold et al. (2016) study. This module,
however, does not import them as doing so would update the yields
multiple times. Users should instead import one of the modules listed below
under `Contents`_.

.. tip:: By importing this module or any of its sub-modules, the user does not
	sacrifice the ability to specify their yield settings directly.

.. note:: This module is not imported with a simple ``import vice`` statement.

Contents
--------
N20 : module
	Sets yields according to the N20 explosion engine.
W18 : module
	Sets yields according to the W18 explosion engine.
W18F : module
	Sets yields according to the W18 engine with forced explosions.

For details on the W18F engine, see discussion in Griffith et al. (2021) [1]_.

.. [1] Griffith et al. (2021), arxiv:2103.09837
"""

pass

