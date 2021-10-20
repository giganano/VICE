r"""
Core collapse supernova explosion engines: explodability as a function of
progenitor mass in solar masses as reported by the Sukhbold et al. (2016) [1]_
models.

**Signature**: from vice.yields.ccsne.engines import S16

.. versionadded:: 1.2.0

.. tip:: Instances of the ``engine`` class can be passed the keyword argument
	``explodability`` to ``vice.yields.ccsne.fractional`` to calculate
	IMF-averaged yields assuming a particular black hole landscape. The impact
	of these assumptions is explored in Griffith et al. (2021) [2]_.

.. note:: For all explosion engines, progenitors with zero age main sequence
	masses between 9 and 12 :math:`M_\odot` proceed according to the Z9.6
	engine, while remaining masses explode or collapse according to the
	associated engine. (See: Section 2.2.2 of Sukhbold et al. 2016)

Contents
--------
N20 : ``engine``
	An engine characterized by the N20 explosion model.
S19p8 : ``engine``
	An engine characterized by the S19p8 explosion model.
W15 : ``engine``
	An engine characterized by the W15 explosion model.
W18 : ``engine``
	An engine characterized by the W18 explosion model.
W20 : ``engine``
	An engine characterized by the W20 explosion model.

.. [1] Sukhbold et al. (2016), ApJ, 821, 38
.. [2] Griffith et al. (2021), arxiv:2103.09837
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["N20", "S19p8", "W15", "W18", "W20", "test"]
	from .N20 import N20
	from .S19p8 import S19p8
	from .W15 import W15
	from .W18 import W18
	from .W20 import W20
	from .tests import test

	# Instances of derived classes rather than derived classes themselves
	N20 = N20()
	S19p8 = S19p8()
	W15 = W15()
	W18 = W18()
	W20 = W20()

else: pass

