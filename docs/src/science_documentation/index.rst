
.. _scidocs:

Science Documentation
=====================
In this documentation we adopt the notation where a lower-case :math:`m`
implicitly represents the mass ratio of the star to the sun, a unitless
mass measurement. When relevant, we refer to the mass of a star with units
with an upper-case :math:`M`. In a similar fashion, :math:`l` and :math:`u`
refer to the lower and upper mass limits of star formation, respectively.

All nucleosynthetic yields in chemical evolution models provided by VICE are
defined as *fractional net yields*.
That is, they quantify the mass of stellar material that is processed into a
given element and subsequently ejected to the ISM
*in units of the star or stellar population's initial mass*, and they do *not*
quantify the mass fraction of nucleosynthetic material that a star or stellar
population was born with.
We denote these values with a lower-case :math:`y` with subscripts and
superscripts denoting the element and the enrichment channel, respectively.

A capital :math:`Z` refers always to the metallicity by mass:

.. math:: Z \equiv \frac{M_x}{M}

Where :math:`M_x` refers to the mass of some element :math:`x` and :math:`M`
to the mass of either the interstellar gas or a star.

The logarithmic abundance measurement :math:`[X/H]` is defined by:

.. math:: [X/H] \equiv \log_{10}\left(\frac{Z_x}{Z_x^\odot}\right)

This approximation assumes hydrogen mass fractions are similar to the sun
always.
Relaxing this assumption would require subtracting the term
:math:`\log_{10}(X/X_\odot)` where :math:`X` is the hydrogen mass fraction.
However, this is generally a negligible correction as hydrogen mass fractions
vary only a little, especially on a logarithmic scale (:math:`\lesssim` 0.05
dex), and neither the types of models that VICE provides nor observationally
derived abundances can claim this level of precision anyway.
The logarithmic abundance ratios :math:`[X/Y]` follow accordingly:

.. math:: [X/Y] = [X/H] - [Y/H] =
	\log_{10}\left(\frac{Z_x}{Z_x^\odot}\right) -
	\log_{10}\left(\frac{Z_y}{Z_y^\odot}\right)

The symbols :math:`\odot` and :math:`\tau` refer to the sun and a timescale,
respectively, and we use the term "zone models" refers to both one-zone and
multi-zone models in the general sense.


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

