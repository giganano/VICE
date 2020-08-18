
.. _gas: 

The Gas Supply 
==============

.. _gas_ifr_sfr_eff: 

Inflows, Star Formation, and Efficiency 
---------------------------------------
Like the :ref:`enrichment equation <enr_eq>`, the time derivative of the mass 
of the gas in the interstellar medium (ISM) :math:`M_\text{g}` is a simple sum 
of source and sink terms. For an infall rate (IFR) :math:`\dot{M}_\text{in}`, 
star formation rate (SFR) :math:`\dot{M}_\star`, and outflow rate (OFR) 
:math:`\dot{M}_\text{out}`: 

.. math:: \dot{M}_g = \dot{M}_\text{in} - \dot{M}_\star - \dot{M}_\text{out} + 
	\dot{M}_\text{r} 

where :math:`\dot{M}_\text{r}` is the rate of recycling from stars producing 
remnants and return gas to the ISM at their birth metallicity. Because VICE is 
implemented with a Forward Euler solution, this equation is evaluated via: 

.. math:: \Delta M_g \approx \dot{M}_g\Delta t = 
	\dot{M}_\text{in}\Delta t - \dot{M}_\star \Delta t - \dot{M}_\text{out} 
	\Delta t + \dot{M}_\text{r}\Delta t 

By construction, VICE operates such that the user specifies either an infall 
history (:math:`\dot{M}_\text{in}` in :math:`M_\odot yr^{-1}` as a function of 
time), a star formation history (:math:`\dot{M}_\star` in :math:`M_\odot 
yr^{-1}` as a function of time), or the gas history (:math:`M_\text{g}` in 
:math:`M_\odot` as a function of time). The user also specifies a star 
formation efficiency timescale [1]_: 

.. math:: \tau_\star \equiv \frac{M_g}{\dot{M}_\star} 

Users may specify an arbitrary function of time in Gyr to describe 
:math:`\tau_\star`, whose units are assumed to be Gyr. With one of either 
:math:`\dot{M}_\text{in}`, :math:`\dot{M}_\star`, or :math:`M_\text{g}` 
specified by the user, :math:`\tau_\star`,  and the implementation of 
:math:`\dot{M}_\text{out}` and :math:`\dot{M}_\text{r}` discussed in this 
section, the solutions to :math:`\dot{M}_\text{in}`, :math:`\dot{M}_\star`, 
and :math:`M_g` as functions of time are unique. 

VICE also allows users to adopt a formulation of :math:`\tau_\star` that 
depends on the gas supply; this is an application of the Kennicutt-Schmidt 
relation to the single-zone approximation. This is implemented as a power-law: 

.. math:: \tau_\star^{-1} = \tau_{\star,\text{spec}}^{-1} 
	\left(\frac{M_g}{M_{g,\text{Schmidt}}}\right)^\alpha 

where :math:`M_{g,\text{Schmidt}}` is a normalizing gas supply and 
:math:`\tau_{\star,\text{spec}}` is the user-specified :math:`\tau_\star`. 
The ``singlezone`` object will employ this scaling when the attribute 
``schmidt = True``. 

Relevant Source Code: 

	- ``vice/src/singlezone/ism.c`` 

.. [1] In the interstellar medium literature, this quantity is often referred 
	to as the "depletion time" due to star formation. In the galactic 
	archaeology literature, it quantifies the fractional rate at which gas 
	forms stars, and is thus often refered to in terms of star formation 
	efficiency. We retain this nomenclature here. 

.. _gas_outflows: 

.. include:: outflows.rst 

.. _gas_recycling: 

.. include:: recycling.rst 
