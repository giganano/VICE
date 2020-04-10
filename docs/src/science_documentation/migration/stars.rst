
Stars 
-----
VICE adopts a star particle approach to the treatment of stars in multizone 
models. Users specify how many star particles should form per zone per 
timestep :math:`n_\star` via the attribute ``n_stars`` of the ``multizone`` 
class. The mass of a star particle is then given by: 

.. math:: M_\star \equiv \frac{\dot{M}_\star \Delta t}{n_\star} 

where :math:`\dot{M}_\star` and :math:`\Delta t` are the star formation rate 
and timestep size in the star particles zone of formation, respectively. In 
words, VICE divides the total mass of newly formed stars evenly amongst the 
star particles it should form. Rather than forming more/fewer star particles 
when the star formation rate is higher/lower, VICE forms star particles of 
varying mass. Star particles are also still formed when :math:`\dot{M}_\star` 
= 0; they simply have zero mass. 

For a given star particle formed in a given zone and at a given time, the zone 
it occupies at subsequent times can be expressed as an arbitrary function of 
time :math:`S` [1]_. Allowing for the fact that star particles form in all 
zones and at all timesteps, the full stellar migration prescription can be 
expressed as a function of three variables :math:`S(i, t_\text{form}, t)` 
where :math:`i` is the zone number the star particle forms in, 
:math:`t_\text{form}` the time at which it forms, and :math:`t` the time in 
the simulation (obviously, only times at which :math:`t > t_\text{form}` are 
relevant). 

:math:`S` is specified by the user. If the user does not specify a value of 
:math:`S`, VICE adopts a default value which returns :math:`i` at all times; 
that is, star particles remain in their zone of birth and do not migrate. 
If star particles forming in the same zone at the same time should have 
different zone histories, the user-defined function :math:`S` can be specified 
to take a fourth parameter: a keyword argument ``n``. VICE will then call the 
function with ``n = 1``, ``n = 2``, ``n = 3``, and so on, up to 
``n = n_stars``, and users can assign zone histories to star particles based 
on the value of ``n``. 

Relevant Source Code: 

	- ``vice/core/multizone/_migration.pyx`` 
	- ``vice/src/multizone/migration.c`` 

.. [1] Because :math:`Z` for zone would cause confusion with the metallicity 
	by mass :math:`Z`, we choose :math:`S` for star to denote this function 
	instead. 

