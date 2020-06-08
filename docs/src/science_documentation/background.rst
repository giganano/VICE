
Background 
==========

Galactic Chemical Evolution 
---------------------------
Galactic Chemical Evolution (often referred to as galactic archaeology) 
studies the connection between a galaxy's evolution and the chemical 
compositions of its stars. Big Bang Nucleosynthesis produced only hydrogen, 
helium, and trace amounts of lithium, the three lightest elements on the 
periodic table. To first order, everything else was produced via nuclear 
fusion in supernovae and through various channels of stellar evolution, the 
yields of which are dictated by nuclear physics. The abundances of different 
nuclei within stars therefore has physical information on the number of 
nucleosynthetic events and thus the number of stars that came before it. 
For more theoretical background on galactic archaeology, see sections 1 and 2 
and the citations therein of `Johnson & Weinberg (2020)`__. 

__ paper1_ 
.. _paper1: https://arxiv.org/abs/1911.02598 

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

