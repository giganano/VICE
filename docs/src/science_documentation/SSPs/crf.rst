
The Cumulative Return Fraction 
------------------------------
The cumulative return fraction is defined as the mass fraction of a single 
stellar population that is returned back to the interstellar medium (ISM) 
as gas. When dying stars produce their remnants, whatever material that does 
not end up in the remnant is returned to the ISM. This quantity can be 
calculated from an initial-final mass relation and an adopted stellar initial 
mass function (IMF). In short, the cumulative return fraction can be stated 
mathematically as "ejected material from dead stars in units of total initial 
amount of material." Its analytic form is therefore given by: 

.. math:: r(t) = 
	\int_{m_\text{to}(t)}^u (m - m_\text{rem})\frac{dN}{dm} dm 
	\left[\int_l^u M \frac{dN}{dm} dm\right]^{-1} 

The current version of VICE employs the initial-final remnant mass relation 
of Kalirai et al. (2008) [17]_: 

.. math:: m_\text{rem}(m) = \Biggl \lbrace {
	1.44\ (m \geq 8) 
	\atop 
	0.394 + 0.109 m\ (m < 8) 
	}

For a power-law IMF :math:`dN/dm \sim m^{-\alpha}`, the numerator of 
:math:`r(t)` is thus given by: 

.. math:: \int_{m_\text{to}(t)}^u (m - m_\text{rem}(m)) \frac{dN}{dm} dm = 
	\frac{1}{2 - \alpha} m^{2 - \alpha}\Bigg|_{m_\text{to}(t)}^u - 
	\frac{1.44}{1 - \alpha} m^{1 - \alpha} \Bigg|_{m_\text{to}(t)}^u 

for :math:`m_\text{to}(t) \geq 8`, and 

.. math:: \int_{m_\text{to}(t)}^u (m - m_\text{rem}(m)) \frac{dN}{dm} dm = 
	\frac{1.44}{1 - \alpha} m^{1 - \alpha} \Bigg|_8^u + 
	\left[\frac{0.394}{1 - \alpha}m^{1 - \alpha} + 
	\frac{0.109}{2 - \alpha}m^{2 - \alpha} 
	\right]_{m_\text{to}(t)}^8 


for :math:`m_\text{to}(t) < 8`. 

This solution is analytic. For piecewise IMFs, this becomes a summation over 
the relevant mass ranges of the IMF, and each term has the exact same form. 
The normalization of the IMF is irrelvant here, because the same normalization 
will appear in the denominator. 

The denominator has a simpler analytic form: 

.. math:: \int_l^u m \frac{dN}{dm} dm = 
	\frac{1}{2 - \alpha} m^{2 - \alpha} \Bigg|_l^u 

:ref:`Here <fig_crf>` we plot :math:`r` as a function of the stellar 
population's age assuming the mass-lifetime relation of Hurley, Pols & Tout 
(2000) [18]_ (see discussion :ref:`here <mlr>`). 
Weinberg, Andrews, and Freudenburg (2017) [19]_ adopted 
instantaneous recycling, whereby a fraction of the stellar population's mass 
:math:`r_\text{inst}` is returned *instantaneously* in the interest of an 
analytic approach to singlezone models. They find that :math:`r_\text{inst}` = 
0.4 and :math:`r_\text{inst}` = 0.2 is an adequate approximation for Kroupa 
[20]_ and Salpeter [21]_ IMFs. This reduces the more sophisticated formulation 
implemented here to: 

.. math:: r(t) \approx \Bigg \lbrace { 
	r_\text{inst}\ (t = 0) 
	\atop 
	0\ (t > 0) 
	} 

In reality, the rate of mass return from a stellar population of mass 
:math:`M_*` is given by :math:`\dot{r}M_*`, but in implementation, the 
quantization of timesteps allows each timestep to represent a single stellar 
population which will eject mass :math:`M_*dr` in a time interval :math:`dt`. 
For that reason, VICE is implemented with a calculation of :math:`r(t)` rather 
than :math:`\dot{r}`. 

In simulations, VICE allows users the choice between the time-dependent 
formulation of :math:`r(t)` derived here and the instantaneous approximation 
of Weinberg, Andrews, and Freudenburg (2017) by specifying a preferred value 
of :math:`r_\text{inst}`, which allows any fraction between 0 and 1. 

In calculations of :math:`r(t)` with the built-in Kroupa and Salpeter IMFs, 
the analytic solution is calculated. In the case of a user-customized IMF, 
VICE solves the equation numerically using quadrature with the methods 
described in chapter 4 of Press, Teukolsky, Vetterling & Flannery (2007) [22]_. 

.. note:: The approximation of :math:`h(t) \approx 1 - r(t)` where :math:`h` 
	is the :ref:`main sequence mass fraction <msmf>` fails at the 
	:math:`\sim5-10\%` level. See our discussion of this point 
	:ref:`here <approx_1minusr>`. 

Relevant source code: 

	- ``vice/src/ssp/crf.c`` 
	- ``vice/src/yields/integral.c`` 

.. [17] Kalirai et al. (2008), ApJ, 676, 594 
.. [18] Hurley, Pols & Tout (2000), MNRAS, 315, 543 
.. [19] Weinberg, Andrews & Freudenburg (2017), ApJ, 837, 183 
.. [20] Kroupa (2001), MNRAS, 322, 231 
.. [21] Salpeter (1955), ApJ, 121, 161 
.. [22] Press, Teukolsky, Vetterling & Flannery (2007), Numerical Recipes, 
	Cambridge University Press 
