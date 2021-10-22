r"""
Woosley & Weaver (1995), ApJ, 101, 181 core collapse supernova (CCSN) yields

**Signature**: from vice.yields.ccsne import WW95

Importing this module will automatically set the CCSN yield settings for all
elements to the IMF-averaged yields calculated with the Woosley & Weaver
(1995) yield table for [M/H] = 0 stars. This will adopt an upper mass limit
of 40 :math:`M_\odot`.

We provide core collapse supernova yields for non-rotating progenitors as
reported by Woosley & Weaver (1995) at metallicities relative to solar of
:math:`\log_{10}(Z / Z_\odot)` =

	- -inf
	- -4
	- -2
	- -1
	- 0

.. tip:: By importing this module, the user does not sacrifice the ability to
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
	from ...._globals import _RECOGNIZED_ELEMENTS_
	from .. import fractional as __fractional
	from .. import settings as __settings
	from .tests import test

	def set_params(**kwargs):
		r"""
		Update the parameters with which the yields are calculated from the
		Woosley & Weaver (1995) [1]_ data.

		**Signature**: vice.yields.ccsne.WW95.set_params(\*\*kwargs)

		Parameters
		----------
		kwargs : varying types
			Keyword arguments to pass to vice.yields.ccsne.fractional.

		Raises
		------
		* TypeError
			- 	Received a keyword argument "study". This will always be "WW95"
				when called from this module.

		Other exceptions are raised by vice.yields.ccsne.fractional.

		Notes
		-----
		We provide core collapse supernova yields for non-rotating progenitors
		as reported by Woosley & Weaver (1995) at metallicities relative to
		solar of :math:`\log_{10}(Z / Z_\odot)` =

			- -inf
			- -4
			- -2
			- -1
			- 0

		Example Code
		------------
		>>> import vice
		>>> from vice.yields.ccsne import WW95
		>>> vice.yields.ccsne.settings['o']
		0.011213287529967898
		>>> WW95.set_params(IMF = "salpeter")
		>>> vice.yields.ccsne.settings['o']
		0.01031925181253855
		>>> WW95.set_params(IMF = "salpeter", m_upper = 80)
		>>> vice.yields.ccsne.settings['o']
		0.009732682861255278
		>>> from vice.yields.ccsne.engines.S16 import W18
		>>> from vice.yields.ccsne.engines import E16
		>>> # Sukhbold et al. (2016) W18 black hole landscape with WW95 yields
		... WW95.set_params(explodability = W18)
		>>> vice.yields.ccsne.settings['o']
		0.004076427850896676
		>>> # Ertl et al. (2016) black hole landscape with WW95 yields
		... WW95.set_params(explodability = E16)
		>>> vice.yields.ccsne.settings['o']
		0.0026048168655224023

		.. seealso:: vice.yields.ccsne.fractional

		.. [1] Woosley & Weaver (1995), ApJ, 101, 181
		"""
		if "study" in kwargs.keys():
			raise TypeError("Got an unexpected keyword argument: 'study'")
		else:
			for i in _RECOGNIZED_ELEMENTS_:
				__settings[i] = __fractional(i, study = "WW95", **kwargs)[0]

	if not __VICE_DOCS__: set_params(m_upper = 40, Nmax = 1e5)

else:
	pass

