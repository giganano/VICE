r"""
Gronow et al. (2021a, b) Type Ia supernova (SN Ia) yields

**Signature**: from vice.yields.sneia import gronow21

.. versionadded:: 1.3.0

Importing this module will automatically set the SN Ia yield settings for all
elements to the delay-time distribution integrated yields calculated with the
Gronow et al. (2021a, b) [1]_ [2]_ yield tables under the M10_10_1 progenitor
model. These studies reports yields for double detonations of sub-Chandrasekhar
mass (1.4 :math:`M_\odot`) white dwarfs at various progenitor metallicities,
with the solar metallicity yields published in Gronow et al. (2021a) and those
for remaining metallicities (:math:`Z / Z_\odot` = 0.01, 0.1, and 3) in Gronow
et al. (2021b).

We provide type Ia supernova yields from the Gronow et al. (2021a, b) studies
under the following explosion models presented in their journal publications:

	- M08_03_001, M08_03_01, M08_03_1, M08_03_3
	- M08_05_001, M08_05_01, M08_05_1, M08_05_3
	- M08_10_001, M08_10_01, M08_10_1, M08_10_3
	- M09_03_001, M09_03_01, M09_03_1, M09_03_3
	- M09_05_001, M09_05_01, M09_05_1, M09_05_3
	- M09_10_001, M09_10_01, M09_10_1, M09_10_3
	- M10_02_001, M10_02_01, M10_02_1, M10_02_3
	- M10_03_001, M10_03_01, M10_03_1, M10_03_3
	- M10_05_001, M10_05_01, M10_05_1, M10_05_3
	- M10_10_001, M10_10_01, M10_10_1, M10_10_3
	- M11_05_001, M11_05_01, M11_05_1, M11_05_3

These models are named for the mass of the carbon-oxygen core, the mass of the
helium shell, and the metallicity of the progenitor relative to solar, in that
order. For example, the "M09_05_01" model refers to one with a 0.9 
:math:`M_\odot` carbon-oxygen core and a 0.05 :math:`M_\odot` helium shell
produced by a star that was initially at a metallicity of 0.1 :math:`Z_\odot`.

.. tip:: By importing this module, the user does not sacrifice the ability to
	specify their yield settings directly.

.. note:: This module is not imported with a simple ``import vice`` statement.

Contents
--------
set_params : <function>
	Update the parameters with which the yields are calculated.

.. [1] Gronow et al. (2021a), A&A, 649, 155
.. [2] Gronow et al. (2021b), arxiv:2103.14050
"""

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
		Gronow et al. (2021a, b) [1]_ [2]_ data.

		**Signature**: vice.yields.sneia.gronow21.set_params(\*\*kwargs)

		Parameters
		----------
		kwargs : varying types
			Keyword arguments to pass to vice.yields.sneia.fractional.

		Raises
		------
		* TypeError
			-	Received a keyword argument "study". This will always be
				"gronow21" when called from this module.

		Other exceptions are raised by vice.yields.sneia.fractional.

		.. seealso:: vice.yields.sneia.fractional

		Notes
		-----
		We provide type Ia supernova yields from the Gronow et al. (2021a, b)
		studies under the following explosion models presented in their journal
		publications:

			- M08_03_001, M08_03_01, M08_03_1, M08_03_3
			- M08_05_001, M08_05_01, M08_05_1, M08_05_3
			- M08_10_001, M08_10_01, M08_10_1, M08_10_3
			- M09_03_001, M09_03_01, M09_03_1, M09_03_3
			- M09_05_001, M09_05_01, M09_05_1, M09_05_3
			- M09_10_001, M09_10_01, M09_10_1, M09_10_3
			- M10_02_001, M10_02_01, M10_02_1, M10_02_3
			- M10_03_001, M10_03_01, M10_03_1, M10_03_3
			- M10_05_001, M10_05_01, M10_05_1, M10_05_3
			- M10_10_001, M10_10_01, M10_10_1, M10_10_3
			- M11_05_001, M11_05_01, M11_05_1, M11_05_3

		These models are named for the mass of the carbon-oxygen core, the mass
		of the helium shell, and the metallicity of the progenitor relative to
		solar, in that order. For example, the "M09_05_01" model refers to one
		with a 0.9 :math:`M_\odot` carbon-oxygen core and a 0.05 :math:`M_\odot`
		helium shell produced by a star that was initially at a metallicity of
		0.1 :math:`Z_\odot`.

		Example Code
		------------
		>>> import vice
		>>> from vice.yields.sneia import gronow21
		>>> vice.yields.sneia.settings['fe']
		0.0017619157670400003
		>>> gronow21.set_params(n = 1.5e-3)
		>>> vice.yields.sneia.settings['fe']
		0.0012013062048000002
		>>> gronow21.set_params(n = 1.8e-3, model = "M09_10_001")
		>>> vice.yields.sneia.settings['fe']
		0.0009757080218934002
		>>> gronow21.set_params(model = "M11_05_01")
		>>> vice.yields.sneia.settings['fe']
		0.0019527508063624003

		.. seealso::
			- vice.yields.sneia.fractional
			- vice.yields.sneia.single 				

		.. [1] Gronow et al. (2021a), A&A, 649, 155
		.. [2] Gronow et al. (2021b), arxiv:2103.14050
		"""
		if "study" in kwargs.keys():
			raise TypeError("Got an unexpected keyword argument: 'study'")
		else:
			# Override the default, which is for Seitenzahl et al. (2013) yields
			if "model" not in kwargs.keys(): kwargs["model"] = "M10_10_1"
			for i in _RECOGNIZED_ELEMENTS_:
				__settings[i] = __fractional(i, study = "gronow21", **kwargs)

	if not __VICE_DOCS__: set_params(model = "M10_10_1")

else:
	pass

