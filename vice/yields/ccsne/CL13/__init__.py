r"""
Chieffi & Limongi (2013), ApJ, 764, 21 core collapse supernova (CCSN) yields

**Signature**: from vice.yields.ccsne import CL13

Importing this module will automatically set the CCSN yield settings for all
elements to the IMF-averaged yields calculated with the Chieffi & Limongi
(2013) yield table for [M/H] = 0 stars. This will adopt an upper mass limit of
100 :math:`M_\odot`.

We provide core collapse supernova yields for progenitors at rotational
velocities of 0 and 300 km/s as reported by Chieffi & Limongi (2013) at solar
metallicity.

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
		Chieffi & Limongi (2013) [1]_ data.

		**Signature**: vice.yields.ccsne.CL13.set_params(\*\*kwargs)

		Parameters
		----------
		kwargs : varying types
			Keyword arguments to pass to vice.yields.ccsne.fractional.

		Raises
		------
		* TypeError
			- 	Received a keyword argument "study". This will always be "CL13"
				when called from this module.

		Other exceptions are raised by vice.yields.ccsne.fractional.

		Notes
		-----
		We provide core collapse supernova yields for progenitors at rotational
		velocities of 0 and 300 km/s as reported by Chieffi & Limongi (2013) at
		solar metallicity.

		Example Code
		------------
		>>> import vice
		>>> from vice.yields.ccsne import CL13
		>>> vice.yields.ccsne.settings['o']
		0.01559740936489062
		>>> CL13.set_params(IMF = "salpeter")
		>>> vice.yields.ccsne.settings['o']
		0.009261587578694157
		>>> CL13.set_params(rotation = 300)
		>>> vice.yields.ccsne.settings['o']
		0.024372870613029975
		>>> CL13.set_params(rotation = 300, IMF = "salpeter")
		>>> vice.yields.ccsne.settings['o']
		0.014655521027938309
		>>> from vice.yields.ccsne.engines.S16 import W18
		>>> from vice.yields.ccsne.engines import E16
		>>> # Sukhbold et al. (2016) W18 black hole landscape with CL13 yields
		... CL13.set_params(explodability = W18)
		>>> vice.yields.ccsne.settings['o']
		0.0029448935889672184
		>>> # Ertl et al. (2016) black hole landscape with CL13 yields
		... CL13.set_params(explodability = E16, rotation = 300)
		>>> vice.yields.ccsne.settings['o']
		0.005392906178396455

		.. seealso:: vice.yields.ccsne.fractional

		.. [1] Chieffi & Limongi (2013), ApJ, 764, 21
		"""
		if "study" in kwargs.keys():
			raise TypeError("Got an unexpected keyword argument: 'study'")
		else:
			for i in range(len(_RECOGNIZED_ELEMENTS_)):
				__settings[_RECOGNIZED_ELEMENTS_[i]] = __fractional(
					_RECOGNIZED_ELEMENTS_[i], study = "CL13", **kwargs)[0]

	if not __VICE_DOCS__: set_params(Nmax = 1e5)

else:
	pass

