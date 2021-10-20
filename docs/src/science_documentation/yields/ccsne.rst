
Core Collapse Supernovae
------------------------
Because core collapse supernovae (CCSNe) are assumed to occur simultaneously
with the formation of their progenitor stars [2]_, :math:`y_x^\text{CC}`
represents the total yield from all CCSNe associated with a single stellar
population. Letting :math:`m_x` denote the net mass of some element :math:`x`
present in the CCSN ejecta, the yield at a given metallicity is defined by:

.. math:: y_x^\text{CC} \equiv \frac{
	\int_{l_\text{CC}}^u (E(m)m_x + w_x - Z_{x,\text{prog}} m)
	\frac{dN}{dm} dm
	}{
	\int_l^u m \frac{dN}{dm} dm
	}

where the numerator is taken from the minimum mass for a CCSN explosion
:math:`l_\text{CC}` to the upper mass limit of star formation :math:`u`, but
the denominator is over the entire mass range of star formation, and
:math:`dN/dm` is the stellar initial mass function (IMF). This equation is
nothing more or less than the mathematical statement of "production divided
by total initial mass."
:math:`E(m)` denotes the *explodability*: the fraction of star of mass
:math:`m` which explode as a CCSN. :math:`w_x` denotes the mass yield of the
element :math:`x` due to winds at a mass :math:`m`, and the corrective term
:math:`Z_{x,\text{prog}} m` accounts for the birth abundances of the star to
compute a *net* rather than a *gross* yield. The constant
``CC_MIN_STELLAR_MASS`` declares :math:`l_\text{CC} = 8 M_\odot` in
``vice/src/ccsne.h``.

In practice, supernova nucleosynthesis studies determine the value of
:math:`m_x` for of order 10 values of :math:`m` at a given metallicity and
rotational velocity. To compute the numerator of this equation, VICE adopts a
grid of :math:`m_x` and :math:`w_x` values from a user-specified
nucleosynthesis study, interpolating linearly between values of :math:`m` on
the grid. We clarify that the interpolation is linear in :math:`m`, and not
:math:`\log m`.

In this version of VICE, users can choose between the following
nucleosynthesis studies:

	- Limongi & Chieffi (2018), ApJS, 237, 13
	- Sukhbold et al. (2016), ApJ, 821, 38 (W18 and N20 explosion engines)
	- Chieffi & Limongi (2013), ApJ, 764, 21
	- Nomoto, Kobayashi & Tominaga (2013), ARA&A, 51, 547
	- Chieffi & Limongi (2004), ApJ, 608, 405
	- Woosley & Weaver (1995), ApJS, 101, 181

VICE affords users the ability to specify whether or not winds should be
included in their yield calculations; it stores values of :math:`w_x` for all
recognized elements at each metallicity and rotational velocity it has
built-in tables for. It also allows users the option to calculate net or
gross yields based on whether or not it sets :math:`Z_{x,\text{prog}}` equal
to zero. We caution however that not every study separates their wind yields
from their explosive yields, in which case :math:`w_x = 0` and the wind
contribution is included in :math:`m_x`. Furthermore, not every study reports
the detailed initial composition of their model stars, in which case
assigning :math:`Z_{x,\text{prog}}` is ambiguous. For these studies VICE is
incapable of computing net yields, so it sets :math:`Z_{x,\text{prog}}` to
zero always for these studies, only reporting gross yields. For a breakdown on
which of these cautionary tales apply to which studies, we refer users to the
``vice.yields.ccsne.fractional`` documentation.

By default, VICE will assume that all stars above :math:`8 M_\odot` explode
as a CCSN. Because stellar explodability is an open question in astronomy [3]_,
:math:`E(m)` can be specified as an arbitrary mathematical function, which
must accept stellar mass in :math:`M_\odot` as the only parameter. Lastly,
this can be done with either the built-in Kroupa [4]_ or Salpeter [5]_ IMFs,
or a function of mass interpreted as a user-constructed IMF.

.. note:: VICE also forces :math:`m_x` = 0 at :math:`8 M_\odot`, the default
	value of :math:`l_\text{CC}`, in order to minimize numerical artifacts
	introduced when extrapolating off of the grid in :math:`m` to lower
	stellar masses.

Although :math:`E(m)` can take on any mathematical form in VICE as long as its
value is always between 0 and 1, a number of popular forms both simple and
complex can be found in the ``vice.yields.ccsne.engines`` module.

Users can evaluate the solution to this equation by calling the function
``vice.yields.ccsne.fractional``, implemented in
``vice/yields/ccsne/_yield_integrator.pyx``. This function makes use of
numerical quadrature routines written in ANSI/ISO C built into VICE, and is
thus not dependent on any publicly available quadrature functions such as
those found in ``scipy``.

In addition to evaluating the solution to this equation, users may also
read in the table of :math:`m_x` values by calling ``vice.yields.ccsne.table``,
and may request the full isotopic breakdown. A ``dataframe`` is returned from
this function.

.. note:: These functions have no impact whatsoever on the chemical enrichment
	simulations built into VICE. Users declare their own yields for that
	purpose, while this function merely calculates them.

Relevant Source Code:

	- ``vice/src/yields/integral.c``
	- ``vice/yields/ccsne/_yield_integrator.pyx``
	- ``vice/yields/ccsne/table.py``
	- ``vice/core/dataframe/_ccsn_yield_table.pyx``


.. [2] See the discusion on :ref:`CCSN enrichment <enr_ccsne>` for
	justification of this assumption.

.. [3] See the discussion in Sukhbold et al. (2016), ApJ, 821, 38 and the
	citations therein for details.

.. [4] Kroupa (2001), MNRAS, 231, 322

.. [5] Salpeter (1955), ApJ, 121, 161

