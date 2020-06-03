
Outflows 
--------
In the astronomical literature, the strength/efficiency of outflows are 
typically quantified according to a dimensionless parameter referred to as the 
*mass loading factor*, defined as the ratio of the mass outflow rate to the 
star formation rate: :math:`\eta \equiv \dot{M}_\text{out}/\dot{M}_\star`. 
`Johnson & Weinberg (2020)`__ introduced a new parameter to generalize this, 
dubbed the "outflow smoothing time." This is the timescale on which the 
star-formation rate is averaged (i.e. "smoothed") to determine the outflow 
rate: 

__ paper1_ 
.. _paper1: https://ui.adsabs.harvard.edu/abs/2019arXiv191102598J/abstract 

.. math:: \dot{M}_\text{out} = 
	\eta(t)\langle\dot{M}_\star\rangle_{\tau_\text{s}} 
	= \frac{\eta(t)}{\tau_\text{s}}\int_{t - \tau_\text{s}}^t 
	\dot{M}_\star(t') dt' 

At early times when :math:`0 \leq t \leq \tau_\text{s}`, this average is taken 
over only the time interval from 0 to :math:`t`. This equation is approximated 
numerically according to: 

.. math:: \dot{M}_\text{out} \approx \eta(t) \frac{\Delta t}{\tau_\text{s}} 
	\sum_{i = 0}^{\tau_\text{s}/\Delta t} \dot{M}_\star(t - i\Delta t) 

Put simply, at each timestep VICE looks backs at the number of timesteps 
corresponding to the smoothing time, and determines the arithmetic mean of the 
star formation rate at those timesteps, then multiplies this number by 
:math:`\eta(t)`, which may be a user-specified function of time in Gyr. An 
advantage of this formulation is that when :math:`\tau_\text{s} < \Delta t`, 
VICE automatically recovers the traditional relation of 
:math:`\dot{M}_\text{out} = \eta(t)\dot{M}_\star(t)`. 

.. note:: It is only the star formation rate which is time averaged. The mass 
	loading factor is not time-averaged in any way. 

Relevant Source Code: 

	- ``vice/src/singlezone/ism.c`` 

