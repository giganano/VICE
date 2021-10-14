
.. _yields: 

Nucleosynthetic Yields 
======================
Due to the associated uncertainties [1]_, VICE takes an agnostic approach to 
the user's desired nucleosynthetic yields. Rather than adopting the results of 
a nucleosynthesis study, the user declares their yields outright. VICE 
includes features which will calculate yields upon request, but requires the 
user to explicitly tell it what the yield of each element from each enrichment 
channel should be (although there is a set of defaults). 

All yields in VICE are defined as *fractional net yields*. This is the 
amount of an element that is *produced and ejected* to the interstellar medium 
*minus* that which was already present, in units of the star or stellar 
population's initial mass. Previously produced nuclei should not be taken into 
account, because this is handled via *recycling*. For example, if a stellar 
population is born with :math:`1 M_\odot` of oxygen total and ejects 
:math:`1 M_\odot` of oxygen back to the interstellar medium, the yield is 
zero since there is no net gain. 

Yields are also defined for the average star or stellar population. 
Stochasticity in yields introduced by, e.g., sampling of the stellar initial 
mass function, should not be taken into account in yield calculations 
intended for use in VICE. 


.. [1] See Andrews, Weinberg, Schoenrich & Johnson (2017), ApJ, 835, 224 and 
	the citations therein for a detailed analysis of multiple elements. 

.. _yields_ccsne: 

.. include:: ccsne.rst 

.. _yields_sneia: 

.. include:: sneia.rst 

.. _yields_agb: 

.. include:: agb.rst 

.. _fig_yields_agb: 

.. include:: agb.fig.rst 
