
Asymptotic Giant Branch Stars
-----------------------------
The net yield of some element :math:`x` from an asymptotic giant branch (AGB)
star is defined as the net fraction of a star's mass that is converted to an
element :math:`x`. For many elements, this also varies considerably with the
initial metallicity of the star. This is therefore inherently a function of
two parameters:

.. math:: y_x^\text{AGB}(M_\star, Z) = \frac{M_{x,\text{ejected}}}{M_\star(|Z)}

where :math:`M_\star(|Z)` is the mass of a single star of known metallicity
:math:`Z`.

Contrary to yields from supernovae, no remaining calculations are necessary,
because :math:`M_{x,\text{ejected}}` is quantified in supernova
nucleosynthesis studies, and VICE's internal data tables have already divided
these values by :math:`M_\star(|Z)`. These tables are sampled on of order
:math:`\sim` 10 solar masses and metallicities; users may adopt these tables
in their simulations and VICE will determine the yield for all other masses
and metallicities via bilinear interpolation between masses and metallicities
on the grid. For masses and metallicities above or below the grid, it
extrapolates from the two highest or lowest elements on the grid, respectively.
Users may also construct their own mathematical forms of
:math:`y_x^\text{AGB}`.

When using a built-in table of yields, VICE enforces non-negative yields for
progenitors with masses below 1.5 :math:`M_\odot`.
This is to prevent numerical artifacts associated with extrapolation to
progenitor masses below the lowest value on the yield table.
In the :ref:`figure below <fig_yields_agb>`, we plot the AGB star yields of
barium as a function of progenitor mass for a handful of metallicities on
the Cristallo et al. (2011, 2015) table of yields.
This is a prototypical example of the motivation behind this decision - many
elements have a non-monotonic dependence of their AGB star yields on progenitor
mass, and this grid does not sample below 1.3 :math:`M_\odot`.
As a consequence, VICE's interpolation routines without modification would
extrapolate :math:`y_\text{Ba}^\text{AGB}` to be negative for lower masses;
this would be a purely numerical artifact.
Rather than allowing linear extrapolation to infer potentially large, negative
yields, it is safer to assume that the yields approach zero with decreasing
mass.

If this behavior isn't desired and it would instead be preferred to allow
linear extrapolation at low masses, the object ``vice.yields.agb.interpolator``
does not force yields to zero, and it can be used as an element's AGB star
yield setting (i.e. its entry in the ``vice.yields.agb.settings`` object).
Users looking to modify the AGB star yields of a given element with this
object should also be aware that they may need to force yields to zero below
some characteristic mass in order to suppress these numerical artifacts.

In this version of VICE, users can choose between the following
nucleosynthesis studies:

	- Cristallo et al. (2011, 2015) [7]_ [8]_
	- Karakas (2010) [9]_
	- Ventura et al. (2013) [10]_
	- Karakas & Lugaro (2016) [11]_; Karakas et al. (2018) [12]_

Users can also read these tables in with the ``vice.yields.agb.grid`` function.

Relevant Source Code:

	- ``vice/src/singlezone/agb.c``
	- ``vice/yields/agb/_grid_reader.pyx``

.. [7] Cristallo et al. (2011), ApJS, 197, 17
.. [8] Cristallo et al. (2015), ApJS, 219, 40
.. [9] Karakas (2010), MNRAS, 403, 1413
.. [10] Ventura et al. (2013), MNRAS, 431, 3642
.. [11] Karakas & Lugaro (2016), ApJ, 825, 26
.. [12] Karakas et al. (2018), MNRAS, 477, 421
