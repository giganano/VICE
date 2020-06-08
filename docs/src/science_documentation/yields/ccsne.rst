
Core Collapse Supernovae 
------------------------
Because core collapse supernovae (CCSNe) are assumed to occur simultaneously 
with the formation of their progenitor stars [2]_, :math:`y_x^\text{CC}` 
represents the total yield from all CCSNe associated with a single stellar 
population. Letting :math:`m_x` denote the net mass of some element :math:`x` 
present in the CCSN ejecta, the yield at a given metallicity is defined by: 

.. math:: y_x^\text{CC} \equiv \frac{
	\int_{l_\text{CC}}^u E(m) m_x \frac{dN}{dm} dm 
	}{
	\int_l^u m \frac{dN}{dm} dm 
	}

where the numerator is taken from the minimum mass for a CCSN explosion 
:math:`l_\text{CC}` to the upper mass limit of star formation :math:`u`, but 
the denominator is over the entire mass range of star formation, and 
:math:`dN/dm` is the stellar initial mass function (IMF). 
:math:`E(m)` denotes the *explodability*: the fraction of stars of mass 
:math:`m` which explode as a CCSN. The constant ``CC_MIN_STELLAR_MASS`` 
declares :math:`l_\text{CC} = 8 M_\odot` in ``vice/src/ccsne.h``. This 
equation is nothing more than the mathematical statement of "production 
divided by total initial mass." 

In practice, supernova nucleosynthesis studies determine the value of 
:math:`m_x` for of order 10 values of :math:`m` at a given metallicity and 
rotational velocity. To compute the numerator of this equation, VICE adopts a 
grid of :math:`m_x` values from a user-specified nucleosynthesis study, 
interpolating linearly between values of :math:`m` on the grid. We clarify 
that the interpolation is linaer in :math:`m`, and not :math:`\log m`. 

In this version of VICE, users can choose between the following 
nucleosynthesis studies: 

	- Limongi & Chieffi (2018), ApJS, 237, 13 
	- Chieffi & Limongi (2013), ApJ, 764, 21 
	- Chieffi & Limongi (2004), ApJ, 608, 405 
	- Woosley & Weaver (1995), ApJS, 101, 181 

By default, VICE will assume that all stars above :math:`8 M_\odot` explode 
as a CCSN. Because stellar explodability is an open question in astronomy [3]_, 
:math:`E(m)` can be specified as an arbitrary mathematical function, which 
must accept stellar mass in :math:`M_\odot` as the only parameter. Lastly, 
this can be done with either the built-in Kroupa [4]_ or Salpeter [5]_ IMFs, 
or a function of mass interpreted as a user-constructed IMF. 

.. note:: VICE also forces :math:`m_x` = 0 at :math:`8 M_\odot`, the default 
	value of :math:`l_\text{CC}`, in order to minimize numerical artifacts 
	introduced when extrapolating off of the grid in :math:`m` to lower 
	stellar masses. 

Users can evaluate the solution to this equation by calling the function 
``vice.yields.ccsne.fractional``, implemented in 
``vice/yields/ccsne/_yield_integrator.pyx``. This function makes use of 
numerical quadrature routines written in ANSI/ISO C built into VICE, and is 
thus not dependent on any publicly available quadrature functions such as 
those found in ``scipy``. 

In addition to evaluating the solution to this equation, users may also 
read in the table of :math:`m_x` values by calling ``vice.yields.ccsne.table``, 
and may request the full isotopic breakdown. A ``dataframe`` is returned from 
this function. 

.. note:: These functions have no impact whatsoever on the chemical enrichment 
	simulations built into VICE. Users declare their own yields for that 
	purpose, while this function merely calculates them. 

Relevant Source Code: 

	- ``vice/src/yields/integral.c`` 
	- ``vice/yields/ccsne/_yield_integrator.pyx`` 
	- ``vice/yields/ccsne/table.py`` 
	- ``vice/core/dataframe/_ccsn_yield_table.pyx`` 


.. [2] See the discusion on :ref:`CCSN enrichment <enr_ccsne>` for 
	justification of this assumption. 

.. [3] See the discussion in Sukhbold et al. (2016), ApJ, 821, 38 and the 
	citations therein for details. 

.. [4] Kroupa (2001), MNRAS, 231, 322 

.. [5] Salpeter (1955), ApJ, 121, 161 

