r"""
Type Ia Supernovae (SNe Ia) Nucleosynthetic Yield Tools

Calculate IMF-averaged yields and modify yield settings for use in simulations.
This package provides tables from the following nucleosynthetic yield studies:

	- Seitenzahl et al. (2013) [1]_
	- Iwamoto et al. (1999) [2]_
	- Gronow et al. (2021a, b) [3]_ [4]_

Contents
--------
fractional : <function>
	Calculate an IMF-averaged yield for a given element.
single : <function>
	Look up the mass yield of a given element from a single type Ia supernova
	from a specified study.
settings : dataframe
	Stores current settings for these yields.
gronow21 : yield preset
	Sets the yields according to one of the models published in the Gronow et
	al. (2021a, b) studies.
seitenzahl13 : yield preset
	Sets the yields according to one of the models published in the Seitenzahl
	et al. (2013) study.
iwamoto99 : yield preset
	Sets the yields according to one of the models published in the Iwamoto et
	al. (1999) study.

.. versionadded:: 1.3.0
	The "gronow21" yield model was introduced in version 1.3.0.

Notes
-----
The data stored in this module are reported for each corresponding study
*as published*. The Seitenzahl et al. (2013) and Gronow et al. (2021a, b)
models reported mass yields after complete decay of all radioactive nuclides
with half-lives less than 2 Gyr, and the Iwamoto et al. (1999) study fully
decayed *all* unstable isotopes; any additional treatment for radioactive
isotopes is thus unnecessary.

.. [1] Seitenzahl et al. (2013), MNRAS, 429, 1156
.. [2] Iwamoto et al. (1999), ApJ, 124, 439
.. [3] Gronow et al. (2021a), A&A, 649, 155
.. [4] Gronow et al. (2021b), arxiv:2103.14050
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:
	__all__ = ["single", "fractional", "settings", "test"]
	__all__ = [str(i) for i in __all__] 	# appease python 2 strings

	from ._yield_lookup import single_detonation as single
	from ._yield_lookup import integrated_yield as fractional
	from .settings import settings
	from .tests import test

else:
	pass

