r"""
Leung & Nomoto (2018), ApJ, 861, 143 Type Ia supernova (SN Ia) yields

**Signature**: from vice.yields.sneia import leung2018

Importing this module will automatically set the SN Ia yield settings for all
elements to the delay-time distribution integrated yields calculated with the
Leung & Nomoto (2018) yield table under the 300-1-c3-1 explosion model. This 
study reports yields for near-Chandrasekhar Mass progenitors (1.3-1.38 
:math:`M_\odot`) with a variety of initial metallicities.

We provide type Ia supernova yields from the Leung & Nomoto (2018) study under
the following explosion models presented in their journal publication:

	- 300-0-C3-1
	- 300-1-C3-1
	- 300-3-C3-1
	- 300-5-C3-1

These models are named for the initial central density, the metallicity of the
progenitor relative to solar, the flame shape, and the initial carbon-to-oxygen
ratio, in that order. For example, the "300-1-C3-1" model refers to one with a 
central density of :math:`\rho_C=3\times10^9\,{\rm g}\,{\rm cm}^3`, a 
metallicity of :math:`Z_\odot`, a c3 flame, and a C/O ratio of 1.

.. tip:: By importing this module, the user does not sacrifice the ability to
	specify their yield settings directly.

.. note:: This module is not imported with a simple ``import vice`` statement.

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
		Leung & Nomoto (2018) [1]_ data.

		**Signature**: vice.yields.sneia.leung18.set_params(\*\*kwargs)

		Parameters
		----------
		kwargs : varying types
			Keyword arguments to pass to vice.yields.sneia.fractional.

		Raises
		------
		* TypeError
			- 	Received a keyword argument "study". This will always be
				"leung18" when called from this module.

		Other exceptions are raised by vice.yields.sneia.fractional.

		Notes
		-----
		We provide type Ia supernova yields from the Iwamoto et al. (1999)
		study under the following explosion models presented in their
		journal publication:

			- 300-0-C3-1
			- 300-1-C3-1
			- 300-3-C3-1
			- 300-5-C3-1

		Example Code
		------------
		>>> import vice
		>>> from vice.yields.sneia import iwamoto99
		>>> vice.yields.sneia.settings['fe']
		0.001705352
		>>> iwamoto99.set_params(n = 1.5e-3)
		>>> vice.yields.sneia.settings['fe']
		0.00116274
		>>> iwamoto99.set_params(n = 1.8e-3, model = "CDD1")
		>>> vice.yields.sneia.settings['fe']
		0.0011663333999999998
		>>> iwamoto99.set_params(model = "cdd2")
		>>> vice.yields.sneia.settings['fe']
		0.001835812

		.. seealso::
			- vice.yields.sneia.fractional
			- vice.yields.sneia.single

		.. [1] Leung & Nomoto (2018), ApJ, 861, 143
		"""
		if "study" in kwargs.keys():
			raise TypeError("Got an unexpected keyword argument 'study'.")
		else:
			# Override the default, which is for Seitenzahl et al. (2013) yields
			if "model" not in kwargs.keys(): kwargs["model"] = "300-1-C3-1"
			for i in _RECOGNIZED_ELEMENTS_:
				__settings[i] = __fractional(i, study = "leung18", **kwargs)

	if not __VICE_DOCS__: set_params(model = "300-1-C3-1")

else:
	pass

