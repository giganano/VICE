
Core Collapse Supernovae  
------------------------
Core collapse supernovae (CCSNe) are the explosions of massive stars 
(:math:`\gtrsim 8 M_\odot`) at the end of their post main sequence lifetimes. 
Due to the steep nature of the lifetime-stellar mass relationship, these stars 
have lifetimes that are extremely short compared to the relevant timescales of 
galactic chemical evolution (:math:`\sim` few Myr compared to :math:`\sim` few 
Gyr). To a good approximation, the lifetimes of these stars can be treated as 
instantaneous in zone models. 

.. note:: Another motivation for this approximation is that the lifetimes are 
	often significantly shorter than the typical mixing timescales in even 
	modestly sized galaxies. The longest lifetimes of these stars is of order 
	tens of megayears; in comparison, the mixing timescale in the solar 
	annulus of the Milky Way is likely comparable to the dynamical timescale 
	at this distance (:math:`\sim` 250 Myr, a factor of ten larger). Zone 
	models at their core already assume that these mixing timescales are 
	negligibly short due to the assumption of instantaneous mixing; if 
	CCSN timescales are even shorter, then they can certainly also be modeled 
	as instantaneous. 

VICE therefore approximates CCSNe as being simultaneous with the formation 
of their progenitor stars. This implies a linear relationship between the 
rate of production of some element :math:`x` from CCSNe and the star formation 
rate: 

.. math:: \dot{M}_x^\text{CC} = \epsilon_x^\text{CC} 
	y_x^\text{CC}(Z)\dot{M}_\star 

where :math:`y_x^\text{CC}` is the *IMF-averaged fractional net yield* of 
the element :math:`x` from CCSNe at a metallicity :math:`Z`: the fraction of 
the entire stellar population's initial mass that is processed into the 
element :math:`x` *and* ejected to the interstellar medium *minus* the amount 
that the star was born with. :math:`\epsilon_x^\text{CC}` is the 
*entrainment fraction* of the element :math:`x` from CCSNe; this is the mass 
fraction of the net yield which is retained by the interstellar medium, the 
remainder of which is added directly to the outflow. 

.. note:: VICE implements recycling of previously produced elements separate 
	from nucleosynthesis, running from the standpoint of *net* rather than 
	*absolute* yields. 

In practice, :math:`y_x^\text{CC}` is highly uncertain [1]_. VICE therefore 
makes no assumptions about the user's desired form of the yield; this 
parameter can be assigned either a number to represent a 
metallicity-independent yield, or a function of the metallicity by mass 
:math:`Z = M_x/M_g`. VICE includes features which will calculate the value of 
:math:`y_x^\text{CC}` for a given element and metallicity based on the results 
of supernova nucleosynthesis studies upon request, but requires the user to 
specify an exact number or function. 

Relevant Source Code: 

	- ``vice/src/singlezone/ccsne.c`` 
	- ``vice/core/dataframe/_yield_settings.pyx`` 
	- ``vice/yields/ccsne/__init__.py`` 

.. [1] See Andrews, Weinberg, Schoenrich & Johnson (2017), ApJ, 835, 224 and 
	the citations therein for a detailed analysis of multiple elements. 


Extension to Multizone Models 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Because VICE approximates core collapse supernovae as occuring instantaneously 
following the formation of their progenitor stars, this implies that 
CCSN progenitors also should not migrate between zones in a multizone model. 
Therefore, the formalism implemented for singlezone models is retained in 
multizone simulations. 

Relevant Source Code: 

	- ``vice/src/multizone/ccsne.c`` 

