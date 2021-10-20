
Asymptotic Giant Branch Stars
-----------------------------
Asymptotic giant branch (AGB) stars are evolved stars that have carbon-oxygen
cores surrounded by helium and hydrogen shells. These stars undergo thermal
pulsations due to explosive ignition of helium fusion in the shell, typically
referred to as helium shell flashes. During these pulses, material from the
core is often mixed into the outer layers via convection, a process known as
*dredge-up*. This brings heavy nuclei produced in the deeper regions of the
star to the envelope, which is then ejected to the interstellar medium (ISM).
This is one of the primary sites of s-process nucleosynthesis in the universe.

It may be tempting to model AGB star enrichment as a delay-time distribution
(DTD) similar to that adopted for SNe Ia. However, this approach would
implicitly adopt the assumption that every element is enriched via AGB stars
with the same DTD, or that for a given element, the effective DTD is
independent of metallicity. These may be fine assumptions, but it is not
adopted in VICE due to the desire for as few assumptions as possible.

Instead, AGB star enrichment in VICE is implemented using the
:ref:`mass-lifetime relationship for stars <mlr>` and the
:ref:`main sequence mass fraction <msmf>` (MSMF). However, the form of the
:ref:`MSMF <msmf>` required here differs in detail from the true
:ref:`MSMF <msmf>`. Being evolved stars, the
:ref:`MSMF <msmf>` does not consider AGB stars. It is thus not the
:ref:`MSMF <msmf>` and the main sequence lifetimes of stars that are of
interest, but the mass fraction of both main sequence and evolved stars and
the *total* lifetime of stars. The form of :math:`h(t)` necessary for modeling
AGB star enrichment then changes to:

.. math:: h(t) \rightarrow \frac{
	\int_l^{m_\text{postMS}(t)} m \frac{dN}{dm} dm
	}{
	\int_l^u m \frac{dN}{dm} dm
	}

The numerator is evaluated from :math:`l` to the mass of stars ending their
post main sequence lifetime :math:`m_\text{postMS}` rather than the main
sequence turnoff mass :math:`m_\text{to}`. As detailed
:ref:`here <mlr_m_postMS>` for a stellar population of age :math:`\tau`:

.. math:: m_\text{postMS} = \left(\frac{\tau}{(1 + p_\text{MS})\tau_\odot}
	\right)^{-1/\alpha}

where :math:`\alpha` is the power-law index on the
:ref:`mass-lifetime relationship <mlr>`, :math:`\tau_\odot` is the main
sequence lifetime of the sun, and :math:`p_\text{MS}` is the ratio of a star's
post main sequence lifetime to its main sequence lifetime.

From a single stellar population, the rate of ejection of an element :math:`x`
from AGB stars to the ISM is given by:

.. math:: \dot{M}_x^\text{AGB} =
	-\epsilon_x^\text{AGB}y_x^\text{AGB}(m_\text{postMS}, Z)M_\star\dot{h}

where :math:`\dot{h}` is evaluated at the lookback time to the stellar
population's formation [3]_, :math:`M_\star` is the initial mass of the
stellar population, and :math:`y_x^\text{AGB}` is the
*fractional net yield* of :math:`x` from an AGB star of initial mass
:math:`m_\text{postMS}` and metallicity :math:`Z`: the fraction of a single
star's initial mass that is processed into element :math:`x` *and* ejected to
the interstellar medium *minus* the amount that the star was born with.
:math:`\epsilon_x^\text{AGB}` is the *entrainment fraction* of the element
:math:`x` from AGB stars; this is the mass fraction of the net yield which is
retained by the interstellar medium, the remainder of which is added directly
to the outflow.

.. note:: VICE implements recycling of previously produced elements separate
	from nucleosynthetic yields, running from the standpoint of *net* rather
	than *absolute* yields.

For continuous star formation, the enrichment rate can be expressed as this
quantity integrated over the star formation history:

.. math:: \dot{M}_x^\text{AGB} =
	-\int_0^t \epsilon_x^\text{AGB} y_x^\text{AGB}(m_\text{postMS}(t - t'),
	Z_\text{ISM}(t')) \dot{M}_\star(t') \dot{h}(t - t') dt

This expression is approximated numerically as:

.. math:: \dot{M}_x^\text{AGB} \approx
	\sum_i \epsilon_x^\text{AGB} y_x^\text{AGB}(m_\text{postMS}(t - i\Delta t),
	Z_\text{ISM}(i\Delta t)) \dot{M}_\star(i\Delta t)
	\left[h((i + 1)\Delta t) - h(i\Delta t)\right]

where the summation is taken over all previous timesteps.
The need to differentiate :math:`h` with time is eliminated in the
numerical approximation by allowing each stellar population to be weighted
by :math:`\Delta h` between the current timestep and the next, made possible
by the quantization of timesteps.

In practice, :math:`y_x^\text{AGB}` is highly uncertain [4]_. VICE therefore
makes no assumptions about the user's desired form of the yield; this
parameter can be assigned either a built-in table published in an AGB star
nucleosynthesis study or a function of stellar mass and metallicity
constructed by the user.


Relevant source code:

	- ``vice/src/singlezone/agb.c``
	- ``vice/core/dataframe/_agb_yield_settings.pyx``
	- ``vice/yields/agb/__init__.py``


.. [3] There is a minus sign here because :math:`h(t)` is a monotonically
	decreasing function, and thus :math:`\dot{h} < 0`.

.. [4] See Andrews, Weinberg, Schoenrich & Johnson (2017), ApJ, 835, 224 and
	the citations therein for a detailed analysis of multiple elements.


Extension to Multizone Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The migration of star particles into and out of zones can affect the AGB star
enrichment rate in a given zone. In a singlezone simulation it is exactly as
expected for the star formation history, but in a multizone model, it is
coupled to the star formation histories in other zones. Because VICE knows the
zone each star particle occupies at all times in simulation, the rate of AGB
star enrichment rate of some element :math:`x` should not be expressed as an
integral over the star formation history, but as a summation over the stellar
populations present in the zone:

.. math:: \dot{M}_x^\text{AGB} \approx \sum_i
	\epsilon_x^\text{AGB} y_x^\text{AGB}(m_\text{postMS}(\tau_i), Z_i) M_i
	[h(\tau_i) - h(\tau_i + \Delta t)]

where :math:`Z_i`, :math:`M_i`, and :math:`\tau_i` are the metallicity,
initial mass, and age, respectively, of the :math:`i`'th star particle in a
given zone at a given time.

Relevant Source Code:

	- ``vice/src/multizone/agb.c``

