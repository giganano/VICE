r"""
Sukhbold et al. (2016), ApJ, 821, 38 W18 Engine with Forced Explosions

**Signature**: from vice.yields.ccsne.S16 import W18F

.. versionadded:: 1.2.0

Importing this module will automatically set the CCSN yield settings for all
elements to the IMF-averaged yields calculated with the Sukhbold et al. (2016)
yield table under the W18F explosion engine for [M/H] = 0 stars. This will
adopt an upper mass limit of 120 :math:`M_\odot`.

We provide core collapse supernova yields for non-rotating progenitors at
solar metallicity only as reported by Sukhbold et al. (2016) under the
W18F explosion engine.

For details on the nature of the forced explosion model, see discussion in
Griffith et al. (2021) [1]_.

.. tip:: By importing this module the user does not sacrifice the ability to
	specify their yield settings directly.

.. note:: This module is not imported with a simple ``import vice`` statement.

.. note:: When this module is imported, the yields will be updated with a
	maximum of 10^5 bins in quadrature to decrease computational overhead. For
	some elements, the yield calculation may not converge. To rerun the yield
	calculation with higher numerical precision, simply call ``set_params``
	with a new value for the keyword ``Nmax`` (see below).

Contents
--------
set_params : <function>
	Update the parameters with which the yields are calculated.

.. [1] Griffith et al. (2021), arxiv:2103.09837
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False
try:
	__VICE_DOCS__
except NameError:
	__VICE_DOCS__ = False

if not __VICE_SETUP__:

	__all__ = ["set_params", "test"]
	from ....._globals import _RECOGNIZED_ELEMENTS_
	from ... import fractional as __fractional
	from ... import settings as __settings
	from .tests import test

	def set_params(**kwargs):
		r"""
		Update the parameters with which the yields are calculated from the
		Sukhbold et al. (2016) [1]_ W18F explosion engine data.

		**Signature**: vice.yields.ccsne.S16.W18F.set_params(\*\*kwargs)

		Parameters
		----------
		kwargs : varying types
			Keyword arguments to pass to vice.yields.ccsne.fractional.

		Raises
		------
		* TypeError
			- 	Received a keyword argument "study". This will always be
				"S16/W18F" when called from this module.

		Other exceptions are raised by vice.yields.ccsne.fractional.

		Notes
		-----
		We provide core collapse supernova yields for non-rotating progenitors
		at solar metallicity only as reported by Sukhbold et al. (2016) under
		the W18F explosion engine.

		Example Code
		------------
		>>> import vice
		>>> from vice.yields.ccsne.S16 import W18F
		>>> vice.yields.ccsne.settings['o']
		0.018063484040223107
		>>> W18F.set_params(IMF = "salpeter")
		>>> vice.yields.ccsne.settings['o']
		0.010770572437600351
		>>> W18F.set_params(IMF = "salpeter", m_upper = 80)
		>>> vice.yields.ccsne.settings['o']
		0.010523432438733342
		>>> from vice.yields.ccsne.engines import E16
		>>> from vice.yields.ccsne.engines.S16 import W20
		>>> # Ertl et al. (2016) black hole landscape with W18F yields
		... W18F.set_params(explodability = E16)
		>>> vice.yields.ccsne.settings['o']
		0.0044613656957736055
		>>> # Sukhbold et al. (2016) W20 black hole landscape with W18F yields
		... W18F.set_params(explodability = W20)
		>>> vice.yields.ccsne.settings['o']
		0.0034641626751717044

		.. seealso:: vice.yields.ccsne.fractional

		.. [1] Sukhbold et al. (2016), ApJ, 821, 38
		"""
		if "study" in kwargs.keys():
			raise TypeError("Got an unexpected keyword argument: 'study'")
		else:
			for i in _RECOGNIZED_ELEMENTS_:
				__settings[i] = __fractional(i, study = "S16/W18F", **kwargs)[0]

	if not __VICE_DOCS__: set_params(m_upper = 120, Nmax = 1e5)

else:
	pass

