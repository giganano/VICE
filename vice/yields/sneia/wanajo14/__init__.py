r"""
Wanajo et al. (2014), ApJL, 789, 2 binary neutron star (BNS) merger yields.

**Signature**: from vice.yields.sneia import wanajo14

Importing this module will set the SN Ia yield settings for all elements to
the integrated **r**-process yields calculated with the Wanajo et al. (2014) 
yield table for BNS mergers. This study reports the yields for the merger of
two 1.3 :math:`M_\odot` neutron stars.

.. tip:: By importing this module, the user does not sacrifice the ability to
	specify their yield settings directly.

.. note:: VICE does not currently support separate SN Ia and BNS merger
	channels. By importing this module, **all** SN Ia yields will be over-
	written by the BNS **r**-process yields. Users who wish to compare element
	ratios between the two sources (e.g., [Eu/Fe]) must run two separate
	models, one with the desired SN Ia yields and the second with these yields.

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
		Wanajo et al. (2014) [1]_ data.

		**Signature**: vice.yields.sneia.leung18.set_params(\*\*kwargs)

		Parameters
		----------
		kwargs : varying types
			Keyword arguments to pass to vice.yields.sneia.fractional.

		Raises
		------
		* TypeError
			- 	Received a keyword argument "study". This will always be
				"wanajo14" when called from this module.

		Other exceptions are raised by vice.yields.sneia.fractional.

		Notes
		-----
		VICE does not currently support separate SN Ia and BNS merger
		channels. By importing this module, **all** SN Ia yields will be over-
		written by the BNS **r**-process yields. Users who wish to compare 
		element ratios between the two sources (e.g., [Eu/Fe]) must run two 
		separate models, one with the desired SN Ia yields and the second with 
		these yields.

		Only one model is provided by Wanajo et al. (2014), labeled here as:
		
			- NS1.3-NS1.3

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

		.. [1] Wanajo et al. (2014), ApJL, 789, L39
		"""
		if "study" in kwargs.keys():
			raise TypeError("Got an unexpected keyword argument 'study'.")
		else:
			# Override the default, which is for Seitenzahl et al. (2013) yields
			if "model" not in kwargs.keys(): kwargs["model"] = "NS1.3-NS1.3"
			# Override the default production efficiency, which is for SNe Ia
			if "n" not in kwargs.keys(): kwargs["n"] = 1e-5
			for i in _RECOGNIZED_ELEMENTS_:
				__settings[i] = __fractional(i, study = "wanajo14", **kwargs)

	if not __VICE_DOCS__: set_params(model = "NS1.3-NS1.3")

else:
	pass

