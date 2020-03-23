
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
The enrichment equation, at its core, is a simple sum of source and sink terms: 

.. math:: \dot{M}_x = 
	\dot{M}_x^\text{CC} + 
	\dot{M}_x^\text{Ia} + 
	\dot{M}_x^\text{AGB} - 
	\frac{M_x}{M_g}\left[\dot{M}_* + \xi_\text{enh}\dot{M}_\text{out}\right] + 
	\dot{M}_x^\text{r} + 
	Z_{x,\text{in}}\dot{M}_\text{in} 

where :math:`\dot{M}_x^\text{CC}`, :math:`\dot{M}_x^\text{Ia}`, and 
:math:`\dot{M}_x^\text{AGB}` is the rate of production of the element 
:math:`x` from core-collapse supernovae, type Ia supernovae, and asymptotic 
giant branch stars, respectively. :math:`-(M_x/M_g)\dot{M}_*` is the rate of 
mass depletion due to star formation. 
:math:`-(M_x/M_g)\xi_\text{enh}\dot{M}_\text{out}` is the rate of mass loss 
due to outflows. :math:`\dot{M}_x^\text{r}` is the rate of recycling, and 
:math:`Z_{x,\text{in}}\dot{M}_\text{in}` is the rate of metal addition due to 
metal-rich infall. 

.. _enr_ccsne: 

.. include:: ccsne.rst 

.. _enr_sneia: 

.. include:: sneia.rst 
