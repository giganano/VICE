r"""
Limongi & Chieffi (2018), ApJS, 237, 13 core collapse supernova (CCSN) yields

**Signature**: from vice.yields.ccsne import LC18

Importing this module will automatically set the CCSN yield settings for all
elements to the IMF-averaged yields calculated with the Limongi & Chieffi
(2018) yield table for [M/H] = 0 stars. This will adopt an upper mass limit of
100 :math:`M_\odot`.

We provide core collapse supernova yields for progenitors at rotational
velocities of 0, 150, and 300 km/s as reported by Limongi & Chieffi (2018) at
metallicities relative to solar of :math:`\log_{10}(Z / Z_\odot)` =

	- -3
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
	Update the parameters with which the yields are calculated
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
		Limongi & Chieffi (2018) [1]_ data.

		**Signature**: vice.yields.ccsne.LC18.set_params(\*\*kwargs)

		Parameters
		----------
		kwargs : varying types
			Keyword arguments to pass to vice.yields.ccsne.fractional.

		Raises
		------
		* TypeError
			- 	Received a keyword argument "study". This will always be "LC18"
				when called from this module.

		Other exceptions are raised by vice.yields.ccsne.fractional.

		Notes
		-----
		We provide core collapse supernova yields for progenitors at rotational
		velocities of 0, 150, and 300 km/s as reported by Limongi & Chieffi
		(2018) at metallicities relative to solar of
		:math:`\log_{10}(Z / Z_\odot)` =

			- -3
			- -2
			- -1
			- 0

		Example Code
		------------
		>>> import vice
		>>> from vice.yields.ccsne import LC18
		>>> vice.yields.ccsne.settings['o']
		0.0036512768277795864
		>>> LC18.set_params(IMF = "salpeter")
		>>> vice.yields.ccsne.settings['o']
		0.0022556257770960713
		>>> LC18.set_params(rotation = 150)
		>>> vice.yields.ccsne.settings['o']
		0.010851696623329273
		>>> LC18.set_params(rotation = 150, IMF = "salpeter")
		>>> vice.yields.ccsne.settings['o']
		0.006744726174198793
		>>> LC18.set_params(rotation = 150, IMF = "salpeter", MoverH = -2)
		>>> vice.yields.ccsne.settings['o']
		0.0081235534350932

		.. seealso:: vice.yields.ccsne.fractional

		.. [1] Limongi & Chieffi (2018), ApJS, 237, 17
		"""
		if "study" in kwargs.keys():
			raise TypeError("Got an unexpected keyword argument: 'study'")
		else:
			for i in range(len(_RECOGNIZED_ELEMENTS_)):
				__settings[_RECOGNIZED_ELEMENTS_[i]] = __fractional(
					_RECOGNIZED_ELEMENTS_[i], study = "LC18", **kwargs)[0]

	if not __VICE_DOCS__: set_params(Nmax = 1e5)

else: pass

