
Science Documentation 
=====================
In this documentation we adopt the notation where a lower-case :math:`m` 
implicitly represents the mass ratio of the star to the sun, a unitless 
mass measurement. When relevant, we refer to the mass of a star with units 
with an upper-case :math:`M`. In a similar fashion, :math:`l` and :math:`u` 
refer to the lower and upper mass limits of star formation, respectively. 

All nucleosynthetic yields are in fractional units; that is, they quantify the 
mass fraction of stellar material's initial mass that is processed into a 
given element and subsequently ejected to the ISM. Nucleosynthetic products 
that end up locked in stellar remnants should not be taken into account in 
these models. These values are denoted with a lower-case :math:`y` with 
test subscripts and superscripts denoting the element and the enrichment 
channel. 

The metallicity by mass :math:`Z` refers always to the metallicity by mass: 

.. math:: Z \equiv \frac{M_x}{M} 

Where :math:`M_x` refers to the mass of some element :math:`x` and :math:`M` 
to the mass of either the interstellar gas or a star. 

The logarithmic abundance measurement [X/H] is defined by: 

.. math:: [X/H] \equiv \log_{10}\left(\frac{Z_x}{Z_x^\odot}\right) 

This approximation assumes hydrogen mass fractions are similar to the sun 
always. Relaxing this assumption would require subtracting the term 
:math:`\log_{10}(X/X_\odot)` where :math:`X` is the hydrogen mass fraction. 
However, this is generally a negligible correction as hydrogen mass fractions 
vary only a little, especially on a logarithmic scale (:math:`\lesssim` 0.05 
dex). The logarithmic abundance ratios [X/Y] follow accordingly: 

.. math:: [X/Y] = [X/H] - [Y/H] = 
	\log_{10}\left(\frac{Z_x}{Z_x^\odot}\right) - 
	\log_{10}\left(\frac{Z_y}{Z_y^\odot}\right) 

Here and hereafter the symbols :math:`\odot` and :math:`\tau` refer to the sun 
and a timescale, respectively. 

The term "zone models" refers to both singlezone and multizone models in the 
general sense. 


.. toctree:: 
	:maxdepth: 5 
	:numbered:
	
	background 
	implementation 
	SSPs/index 
	gas/index 
	enrichment/index 
	yields/index 
	migration/index 
	milkyway/index 
	z_calibration 
	stellar_mdfs 

