
Asymptotic Giant Branch Stars 
-----------------------------
The net yield of some element :math:`x` from an asymptotic giant branch (AGB) 
star is defined as the net fraction of a star's mass that is converted to an 
element :math:`x`. For many elements, this also varies considerably with the 
initial metallicity of the star. This is therefore inherently a function of 
two parameters: 

.. math:: y_x^\text{AGB}(M_\star, Z) = \frac{M_{x,\text{ejected}}}{M_\star(|Z)} 

where :math:`M_\star(|Z)` is the mass of a single star of known metallicity 
:math:`Z`. 

Contrary to yields from supernovae, no remaining calculations are necessary, 
because :math:`M_{x,\text{ejected}}` is quantified in supernova 
nucleosynthesis studies, and VICE's internal data tables have already divided 
these values by :math:`M_\star(|Z)`. These tables are sampled on of order 
:math:`\sim` 10 solar masses and metallicities; users may adopt these tables 
in their simulations and VICE will determine the yield for all other masses 
and metallicities via bilinear interpolation between masses and metallicities 
on the grid. For masses and metallicities above or below the grid, it 
extrapolates from the two highest or lowest elements on the grid, respectively. 
Users may also construct their own mathematical forms of 
:math:`y_x^\text{AGB}`. 

In this version of VICE, users can choose between the following 
nucleosynthesis studies: 

	- Cristallo et al. (2011), ApJS, 197, 17 
	- Karakas (2010), MNRAS, 403, 1413 

Users can also read these tables in with the ``vice.yields.agb.grid`` function. 

Relevant Source Code: 

	- ``vice/src/singlezone/agb.c`` 
	- ``vice/yields/agb/_grid_reader.pyx`` 
