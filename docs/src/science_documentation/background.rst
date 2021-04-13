
Background 
==========

Galactic Chemical Evolution 
---------------------------
Galactic chemical evolution and galactic archaeology study the connection 
between a galaxy's evolution and the chemical compositions of its gas and 
stars, with the latter having somewhat special emphasis on the Milky Way. 
Big Bang Nucleosynthesis produced only hydrogen, 
helium, and trace amounts of lithium, the three lightest elements on the 
periodic table. To first order, everything else was produced via nuclear 
fusion in supernovae and through various channels of stellar evolution, the 
yields of which are dictated by nuclear physics. The abundances of different 
nuclei within stars therefore has physical information on the number of 
nucleosynthetic events and thus the number of stars that came before it. 
For more theoretical background on galactic chemical evolution, see sections 1 
and 2 and the citations therein of `Johnson & Weinberg (2020)`__. 

__ paper1_ 
.. _paper1: https://ui.adsabs.harvard.edu/abs/2019arXiv191102598J/abstract 

The Singlezone Approximation 
----------------------------
The singlezone approximation (also known as the onezone approximation, onezone 
models, box models, or variations thereof), refers to the assumption of 
instantaneous diffusion of newly produced metals in interstellar gas. This 
assumptions mandates that these nuclei be uniformly distributed at all times. 
By deliberately sacrificing all phase space information, the equations of 
these models reduce to a system of couple integro-differential equations of 
mass with time. While these equations only allow analytic solutions under 
further *mathematical* approximations, they can be easily integrated 
numerically. 

VICE includes features for running numerical simulations of singlezone models 
in the ``singlezone`` class. In this documentation, we detail the analytic 
motivation and numerical approximations implemented in VICE in handling 
these simulations. 

The Multizone Approximation
----------------------------
The multizone approximation refers to the extension of singlezone models to 
take into account phase space information with any degree of sophistication. 
By allowing singlezone models to evolve in parallel, and to mix stars and gas 
amongst them under some prescription, information on the spatial structure of 
the model galaxy can be added back to the simulation. 

VICE includes features for running numerical simulations of multizone models 
in the ``multizone`` class. In this documentation, we detail the analytic 
motivation and numerical approximations implemented in VICE in handling 
these simulations. 
