
Type Ia Supernovae 
------------------
Type Ia supernovae are the thermonuclear detonations of white dwarf stars. 
Being the remnants of lower-mass stars, white dwarfs are born and explode on 
timescales longer than the mixing timescales of galaxies. Therefore, the 
intrinsic time delay is non-negigible. 

This requires a model for the SN Ia delay-time distribution (DTD), defined as 
the rate of SN Ia explosions associated with a single stellar population. 
Given a DTD :math:`R_\text{Ia}` and an age :math:`\tau`, the rate of 
production of some element :math:`x` from a single stellar population is given 
by 

.. math:: \dot{M}_x^\text{Ia} = 
	y_x^\text{Ia}(Z)M_* \frac{
	R_\text{Ia}(\tau) 
	}{
	\int_0^\infty R_\text{Ia}(t) dt 
	}

.. note:: The integral of this equation from :math:`t = 0` to :math:`\infty` 
	must equal the yield times the mass of the stellar population. This 
	necessitates the normalization of the DTD. 

where :math:`y_x^\text{Ia}` is the *IMF-averaged fractional net yield* of the 
element :math:`x` from SNe Ia at metallicity :math:`Z`: the fraction of the 
stellar population's initial mass that is processed into the element 
:math:`x` *and* ejected to the interstellar medium *minus* the amount that 
the star was born with. 

.. note:: VICE implements recycling of previously produced elements separate 
	from nucleosynthesis, running from the standpoint of *net* rather than 
	*absolute* yields. 

In practice, :math:`y_x^\text{Ia}` is highly uncertain [2]_. VICE therefore 
makes no assumptions about the user's desired form of the yield; this 
parameter can be assigned either a number to represent a 
metallicity-independent yield or a function of metallicity by mass 
:math:`Z = M_x/M_g`. VICE includes features which will calculate the value of 
:math:`y_x^\text{Ia}` for a given element and metallicity based on the results 
of supernova nucleosynthesis studies upon request, but requires the user to 
specify an exact number or function. 

The rate of enrichment from all previous episodes of star formation can be 
derived by integrating this equation over all ages: 

.. math:: \dot{M}_x^\text{Ia} = 
	y_x^\text{Ia}(Z)\frac{
	\int_0^t \dot{M}_*(t')R_\text{Ia}(t - t')dt'
	}{
	\int_0^\infty R_\text{Ia}(t')dt' 
	}

This can also be expressed as the star formation history up to a time :math:`t` 
weighted by the SN Ia rate. VICE approximates this equation as: 

.. math:: \dot{M}_x^\text{Ia} \approx \frac{
	\sum_i y_x^\text{Ia}(Z_\text{ISM}(i\Delta t)) \dot{M}_*(i\Delta t) 
	R_\text{Ia}(t - i\Delta t) \Delta t 
	}{
	\sum_i^{T_\text{Ia}} R_\text{Ia}(i\Delta t) \Delta t 
	} 

where the sum in the numerator is over all timesteps and in the denominator up 
to a time :math:`T_\text{Ia}` denoting an adopted full length of the SN Ia 
duty cycle. The constant ``RIA_MAX_EVAL_TIME`` declares :math:`T_\text{Ia}` = 
15 Gyr in ``vice/src/sneia.h``. 

In implementation, VICE normalizes the DTD at the beginning of the simulation. 
For an age :math:`\tau = t - t'`: 

.. math:: R_\text{Ia}(\tau) \rightarrow \frac{
	R_\text{Ia}(\tau) 
	}{
	\int_0^{T_\text{Ia}} R_\text{Ia}(\tau) d\tau 
	} \approx \frac{
	R_\text{Ia}(t - i\Delta t)
	}{
	\sum_i^{T_\text{Ia}} R_\text{Ia}(i\Delta t)\Delta t
	} \implies R_\text{Ia}(t - t')\Delta t \rightarrow 
	\frac{
	R_\text{Ia}(t - i\Delta t)\Delta t
	}{
	\sum_i^{T_\text{Ia}} R_\text{Ia}(i\Delta t)\Delta t 
	}

Inserting the normalized rate into the equation for 
:math:`\dot{M}_x^\text{Ia}`: 

.. math:: \dot{M}_x^\text{Ia} \approx 
	\sum_i y_x^\text{Ia}(Z_\text{ISM}(i\Delta t)) \dot{M}_*(i\Delta t) 
	R_\text{Ia}(t - i\Delta t) 

VICE implements this normalization of :math:`R_\text{Ia}` at the beginning of 
simulations due to the simplification of this expression introduced in doing 
so. This reduces the computational expense in calculating this quantity for 
each element at each timestep. 

VICE includes two built-in DTDs, denoting by strings as ``plaw`` and ``exp``. 
As their names suggest, they are a power-law and an exponential DTD: 

	- "plaw": :math:`R_\text{Ia} \sim t^{-1.1}` 
	- "exp": :math:`R_\text{Ia} \sim e^{-t/\tau_\text{Ia}}` 

Users may also construct their own functional forms of :math:`R_\text{Ia}`, 
which must accept time in Gyr as the only parameter. These functions need not 
be normalized in any way; VICE normalizes the DTD automatically. 

Relevant Source Code: 

	- ``vice/src/sneia.h`` 
	- ``vice/src/singlezone/sneia.c`` 
	- ``vice/yields/sneia/__init__.py`` 

.. [2] See Andrews, Weinberg, Schoenrich & Johnson (2017), ApJ, 835, 224 and 
	the citations therein for a detailed analysis of multiple elements. 

