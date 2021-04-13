
Milky Way-Like Galaxies 
-----------------------
VICE's ``milkyway`` object is designed handle multi-zone models of Milky 
Way-like galaxies in a flexible manner. Rather than requiring the user to 
construct them from scratch from the base ``multizone`` object, ``milkyway`` 
eases the burden by adopting a spatial configuration in which each zone 
represents an annulus of the Milky Way disk; these annuli are concentric from 
a radius :math:`R` = 0 to 20 kpc. The width of each annulus :math:`\Delta R` is 
a value the user may set upon construction of a ``milkyway`` object. As 
defaults, it adopts an observationally-motivated star formation law and a 
stellar migration prescription based on N-body simulations. For an in-depth 
example of an application of the ``milkyway`` object, we refer users to the 
models of Johnson et al. (2021, in prep [1]_), for which these features were 
designed. 

The default stellar migration model of the ``milkyway`` object is implemented 
in the ``vice.toolkit.hydrodisk.hydrodiskstars`` object. This object is built 
around data from the ``h277`` simulation (Christensen et al. 2021 [2]_), a 
zoom-in hydrodynamical simulation ran from cosmological initial conditions 
which has made a number of appearances in the literature to date (e.g. 
Zolotov et al. 2012 [3]_; Loebman et al. 2012 [4]_, 2014 [5]_; Brooks & 
Zolotov [6]_; Bird et al. 2021 [7]_). Although ``h277`` is currently the only 
simulation whose data is available to the ``hydrodiskstars`` object, it's 
implementation could be extended to include others. 

.. note:: The ``h277`` star particle data is not included in VICE's default 
	distribution, but is available in its GitHub repository at 
	vice/toolkit/hydrodisk/data. VICE will download these files automatically 
	when a ``milkyway`` or ``hydrodiskstars`` object is created for the first 
	time. With a decent internet connection, this process takes about one 
	minute to complete, and does not need repeated. If this process fails, it 
	may be due to not having administrator's privileges; users in this 
	situation should speak with their administrator, who would then be able to 
	download these data with the following few lines in ``python``: 

	>>> import vice 
	>>> vice.toolkit.hydrodisk.data.download() 

The Sample of Star Particles 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``hydrodiskstars`` object, the default stellar migration prescription for 
the ``milkyway`` object, makes use of the birth radii, final radii, and birth 
times of star particles from hydrodynamical simulations, for which only the 
``h277`` simulation is currently available (see above). ``h277`` did not 
record the birth radius of each star particle; however, each star particle 
does have an accurate age at each snapshot. The orbital radii of stars that are 
sufficiently young in their first snapshot should be good approximations of 
their birth radii since dynamical heating will have little effect in a short 
time interval. We have therefore restricted the sample of ``h277`` star 
particles in the ``hydrodiskstars`` object to those with an age at first 
snapshot less than 150 Myr, adopting their galactocentric radius at first 
snapshot as their birth radius. The choice of 150 Myr makes no significant 
impact on the predictions of the ``milkyway`` object (see discussion in section 
2.1 of Johnson et al. 2021). 

Of the star particles that remain after imposing this cut, the oldest one has 
an age of 13.23 Gyr. Since ``h277`` ran for ~13.7 Gyr, we have therefore 
subtracted 500 Myr from the birth times of all star particles, letting 
:math:`T` = 0 in the ``hydrodiskstars`` and ``milkyway`` objects correspond to 
:math:`T` = 500 Myr in ``h277``, and placing the onset of star formation in 
these models at that time. As a consequence, these models support calculations 
of chemical evolution up to lookback times of 13.2 Gyr. Although this limit is 
not enforced in VICE, simulations on longer timescales using the ``milkyway`` 
object are highly likely to produce a ``segmentation fault``. 

We further restrict the sample of ``h277`` star particles to only those with 
both formation and final radii of :math:`R \leq` 20 kpc, and to have formed 
within :math:`\left|z\right|\leq` 3 kpc of the disk midplane. These criteria 
ensure that our sample reflects only the star particles that formed *in-situ*, 
and can therefore be described by a disc GCE model. Although it's possible some 
number of these star particles formed in a dwarf galaxy as it was being 
accreted by ``h277``, these stars are few in number, and are only relevant at 
large radii and early times, where few stars form in nature anyway. 

Based on a kinematic decomposition of these star particles, we exclude halo 
stars from the sample, but include those with bulge, pseudobulge, and disc-like 
kinematics. This ensures that all stars which can be attributed to the 
spatially confined regions reasonably defining a spiral galaxy disk can be 
modeled using the ``hydrodiskstars`` object. Altogether, these cuts yield a 
sample of 3,102,519 star particles from ``h277``, accessible via the 
``analog_data`` attribute of the ``hydrodiskstars`` object. For an analysis of 
the results of these cuts, we refer users to section 2.1 of Johnson et al. 
(2021). 

Migration Models 
~~~~~~~~~~~~~~~~
As in many numerical models of galaxy evolution, stars in VICE are stand-ins 
for entire stellar populations. In the ``milkyway`` object (assuming the 
``hydrodiskstars`` object is driving migration), they are said to be in a 
given zone if their radius is between the inner and outer edges of the annulus. 
At all times, VICE places their nucleosynthetic products and returned envelopes 
in the ISM of the annulus that they are in *at that time*. 

The ``hydrodiskstars`` object assumes that star particles are born at the 
centers of their birth annuli. For a stellar population born at a time 
:math:`T` and galactocentric radius :math:`R`, it first searches for star 
particles in the ``h277`` sample (see above) which formed at :math:`T \pm` 250 
Myr and :math:`R \pm` 250 pc. It then randomly selects a star particle from 
this subsample to act as an *analog*. The stellar population in the VICE model 
then adopts the change in orbital radius :math:`\Delta R`, and moves their 
with an assumed time-dependence (see below). If no candidate analogs are found, 
the ``hydrodiskstars`` object widens the search to :math:`T \pm` 500 Myr and 
:math:`R \pm` 500 pc. If still no analog is found, it maintains the 
:math:`T \pm 500` Myr criterion, but finds the one with the smallest difference 
in birth radius, assigning that star particle as the analog. While this 
prescription allows stellar populations to be assigned analogs with 
significantly birth radii, this is only an issue for small :math:`T` and 
large :math:`R` where there are few star particles from ``h277``, and where few 
stars form in nature anyway. When an ``h277`` star particle is assigned as an 
analog, it is *not* thrown out of the sample of candidate analogs, in theory 
allowing a star particle to act as an analog for multiple stellar populations. 

The ``hydrodiskstars`` object provides four models for the time-dependence of 
a star's radius between its birth and the present day. The first case is one 
in which stars remain at their birth radius until the present-day, at which 
time they instantly migrate; mixing is a post-processing prescription in this 
scenario. The second case is a generalization of this in which the sudden 
migration to the present-day radius occurs at some time randomly drawn between 
the birth time and the end of the simulation. The third is one in which the 
radius change with a :math:`\sqrt{\text{age}}` dependence, and the final is one 
with a linear dependence on time. These are the "post-processing", "sudden", 
"diffusion", and "linear" migration models from Johnson et al. (2021, see 
section 2.2 therein for further details). The ``hydrodiskstars`` object adopts 
"diffusion" as the default. 

:ref:`Here <fig_migration>` we illustrate these four migration models 
in the :math:`R-T` plane. While VICE's internal ``h277`` data supply a stellar 
population in VICE's models with :math:`\Delta R`, given one of these four 
assumptions and its birth radius (assumed to be in the center of its zone of 
birth), its radius at all remaining times is known. We emphasize that there is 
no N-body integration that goes into VICE's ``milkyway`` models. Although these 
are four built-in presets that users may choose from, they are not restricted 
to these options. A custom migration scheme based on the ``h277`` data can be 
implemented by subclassing the ``hydrodiskstars`` object, overriding its 
``__call__`` function, and setting the attribute ``mode`` to ``None``. 

The Default Star Formation Law 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
As a default, the ``milkyway`` object adopts the ``vice.toolkit.J21_sf_law`` 
to describe the relation between the surface density of star formation 
:math:`\dot{\Sigma}_\star` and the surface density of the interstellar medium 
:math:`\Sigma_\text{g}`. This is also the star formation law adopted in 
Johnson et al. (2021). This star formation law is a broken power-law with 
two breaks; below :math:`\Sigma_\text{g} = 5\times10^6 M_\odot~kpc^{-2}`, the 
relation scales as :math:`\dot{\Sigma}_\star \propto \Sigma_\text{g}^{1.7}`. 
Between :math:`5\times10^6 M_\odot~kpc^{-2}` and 
:math:`2\times10^7 M_\odot~kpc^{-2}`, it scales as 
:math:`\dot{\Sigma}_\star \propto \Sigma_\text{g}^{3.6}`. Above 
:math:`2\times10^7 M_\odot~kpc^{-2}`, the relation becomes linear. 

The ``J21_sf_law`` calculates the star formation efficiency timescale 
:math:`\tau_\star` (usually referred to as a "depletion time" in the star 
formation, feedback, and interstellar medium literatures) for use with the 
``singlezone`` and ``multizone`` objects. This timescales is defined as the 
gas density per unit star formation: 
:math:`\tau_\star \equiv \dot{\Sigma}_\star / \Sigma_\text{g}`. 
To set the normalization of the star formation law, the ``J21_sf_law`` object 
assumes that in the linear regime, :math:`\tau_\star = \tau_\text{mol}`, the 
value of :math:`\tau_\star` for a star forming reservoir where hydrogen is 
entirely in the molecular phase. Below surface densities of 
:math:`2\times10^7 M_\odot kpc^{-2}`, the timescale increases in a 
piece-wise continuous manner. The ``J21_sf_law`` object affords users the 
ability to modify the surface densities at which there are breaks in the 
power-law, as well as the power-law indeces themselves. For additional 
discussion, we refer users to section 2.5 of Johnson et al. (2021). 

Additional Parameters 
~~~~~~~~~~~~~~~~~~~~~
The ``milkyway`` object adopts a scaling of the mass loading factor 
:math:`\eta \equiv \dot{M}_\text{out} / \dot{M}_\star` with galactocentric 
radius. The scaling is tuned such that the equilibrium abundances as a function 
of radius reflect a reasonable metallicity gradient in agreement with 
observational results from APOGEE (see section 2.3 of Johnson et al. 2021). 
The default scaling is based on alpha-elements (e.g., O, Ne, Mg) under a 
constant star formation history. The slope of the gradient is assumed to be 
mode([:math:`\alpha`/H]) :math:`\propto` -0.08 :math:`kpc^{-2}`, with the 
normalization set by mode([:math:`\alpha`/H]) = +0.3 at :math:`R` = 4 kpc. 
This default scaling is implemented via the function 
``vice.milkyway.default_mass_loading``, and like the star formation law and 
stellar migration prescription, is only a default and can be overridden by the 
user if they so choose. 

The ``milkyway`` object does not have any treatment for vertical structure of 
the star forming disk; that is, the boundaries between zones are purely 
radial. There are no zones off the disk midplane. This implicitly assumes that 
the star forming reservoir is well-mixed in the azimuthal and vertical 
directions, and that significant abundance differences occur only in the 
radial direction. By default it also neglects gas migration, because the 
Johnson et al. (2021) models for which it was designed focused instead on the 
impact of varying assumptions about stellar migration. 

For further discussion of the ``milkyway`` object, we refer users to section 2 
of Johnson et al. (2021, in prep). 

Relevant Source Code 

	- ``vice/milkyway/milkyway.py`` 
	- ``vice/toolkit/J21_sf_law.py`` 
	- ``vice/toolkit/hydrodisk/hydrodiskstars.py`` 
	- ``vice/toolkit/hydrodisk/_hydrodiskstars.pyx`` 
	- ``vice/src/toolkit/hydrodiskstars.c`` 

.. [1] Johnson et al. (2021, in prep) 
.. [2] Christensen et al. (2012), MNRAS, 425, 3058 
.. [3] Zolotov et al. (2012), ApJ, 761, 71 
.. [4] Loebman et al. (2012), ApJ, 758, L23 
.. [5] Loebman et al. (2014), ApJ, 794, 151 
.. [6] Brooks & Zolotov (2014), ApJ, 786, 87 
.. [7] Bird et al. (2020), arxiv:2005.12948 


.. _fig_migration: 
.. include:: migration.fig.rst 

