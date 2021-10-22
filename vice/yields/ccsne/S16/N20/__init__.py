r"""
Sukhbold et al. (2016), ApJ, 821, 38 N20 Explosion Engine

**Signature**: from vice.yields.ccsne.S16 import N20

.. versionadded:: 1.2.0

Importing this module will automatically set the CCSN yield settings for all
elements to the IMF-averaged yields calculated with the Sukhbold et al. (2016)
yield table under the N20 explosion engine for [M/H] = 0 stars. This will
adopt an upper mass limit of 120 :math:`M_\odot`.

We provide core collapse supernova yields for non-rotating progenitors at
solar metallicity only as reported by Sukhbold et al. (2016) under the
N20 explosion engine.

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
		Sukhbold et al. (2016) [1]_ N20 explosion engine data.

		**Signature**: vice.yields.ccsne.S16.N20.set_params(\*\*kwargs)

		Parameters
		----------
		kwargs : varying types
			Keyword arguments to pass to vice.yields.ccsne.fractional.

		Raises
		------
		* TypeError
			- 	Received a keyword argument "study". This will always be
				"S16/N20" when called from this module.

		Other exceptions are raised by vice.yields.ccsne.fractional.

		Notes
		-----
		We provide core collapse supernova yields for non-rotating progenitors
		at solar metallicity only as reported by Sukhbold et al. (2016) under
		the N20 explosion engine.

		Example Code
		------------
		>>> import vice
		>>> from vice.yields.ccsne.S16 import N20
		>>> vice.yields.ccsne.settings['o']
		0.007286488814947039
		>>> N20.set_params(IMF = "salpeter")
		>>> vice.yields.ccsne.settings['o']
		0.004247585262396765
		>>> N20.set_params(IMF = "salpeter", m_upper = 80)
		>>> vice.yields.ccsne.settings['o']
		0.003960345954142228

		.. seealso:: vice.yields.ccsne.fractional

		.. [1] Sukhbold et al. (2016), ApJ, 821, 38
		"""
		if "study" in kwargs.keys():
			raise TypeError("Got an unexpected keyword argument: 'study'")
		else:
			for i in _RECOGNIZED_ELEMENTS_:
				__settings[i] = __fractional(i, study = "S16/N20", **kwargs)[0]

	if not __VICE_DOCS__: set_params(m_upper = 120, Nmax = 1e5)

else:
	pass

