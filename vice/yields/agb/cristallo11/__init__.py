r"""
Cristallo et al. (2011, 2015) Asymptotic Giant Branch (AGB) star yields.

**Signature**: from vice.yields.agb import cristallo11

Importing this module will set the AGB star yield settings for all elements
to "cristallo11", which combines the yields for 1 - 3 :math:`M_\odot` AGB
star progenitors from Cristallo et al. (2011) [1]_ with the yields for 4 - 6
:math:`M_\odot` progenitors from Cristallo et al. (2015) [2]_.
AGB star yields will then be calculated using bi-linear interpolation in
progenitor mass and metallicity using these data to determine AGB star yields
in chemical evolution models.

.. note:: This module is not imported with a simple ``import vice`` statement.

.. [1] Cristallo et al. (2011), ApJS, 197, 17
.. [2] Cristallo et al. (2015), ApJS, 219, 40
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

	from .. import settings as __settings
	if not __VICE_DOCS__:
		for i in __settings.keys():
			__settings[i] = "cristallo11"
	else: pass

else:
	pass

