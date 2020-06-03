

The Main Sequence Mass Fraction 
-------------------------------
The main sequence mass fraction, as the name suggests, is the fraction of a 
single stellar population's initial mass that is still in the form of main 
sequence stars. Because this calculation does not concern evolved stars, 
neither a model for the post main sequence lifetime nor an initial-final 
remnant mass relation is needed; it is thus considerably simpler than the 
:ref:`cumulative return fraction <crf>`. This quantity is instead specified 
entirely by the IMF and the mass-lifetime relation. 

It's analytic form is given by: 

.. math:: h(t) = 
	\int_l^{m_\text{to}(t)} m\frac{dN}{dm} dm 
	\left[
	\int_l^u m\frac{dN}{dm} dm 
	\right]^{-1} 

which for a power-law IMF :math:`dN/dm \sim m^{-\alpha}` becomes 

.. math:: h(t) = 
	\left[\frac{1}{2 - \alpha}m^{2 - \alpha}\Bigg|_l^{m_\text{to}(t)}\right] 
	\left[\frac{1}{2 - \alpha}m^{2 - \alpha}\Bigg|_l^u\right]^{-1} 

It may be tempting to cancel the factor of :math:`1/(2 - \alpha)`, but more 
careful consideration must be taken for piece-wise IMFs like Kroupa [7]_: 

.. math:: h(t) = 
	\left[
	\sum_i \frac{1}{2 - \alpha_i} m^{2 - \alpha_i}
	\right]_l^{m_\text{to}(t)} 
	\left(\left[
	\sum_i \frac{1}{2 - \alpha_i} m^{2 - \alpha_i} 
	\right]_l^u\right)^{-1} 

where the summation is over the relevant mass ranges with different power-law 
indeces :math:`\alpha_i`. In the case of kroupa :math:`\alpha` = 2.3, 1.3, and 
0.3 for :math:`m` > 0.5, 0.08 :math:`\leq m \leq` 0.5, and :math:`m` < 0.08, 
respectively. 

.. _approx_1minusr: 

:ref:`Here <fig_msmf>` we plot :math:`h` as a function of the stellar 
population's age. By 10 Gyr, :math:`h(t)` is as low as :math:`\sim0.45` 
for the Kroupa IMF and 
:math:`\sim0.65` for the Salpeter [8]_ IMF. In comparison, the 
:ref:`cumulative return fraction <crf>` :math:`r(t) \approx 0.45` for the 
Kroupa IMF and :math:`\sim0.28` for the Salpeter IMF. This suggests that the 
approximation :math:`h(t) \approx 1 - r(t)` fails at the :math:`\sim5-10\%` 
level, depending on the choice of IMF. This suggests that for old stellar 
populations, a non-negligible portion of the mass is contained in evolved 
stars and stellar remnants. VICE therefore differentiates between these two 
quantities in its implementation. 

In reality, the rate of the stellar mass evolving off of the main sequence is 
given by :math:`\dot{h}M_*` where :math:`M_*` is the initial mass of the 
stellar population. However, the quantization of timesteps in VICE allows each 
timestep to represent a single stellar population which will eject mass 
:math:`M_*dh` in a time interval :math:`dt`. For that reason, VICE is 
implemented with a calculation of :math:`h(t)` rather than :math:`\dot{h}`. 

In calculations of :math:`h(t)` with the built-in Kroupa and Salpeter IMFs, 
the analytic solution is calculated. In the case of a user-customized IMF, 
VICE solves the equation numerically using quadrature. 

Relevant source code: 

	- ``vice/src/ssp/msmf.c`` 
	- ``vice/src/yields/integral.c`` 

.. [7] Kroupa (2001), MNRAS, 322, 231 
.. [8] Salpeter (1955), ApJ, 121, 161 
