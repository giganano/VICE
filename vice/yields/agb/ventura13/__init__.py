r"""
Ventura et al. (2013, 2014, 2018, 2020) Asymptotic Giant Branch (AGB) Star
yields

**Signature**: from vice.yields.agb import ventura13

.. versionadded:: 1.3.0

Importing this module will set the AGB star yield settings for all elements
where yield tables are available to "ventura13".
AGB star yields will then be calculated using bi-linear interpolation in
progenitor mass and metallicity using these data to determine AGB star yields
in chemical evolution models.
This module combines yields from various Ventura et al. publications into one
yield table.
At the following metallicities, the yields are adopted from the associated
journal publication:

	- Z = 0.0003 : Ventura et al. (2013) [1]_
	- Z = 0.001 : Unpublished
	- Z = 0.002 : Unpublished
	- Z = 0.004 : Ventura et al. (2014) [2]_
	- Z = 0.008 : Ventura et al. (2013)
	- Z = 0.014 : Ventura et al. (2018) [3]_
	- Z = 0.04 : Ventura et al. (2020) [4]_

.. note:: This module is not imported with a simple ``import vice`` statement.

Raises
------
* ScienceWarning
	This module only provides tables for the following elements: he, c, n, o,
	ne, na, mg, al, si. The settings for other elements will not be modified.

.. [1] Ventura et al. (2013), MNRAS, 431, 3642
.. [2] Ventura et al. (2014), MNRAS, 437, 3274
.. [3] Ventura et al. (2018), MNRAS, 475, 2282
.. [4] Ventura et al. (2020), A&A, 641, A103
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

	from ...._globals import ScienceWarning
	from .._grid_reader import _VENTURA13_ELEMENTS_
	from .. import settings as __settings
	import warnings
	if not __VICE_DOCS__:
		for elem in _VENTURA13_ELEMENTS_: __settings[elem] = "ventura13"
	else: pass

	warnings.warn("""\
The Ventura et al. (2013, 2014, 2018, 2020) studies reported yields only for \
the following elements: %s. \
AGB star yield settings for other elements will not be modified.""" % (
		str(_VENTURA13_ELEMENTS_)), ScienceWarning)

else: pass

