
Enrichment from Single Stellar Populations
------------------------------------------
While galaxies form stars continuously, it is often an interesting scientific
problem to quantify the nucleosynthetic production of only one population of
conatal stars. This is inherently cheaper computationally, since this is only
one stellar population while galaxy simulations require many stellar
populations.

VICE includes functionality for simulating the mass production of a given
element from a single stellar population (i.e. an individual star cluster) of
given mass and metallicity under user-specified yields. This by construction
does not take into account depletion from infall low metallicity gas and star
formation, ejection in outflows, recycling, etc. It only calculates the mass
production of the element as a function of the stellar population's age.

The star cluster is assumed to form at time :math:`t = 0`, and thus at this
time there is no net production. Because VICE operates under the assumption
that all core-collapse supernovae (CCSNe) occur instantaneously following the
star cluster's formation [33]_, the entire CCSN net yield is injected within
the first timestep at :math:`t = \Delta t`:

.. math:: \Delta M_x = y_x^\text{CC}(Z) M_\star

where :math:`y_x^\text{CC}(Z)` is the user's current setting for CCSN yields
at a stellar metallicity Z. At subsequent timesteps, enrichment from
asymptotic giant branch (AGB) stars is injected according to [34]_:

.. math:: \dot{M}_x^\text{AGB}\Delta t \approx
	y_x^\text{AGB}(m_\text{postMS}(t), Z)M_\star
	\left[h(t) - h(t + \Delta t)\right]

and from type Ia supernovae (SN Ia) according to [35]_:

.. math:: \dot{M}_x^\text{Ia}\Delta t \approx
	y_x^\text{Ia}(Z) M_\star \frac{
	R_\text{Ia}(t)
	}{
	\int_0^\infty R_\text{Ia}(t') dt'
	}

These are the same equations that are implemented in simulating enrichment
under the single-zone approximation, but applied to only one episode of star
formation.

Users can run these simulations by calling ``vice.single_stellar_population``.

Relevant Source Code:

	- ``vice/src/ssp/ssp.c``
	- ``vice/core/ssp/_ssp.pyx``


.. [33] See the discussion of :ref:`enrichment from CCSNe <enr_ccsne>` for
	justification of this assumption.

.. [34] Justification of this can be found :ref:`here <enr_agb>`.

.. [35] Justification of this can be found :ref:`here <enr_sneia>`.

