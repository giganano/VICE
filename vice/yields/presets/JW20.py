r"""
Johnson & Weinberg (2020), MNRAS, 498, 1364 Nucleosynthetic Yield Settings

**Signature**: from vice.yields.presets import JW20

.. versionadded:: 1.1.0

Importing this module sets the yields of oxygen, iron, and strontium to that
adopted in the Johnson & Weinberg (2020) paper on starburst scenarios.

.. note:: This module is not imported with a simple "import vice" statement.

CCSNe
-----
* :math:`y_\text{O}^\text{CC}` = 0.015
* :math:`y_\text{Fe}^\text{CC}` = 0.0012
* :math:`y_\text{Sr}^\text{CC} = 3.5\times10^{-8}`

SNe Ia
------
* :math:`y_\text{O}^\text{Ia}` = 0
* :math:`y_\text{Fe}^\text{Ia}` = 0.0017
* :math:`y_\text{Sr}^\text{Ia}` = 0

AGB
---
All three elements described by the Cristallo et al. (2011) [1]_ yields.

Other Contents
--------------
alt_cc_sr_linear : <function>
	The functional form of the alternative CCSN Sr yield which is linear in
	metallicity :math:`Z`.
alt_cc_sr_limitexp : <function>
	The functional form of the alternative CCSN Sr yield which is a limited
	exponential in metallicity :math:`Z`.

.. [1] Cristallo et al. (2011), ApJS, 197, 17
"""

__all__ = ["alt_cc_sr_linear", "alt_cc_sr_limitexp"]
import math
import vice
if tuple(vice.version)[:3] >= (1, 1, 0):
	for i in ["o", "fe", "sr"]: vice.yields.agb.settings[i] = "cristallo11"
else: pass
try:
	__VICE_DOCS__
except NameError:
	__VICE_DOCS__ = False

if not __VICE_DOCS__:
	vice.yields.ccsne.settings["o"] = 0.015
	vice.yields.ccsne.settings["fe"] = 0.0012
	vice.yields.ccsne.settings["sr"] = 3.5e-8
	vice.yields.sneia.settings["o"] = 0.0
	vice.yields.sneia.settings["fe"] = 0.0017
	vice.yields.sneia.settings["sr"] = 0.0
else: pass


def alt_cc_sr_linear(Z, Z_solar = 0.014):
	r"""
	The functional form of the alternative CCSN Sr yield explored in Johnson &
	Weinberg (2020) [1]_ which is linear in metallicity :math:`Z`.

	**Signature**: vice.yields.presets.JW20.alt_cc_sr_linear(Z, Z_solar = 0.014)

	.. versionadded:: 1.1.0

	Parameters
	----------
	Z : real number
		The metallicity by mass :math:`M_Z/M_\star`.
	Z_solar : real number [default : 0.014]
		The metallicity by mass of the Sun. Default value is take from
		Asplund et al. (2009) [2]_.

	Returns
	-------
	y : real number
		The IMF-averaged CCSN Sr yield as a function of metallicity Z.

	Notes
	-----
	The yield is defined by:

	.. math:: y_\text{Sr}^\text{CC} = 3.5\times10^{-8}
		\left(\frac{Z}{Z_\odot}\right)

	Example Code
	------------
	>>> import vice
	>>> from vice.yields.presets import JW20
	>>> vice.yields.ccsne.settings['sr'] = JW20.alt_cc_sr_linear
	>>> modified = lambda z: JW20.alt_cc_sr_linear(z, Z_solar = 0.018)
	>>> vice.yields.ccsne.settings['sr'] = modified

	.. [1] Johnson & Weinberg (2020), MNRAS, 498, 1364
	.. [2] Asplund et al. (2009), ARA&A, 47, 481
	"""
	return 3.5e-08 * (Z / Z_solar)


def alt_cc_sr_limitexp(Z, Z_solar = 0.014):
	r"""
	The functional form of the alternative CCSN Sr yield explored in Johnson &
	Weinberg (2020) [1]_ which is a limited exponential in :math:`Z`.

	**Signature**: vice.yields.presets.JW20.alt_cc_sr_limitexp(Z,
	Z_solar = 0.014)

	.. versionadded:: 1.1.0

	Parameters
	----------
	Z : real number
		The metallicity by mass :math:`M_Z/M_\star`.
	Z_solar : real number [default : 0.014]
		The metallicity by mass of the Sun. Default value is take from
		Asplund et al. (2009) [2]_.

	Returns
	-------
	y : real number
		The IMF-averaged CCSN Sr yield as a function of metallicity Z.

	Notes
	-----
	The yield is defined by:

	.. math:: y_\text{Sr}^\text{CC} = 10^{-7}
		\left[1 - e^{-10(Z/Z_\odot)}\right]

	Example Code
	------------
	>>> import vice
	>>> from vice.yields.presets import JW20
	>>> vice.yields.ccsne.settings['sr'] = JW20.alt_cc_sr_limitexp
	>>> modified = lambda z: JW20.alt_cc_sr_limitexp(z, Z_solar = 0.018)
	>>> vice.yields.ccsne.settings['sr'] = modified

	.. [1] Johnson & Weinberg (2020), MNRAS, 498, 1364
	.. [2] Asplund et al. (2009), ARA&A, 47, 481
	"""
	return 1.0e-07 * (1 - math.exp(-10 * (Z / Z_solar)))

