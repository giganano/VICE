r"""
Karakas & Lugaro (2016), Karakas et al. (2018) Asymptotic Giant Branch (AGB)
star yields

**Signature**: from vice.yields.agb import karakas16

.. versionadded:: 1.3.0

Importing this module will set the AGB star yield setting for all elements to
"karakas16". This module combines the yields for :math:`Z` = 0.007, 0.014, and
0.03 progenitors from Karakas & Lugaro (2016) [1]_ with the yields for
:math:`Z` = 0.0028 progenitors from Karakas et al. (2018) [2]_ (a metallicity
characteristic of stars in the Small Magellanic Cloud).
AGB star yields will then be calculated using bi-linear interpolation in
progenitor mass and metallicity using these data to determine AGB star yields
in chemical evolution models.

.. note:: This module is not imported with a simple ``import vice`` statement.

.. [1] Karakas & Lugaro (2016), ApJ, 825, 26
.. [2] Karakas et al. (2018), MNRAS, 477, 421
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
		for i in __settings.keys(): __settings[i] = "karakas16"
	else: pass

else: pass

