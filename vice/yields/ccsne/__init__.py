r"""
Core Collapse Supernovae (CCSNe) Nucleosynthetic Yield Tools

Calculate IMF-averaged yields and modify yield settings for use in simulations.
This package provides tables from the following nucleosynthetic yield studies:

	- Limongi & Chieffi (2018) [1]_
	- Sukhbold et al. (2016) [2]_
	- Chieffi & Limongi (2013) [3]_
	- Nomoto, Kobayashi & Tominaga (2013) [4]_
	- Chieffi & Limongi (2004) [5]_
	- Woosley & Weaver (1995) [6]_

Contents
--------
fractional : <function>
	Calculate an IMF-averaged yield for a given element.
table : <function>
	Obtain the table of mass yields and progenitor masses for a given element
	from a given study.
settings : ``dataframe``
	Stores current settings for these yields.
engines : module
	Models for massive star explodability as a function of progenitor mass for
	use in yield calculations.
LC18 : module
	Sets yields according to the Limongi & Chieffi (2018) study.
S16 : module
	Sets the yields according to one of the explosion engines in the
	Sukhbold et al. (2016) study.
CL13 : module
	Sets yields according to the Chieffi & Limongi (2013) study.
NKT13 : module
	Sets yields according to the Nomoto, Kobayashi & Tominaga (2013) study.
CL04 : module
	Sets yields according to the Chieffi & Limongi (2004) study.
WW95 : module
	Sets yields according to the Woosley & Weaver (1995) study.

Notes
-----
The yield tables built into this module reflect a post-processing treatment for
two radioactive nuclides. For the Limongi & Chieffi (2018), Sukhbold et al.
(2016), and Chieffi & Limongi (2013) tables, we add the nickel-56 yield to the
iron yields and the aluminum-26 yield to the magnesium yields. We also add
the aluminum-26 yield to the magnesium yields for the Woosley & Weaver (1995)
study. Otherwise, the data are included *as published*. The Chieffi & Limongi
(2013) and Nomoto, Kobayashi & Tominaga (2013) yields report yields after
radioactive isotopes have been decayed, so no further treatment is necessary.

.. [1] Limongi & Chieffi (2018), ApJS, 237, 13
.. [2] Sukhbold et al. (2016), ApJ, 821, 38
.. [3] Chieffi & Limongi (2013), ApJ, 764, 21
.. [4] Nomoto, Kobayashi & Tominaga (2013), ARA&A, 51, 457
.. [5] Chieffi & Limongi (2004), ApJ, 608, 405
.. [6] Woosley & Weaver (1995), ApJ, 101, 181
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["engines", "fractional", "settings", "table", "test"]
	from . import engines
	from ._yield_integrator import integrate as fractional
	from .grid_reader import table
	from .settings import settings
	from .tests import test

else:
	pass

