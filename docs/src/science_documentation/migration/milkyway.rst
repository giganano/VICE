
Milky Way-Like Galaxies 
-----------------------
VICE's ``milkyway`` object is designed to handle multizone models of Milky 
Way-like galaxies in a flexible manner. To ease the burden on the user to 
provide all of the details, the ``milkyway`` object adopts a spatial 
configuration in which each zone represents an annulus of the Milky Way disk; 
these annuli are concentric from a radius :math:`R` = 0 to 20 kpc. The width 
of each annulus :math:`\Delta R` is a value the user may set upon construction 
of a ``milkyway`` object. For an in-depth example of an application of the 
``milkyway`` object, we refer users to the models of Johnson et al. (2021, 
in prep [2]_), for which these features were designed. 

As a default, these models adopt the ``vice.toolkit.hydrodisk.hydrodiskstars`` 
object to drive stellar migration. This object is built around star particle 
data from the ``h277`` simulation (Christensen et al. 2012 [3]_), a zoom-in 
hydrodynamical simulation ran from cosmological preconditions which has made a 
number of appearances in the literature to date (e.g. Zolotov et al. 2012 [4]_; 
Loebman et al. 2012 [5]_, 2014 [6]_; Brooks & Zolotov 2014 [7]_). A synopsis of 
the detailed simulation parameters and cosmological model can be found in 
section 2 of Bird et al. (2020 [8]_). In each annulus and timestep, VICE will 
search its built-in ``h277`` data for star particles that formed at a similar 
radius and time: specifically :math:`R \pm` 250 pc and :math:`T \pm` 250 Myr. 
It then selects a star particle at random from those that fit these criteria, 
and assumes the stellar population in its chemical evolution model to have the 
same :math:`\Delta R` as the ``h277`` star particle. If no star particles are 
found which satisfy these initial search criteria, then the search is widened 
to :math:`R \pm` 500 pc and :math:`T \pm` 500 pc. If still no ``h277`` 
particles are found, the search is widened in :math:`R` until one is found, but 
remains restricted to :math:`T \pm` 500 Myr. 

The ``hydrodiskstars`` object supports four models for the time-dependence of a 
star's radius between its birth and the present day. The first case is one in 
which stars remain at their birth radius until the present day, at which time 
they instantly migrate; mixing is a post-processing prescription in this 
scenario. The second case is a generalization of this in which the sudden 
migration to the present-day radius occurs at a time randomly drawn between the 
birth time and the end of the simulation. The third is one in which the radius 
changes with a :math:`\sqrt{\text{age}}` dependence, and the final is one with 
a linear dependence on time. These are the "post-processing", "sudden", 
"diffusion", and "linear" migration models from Johnson et al. (2021, in prep). 
The ``hydrodiskstars`` object adopts "diffusion" as the default. 

:ref:`Here <fig_migration_milkyway>` we illustrate these four migration models 
in the :math:`R-T` plane. While VICE's internal ``h277`` data supply a stellar 
population in VICE's models with :math:`\Delta R`, one of these four 
assumptions and its birth radius (assumed to be in the center of its zone of 
birth), its radius at all times is known. We emphasize that there is no N-body 
integration that goes into VICE's ``milkyway`` models. Although these are four 
built-in presets that users may choose from, they are not restricted to these 
options. A custom migration scheme based on the ``h277`` data can be 
implemented by subclassing the ``hydrodiskstars`` object, overriding its 
``__call__`` function, and setting the attribute ``mode`` to ``None``. 

The ``milkyway`` object also adopts as a default a relation between the surface 
densities of star formation and gas (:math:`\dot{\Sigma}_\star - 
\Sigma_\text{gas}`) which is a power-law with two breaks. Below 
:math:`\Sigma_\text{gas} = 5\times10^6 M_\odot kpc^{-2}`, the relation scales 
as :math:`\dot{\Sigma}_\star \sim \Sigma_\text{gas}^{1.7}`. For surface 
densities between :math:`5\times10^6` and :math:`2\times10^7 M_\odot kpc^{-2}`, 
the relation steepens to a power-law index of 3.6. Above :math:`2\times10^7 
M_\odot kpc^{-2}`, the relation becomes linear. These surface densities at 
which the power-law index changes, and the power-law indeces themselves, can 
be modified by the user. 

Furthermore, the ``milkyway`` object adopts a scaling of the mass loading 
factor :math:`\eta` which corresponds to an :math:`\alpha`-element radial 
abundance gradient that scales as mode([:math:`\alpha`/H]) :math:`\sim` 
-0.08 :math:`kpc^{-1}`, with the normalization set by mode([:math:`\alpha`/H]) 
= +0.3 at :math:`R` = 4 kpc for a constant star formation history. Like the 
stellar migration prescription and the star formation law, this is only a 
default and can be modified by the user if they so choose. 

The ``milkyway`` object does not have any treatment for vertical structure of 
the star forming disk; that is, the boundaries between zones are purely 
radial. There are no zones off the disk midplane. This implicitly assumes that 
the star forming reservoir is well-mixed in the azimuthal and vertical 
directions, and that significant abundance differences occur only in the 
radial direction. For further discussion of the ``milkyway`` object, we refer 
users to section 2 of Johnson et al. (2021, in prep). 

Relevant Source Code 

	- ``vice/milkyway/milkyway.py`` 
	- ``vice/toolkit/J21_sf_law.py`` 
	- ``vice/toolkit/hydrodisk/hydrodiskstars.py`` 
	- ``vice/toolkit/hydrodisk/_hydrodiskstars.pyx`` 

.. [2] Johnson et al. (2021, in prep) 
.. [3] Christensen et al. (2012), MNRAS, 425, 3058 
.. [4] Zolotov et al. (2012), ApJ, 761, 71 
.. [5] Loebman et al. (2012), ApJ, 758, L23 
.. [6] Loebman et al. (2014), ApJ, 794, 151 
.. [7] Brooks & Zolotov (2014), ApJ, 786, 87 
.. [8] Bird et al. (2020), arxiv:2005.12948 

