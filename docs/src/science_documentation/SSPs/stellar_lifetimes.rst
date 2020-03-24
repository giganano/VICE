
.. _mlr: 

Stellar Lifetimes 
-----------------
In VICE we adopt the following functional form for the lifetime of a star on 
the main sequence: 

.. math:: \tau_\text{MS} = \tau_\odot m^{-\alpha} 

where :math:`\tau_\odot` is the sun's main sequence lifetime, :math:`\alpha` 
is the power-law index of the mass-lifetime relationship. The constant 
``SOLAR_LIFETIME`` declares :math:`\tau_\odot` = 10 Gyr, and 
``MASS_LIFETIME_PLAW_INDEX`` delcares :math:`\alpha` = 3.5. Both constants are 
declared in ``vice/src/ssp.h``. 

The scaling of :math:`\tau_\text{MS} \sim m^{-3.5}` fails for high mass 
stars (:math:`\gtrsim 8 M_\odot`), but these stars have lifetimes that are 
very short compared to the relevant timescales of galactic chemical evolution 
(:math:`\sim`few Myr compared to :math:`\few` Gyr). This approximation fails 
for low mass stars as well (:math:`\lesssim 0.5 M_\odot`), but these stars 
have very long lifetimes that are considerably longer than the age of the 
universe. Because VICE does not support simulations on this long of 
timescales, this approximation suffices for all timescales of interest. 

This is motivated by a conventional power-law relationship between mass and 
luminosity :math:`L \sim M^{+\beta}`. The lifetime then scales as 
:math:`\tau \sim M/L \sim M^{1 - \beta}`. :math:`\alpha` = 3.5 corresponds to 
:math:`L \sim M^{4.5}` in the mass range of interest. 

This equation can be generalized to find the the *total lifetime* of a star 
of mass :math:`m`: the time until it produces a remnant by simply amplifying 
the lifetime by a factor :math:`1 + p_\text{MS}`:

.. math:: \tau_\text{total} = (1 + p_\text{MS})\tau_\odot m^{-\alpha} 

where :math:`p_\text{MS}` is an adopted lifetime ratio of the post main 
sequence to main sequence phases of stellar evolution. 

By interpreting :math:`\tau_\text{total}` as lookback time, we can solve for 
the mass of remnant producing stars under this model. 

.. _mlr_m_postMS: 

.. math:: m_\text{postMS} = \left(\frac{t}{(1 + p_\text{MS})\tau_\odot}
	\right)^{-1/\alpha} 

This equation allows the solution of both the *main sequence turnoff mass* and 
the mass of stars at the end of their post main sequence lifetimes by whether 
or not :math:`p_\text{MS}` = 0. 

Relevant source code: 

	- ``vice/src/ssp.h`` 
	- ``vice/src/ssp/mlr.c`` 

