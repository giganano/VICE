
Stellar Metallicity Distribution Functions
------------------------------------------
VICE's ``singlezone`` and ``multizone`` objects automatically determine
normalized stellar metallicity distribution functions (MDFs) for each
simulation. The MDF, in its most general form, is given by:

.. math:: \frac{dN}{dZ} = \frac{\dot{N}}{\dot{Z}} \propto
	\frac{\dot{M}_\star}{\dot{Z}}

This is fairly intuitive; the number of stars that form at a metallicity
:math:`\approx` Z is proportional to the star formation rate at that time and
inversely related to the rate at which the metallicity is evolving away from
that value. VICE converts MDFs to probability distribution functions by
ensuring that the integral over the bins is equal to one:

.. math:: \frac{dN}{d[X/Y]} \rightarrow \frac{
	dN/d[X/Y]
	}{
	\int dN
	} = \frac{
	dN/d[X/Y]
	}{
	\int_{-\infty}^{\infty} \frac{dN}{d[X/Y]} d[X/Y]
	}

.. note:: In its current version, VICE only reports MDFs at the final timestep
	of the simulation.

In practice, the user specifies an array of bin-edges that they would like
the MDF sorted into, and VICE creates arrays of zeroes whose lengths are the
number of bins in the user's array. In a singlezone simulation, the
appropriate bins for each combination of [X/H] and [X/Y] are incremented by
the star formation rate. At the final timestep, the normalization of the i'th
bin is then approximated numerically by:

.. math:: \frac{\Delta N_i}{\Delta [X/Y]_i} \rightarrow \frac{
	\Delta N_i / \Delta [X/Y]_i
	}{
	\sum_j \frac{\Delta N_j}{\Delta [X/Y]_j} \Delta [X/Y]_j
	} = \frac{
	\Delta N_i / \Delta [X/Y]_i
	}{
	\sum_j \Delta N_j
	}

The fraction of stars in a given range :math:`\Delta [X/Y]` is then given by
the value of the reported MDF times :math:`\Delta [X/Y]`.

In a multizone simulation, the metallicity distribution function is calculated
directly from the star particles that are in a given zone at a given time.
For each star particle in a given zone, the appropriate bins in [X/H] and
[X/Y] are incremented by the mass of the star rather than by the star
formation rate at previous timesteps. The same normalization process is then
applied.


