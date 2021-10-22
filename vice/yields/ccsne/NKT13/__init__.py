r"""
Nomoto, Kobayashi & Tominaga (2013), ARA&A, 51, 457 core collapse supernova
yields

**Signature**: from vice.yields.ccsne import NKT13

.. versionadded:: 1.2.0

Importing this module will automatically set the CCSN yield settings for all
elements to the IMF-averaged yields calculated with the Nomoto, Kobayashi &
Tominaga (2013) yield table for [M/H] = 0.15 stars. This will adopt an upper
mass limit of 40 :math:`M_\odot`.

We provide core collapse supernova yields for non-rotating progenitors as
reported Nomoto, Kobayashi & Tominaga (2013) at metallicities relative to
solar of :math:`\log_{10}(Z / Z_\odot)` =

	- -inf
	- -1.15
	- -0.54
	- -0.24
	- 0.15
	- 0.55

assuming :math:`Z_\odot` = 0.014 according to Asplund et al. (2009) [1]_.

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
	Update the parameters with which the yields are calcualted.

.. [1] Asplund et al. (2009), ARA&A, 47, 481
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
		Nomoto, Kobayashi & Tominaga (2013) [1]_ data.

		**Signature**: vice.yields.ccsne.NKT13.set_params(\*\*kwargs)

		Parameters
		----------
		kwargs : varying types
			Keyword arguments to pass to vice.yields.ccsne.fractional.

		Raises
		------
		* TypeError
			- 	Received a keyword argument "study". This will always be
				"NKT13" when called from this module.

		Other exceptions are raised by vice.yields.ccsne.fractional.

		Notes
		-----
		We provide core collapse supernova yields for non-rotating progenitors
		as reported Nomoto, Kobayashi & Tominaga (2013) at metallicities
		relative to solar of :math:`\log_{10}(Z / Z_\odot)` =

			- -inf
			- -1.15
			- -0.54
			- -0.24
			- 0.15
			- 0.55

		assuming :math:`Z_\odot` = 0.014 according to Asplund et al.
		(2009) [2]_.

		Example Code
		------------
		>>> import vice
		>>> from vice.yields.ccsne import NKT13
		>>> vice.yields.ccsne.settings['o']
		0.00849047694119129
		>>> NKT13.set_params(MoverH = 0.55)
		>>> vice.yields.ccsne.settings['o']
		0.020692018117088606
		>>> NKT13.set_params(IMF = "salpeter")
		>>> vice.yields.ccsne.settings['o']
		0.013645466478054947
		>>> NKT13.set_params(IMF = "salpeter", MoverH = -1.15)
		>>> vice.yields.ccsne.settings['o']
		0.015010918224009764
		>>> from vice.yields.ccsne.engines.S16 import W18
		>>> from vice.yields.ccsne.engines import E16
		>>> # Sukhbold et al. (2016) W18 black hole landscape with NKT13 yields
		... NKT13.set_params(explodability = W18)
		>>> vice.yields.ccsne.settings['o']
		0.003980895857851888
		>>> # Ertl et al. (2016) black hole landscape with NKT13 yields
		... NKT13.set_params(explodability = E16, MoverH = -1.15)
		>>> vice.yields.ccsne.settings['o']
		0.0023433951760400543

		.. seealso:: vice.yields.ccsne.fractional

		.. [1] Nomoto, Kobayashi & Tominaga (2013), ARA&A, 51, 457
		.. [2] Asplund et al. (2009), ARA&A, 47, 481
		"""
		if "study" in kwargs.keys():
			raise TypeError("Got an unexpected keyword argument: 'study'")
		else:
			if "MoverH" not in kwargs.keys():
				# fractional will default to 0, override this
				kwargs["MoverH"] = 0.15
			else:
				pass
			for i in _RECOGNIZED_ELEMENTS_:
				__settings[i] = __fractional(i, study = "NKT13", **kwargs)[0]

	if not __VICE_DOCS__: set_params(m_upper = 40, MoverH = 0.15, Nmax = 1e5)

else:
	pass

