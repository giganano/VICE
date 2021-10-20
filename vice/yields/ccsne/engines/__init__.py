r"""
Core collapse supernova explosion engines: explodability as a function of
progenitor mass in solar masses.

**Signature**: from vice.yields.ccsne import engines

.. versionadded:: 1.2.0

.. tip:: Instances of the ``engine`` class can be passed as the keyword
	argument ``explodability`` to ``vice.yields.ccsne.fractional`` to calculate
	IMF-averaged yields assuming a particular black hole landscape. The impact
	of these assumptions is explored in Griffith et al. (2021) [1]_.

Contents
--------
engine : ``type``
	The base class implemented in this module.
cutoff : ``engine``
	An engine characterized by a threshold mass, below which stars explode as
	CCSNe, and above which stars collapse directly to a black hole.
E16 : ``engine``
	An engine implementing the Ertl et al. (2016) [2]_ model, characterized
	by the two parameters :math:`M_4` and :math:`\mu_4`.
S16 : ``module``
	Explodability maps as reported by the various models in Sukhbold et al.
	(2016) [3]_.

.. [1] Griffith et al. (2021), arxiv:2103.09837
.. [2] Ertl et al. (2016), ApJ, 818, 124
.. [3] Sukhbold et al. (2016), ApJ, 821, 38
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["cutoff", "engine", "E16", "S16", "test"]
	from ....testing import moduletest
	from .cutoff import cutoff
	from .engine import engine
	from .E16 import E16
	from . import S16
	from . import tests

	# Instances of derived classes rather than derived classes themselves
	E16 = E16()
	cutoff = cutoff()

	@moduletest
	def test():
		r"""
		vice.yields.ccsne.engines module test
		"""
		return ["vice.yields.ccsne.engines",
			[
				tests.engine.test(run = False),
				tests.cutoff.test(run = False),
				tests.E16.test(run = False),
				tests.usage.test(run = False),
				S16.test(run = False)
			]
		]

else: pass

