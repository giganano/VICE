
.. _enr: 

Enrichment 
==========
VICE takes a general approach in modeling nucleosynthesis. All elements are 
treated equally; there are no special considerations for any element. In this 
documentation we derive the analytic form of 
:ref:`the enrichment equation <enr_eq>` for an arbitrary element :math:`x` 
with arbitrary nucleosynthetic yields for arbitrary evolutionary 
histories. This is an integro-differential equation of the element's mass as a 
function of time, which VICE solves as an initial-value problem by imposing 
the boundary condition that its abundance at time zero is given by the 
primordial abundance from big bang nucleosynthesis. In this version of VICE, 
helium is the only element for which this value is nonzero. 

.. _enr_eq: 

The Enrichment Equation 
-----------------------
The enrichment equation quantifies the rate of change of an element's total 
mass present in the interstellar medium (ISM). At its core, it is a simple sum 
of source and sink terms. 

.. math:: \dot{M}_x = 
	\dot{M}_x^\text{CC} + 
	\dot{M}_x^\text{Ia} + 
	\dot{M}_x^\text{AGB} - 
	\frac{M_x}{M_g}\left[
	\dot{M}_\star + \xi_\text{enh}\dot{M}_\text{out}
	\right] + 
	\dot{M}_x^\text{r} + 
	Z_{x,\text{in}}\dot{M}_\text{in} 

where :math:`M_x` is the mass of the element :math:`x` in the interstellar 
medium, :math:`\dot{M}_x` its time-derivative, and :math:`M_g` the mass of the 
ISM gas. :math:`\dot{M}_x^\text{CC}`, :math:`\dot{M}_x^\text{Ia}`, and 
:math:`\dot{M}_x^\text{AGB}` quantify the rate of production from 
core-collapse supernovae (CCSNe), type Ia supernovae (SNe Ia), and asymptotic 
giant branch (AGB) stars, respectively. 

We detail each term individually here. 

.. _enr_ccsne: 

.. include:: ccsne.rst 

.. _enr_sneia: 

.. include:: sneia.rst 

.. _enr_agb: 

.. include:: agb.rst 

Subsequent Terms 
----------------
The remaining terms in the enrichment equation make simple statements about 
remaining source and sink terms. 

VICE retains the assumption that stars are born at the same metallicity as the 
ISM from which they form. This motivates the sink term 

.. math:: -\left(\frac{M_x}{M_g}\right)\dot{M}_\star 

where the mass of the element :math:`x` is depleted at the metallicity of the 
ISM :math:`Z_x = M_x/M_g` in proportion with the star formation rate 
:math:`\dot{M}_\star`. 

Many galactic chemical evolution models to date have assumed that outflows 
from galaxies occur at the same metallicity of the ISM. This would suggest 
that :math:`\dot{M}_x^\text{out} \approx (M_x/M_g)\dot{M}_\text{out}`. 
However, recent work in the astronomical literature from both simulations 
(e.g. Christensen et al. (2018) [5]_) and observations (e.g. Chisholm, 
Trimonti & Leitherer (2018) [6]_) suggest that this may not be the case. 
Therefore, VICE allows outflows to occur at some multiplicative factor 
:math:`\xi_\text{enh}` above or below the ISM metallicity, which may vary 
with time. This motivates the sink term 

.. math:: -\left(\frac{M_x}{M_g}\right)\xi_\text{enh}\dot{M}_\text{out} 

Because :ref:`VICE works with net rather than absolute yields <yields>`, 
simulations must quantify the rate at which stars return mass to the ISM at 
their birth metallicity. This is mathematically similar to the rate of total 
gas recycling, but weighted by the metallicities of the stars recycling. Since 
stars are assumed to form at the metallicity of the ISM, 

.. math:: \dot{M}_x^\text{r} = 
	\int_0^t \dot{M}_\star(t') Z_{x,\text{ISM}}(t') \dot{r}(t - t') dt 

where :math:`r(\tau)` is the :ref:`cumulative return fraction <crf>` from a 
single stellar population of age :math:`\tau`. This is approximated 
numerically as 

.. math:: \dot{M}_x^\text{r} \approx 
	\sum_i \dot{M}_\star(i\Delta t) Z_{x,\text{ISM}}(i\Delta t) 
	\left[r((i + 1)\Delta t) - r(i\Delta t)\right] 

where the summation is taken over all previous timesteps. The need to 
differentiate :math:`r` with time is eliminated in the numerical approximation 
by allowing each stellar population to be weighted by :math:`\Delta r` between 
the current timestep and the next, made possible by the quantization of 
timesteps. In the event that the user has specified instantaneous recycling: 

.. math:: \dot{M}_x^\text{r} = r_\text{inst}\dot{M}_\star Z_{x,\text{ISM}} 

At any given timestep, there is gas infall onto the simulated galaxy of a 
given metallicity :math:`Z`. In most cases this term is negligibly small, but 
in some interesting cases it may not be (e.g. a major merger event). This 
necessitates the final term :math:`Z_{x,\text{in}}\dot{M}_\text{in}`. 

Relevant source code: 

	- ``vice/src/singlezone/element.c`` 
	- ``vice/src/singlezone/ism.c`` 

Sanity Checks 
-------------
At all timesteps VICE forces the mass of every element to be non-negative. If 
the mass is found to be below zero at any given time, it is assumed to not be 
present in the interstellar medium and is assigned a mass of exactly zero. 
Absent this, the mass of each element reported by VICE is merely the 
numerically estimated solution to the enrichment equation. 


Relevant source code: 

	- ``vice/src/singlezone/element.c`` 

.. [5] Christensen et al. (2018), ApJ, 867, 142 

.. [6] Chisholm, Trimonti & Leitherer (2018), MNRAS, 481, 1690 


