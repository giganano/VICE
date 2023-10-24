
Type Ia Supernovae
------------------
The net yield of some element :math:`x` from a single stellar population due
to type Ia supernovae (SNe Ia) can be expressed as the total production from
the duty cycle of the delay-time distribution (DTD) :math:`R_\text{Ia}`:

.. math:: y_x^\text{Ia} \equiv M_x\int_0^\infty R_\text{Ia}(t) dt

where :math:`M_x` is the average mass yield of the element :math:`x` from a
single type Ia supernovae.

.. note:: In the astronomical literature, the delay-time distribution is
	usually defined as the rate of SN Ia explosions per unit stellar mass
	formed :math:`M_\star`. :math:`R_\text{Ia}` thus has units of
	:math:`M_\odot^{-1} yr^{-1}`, making :math:`y_x^\text{Ia}` unitless as it
	should be. We retain this definition here for consistency.

The integral over the DTD is simply the number of SN Ia events that occur per
unit stellar mass formed:

.. math:: y_x^\text{Ia} = M_x \frac{N_\text{Ia}}{M_\star}

Intuitively, the SN Ia yield is thus specified by the mass yield of a single
SN Ia explosion and the number of SN Ia events that occur per unit solar
mass formed.

Maoz & Mannucci (2012) [7]_ found that :math:`N_\text{Ia}/M_\star` =
:math:`(2 \pm 1) \times 10^{-3} M_\odot^{-1}`. That is, on average,
approximately 500 :math:`M_\odot` of stars must form for a given stellar
population to produce a single SN Ia.

The value of :math:`M_x` can be determined from the results of simulation of
SNe Ia. The yield is then evaluated with a user-specified value of
:math:`N_\text{Ia}/M_\star`; the default value is :math:`N_\text{Ia}/M_\star`
= :math:`2.2 \times 10^{-3}`, the best-fit value from Maoz & Mannucci (2012).

In this version of VICE, users can choose between the following
nucleosynthesis studies:

	- Iwamoto et al. (1999), ApJ, 124, 439
	- Seitenzahl et al. (2013), MNRAS, 429, 1156

.. note:: These functions have no impact whatsoever on the chemical enrichment
	simulations built into VICE. Users declare their own yields for that
	purpose, while this function merely calculates them.

Relevant Source Code:

	- ``vice/yields/sneia/_yield_lookup.pyx``

.. [7] Maoz & Mannucci (2012), PASA, 29, 447
