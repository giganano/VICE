
Gas
---
As discussed above, VICE knows nothing of the spatial configuration of the
zones in a multizone model: the only piece of information identifying a zone
is an integer index. Gas must then be able to move between zones in an
arbitrary manner.

We thus define the gas migration matrix :math:`G_{ij}` to
denote the mass fraction of gas that moves *from* the :math:`i`'th zone *to*
the :math:`j`'th zone in a 10 Myr time interval. We normalize to a specific
time interval so that the rate of migration does not depend on the timestep
size. The mass fraction of gas that migrates from zone :math:`i` to zone
:math:`j` at a time :math:`t` is then given by:

.. math:: f_{ij}(t) = G_{ij}(t)\frac{\Delta t}{\text{10 Myr}}

The mass that migrates is then given by :math:`M_{g,i} f_{ij}(t)`, where
:math:`M_{g,i}` is the total mass of the interstellar medium in zone
:math:`i`.

For a multizone simulation with :math:`N` zones, :math:`G` is an
:math:`N\times N` matrix, the elements of which the user can fill with either
numerical values denoting a constant rate of gas migration between zones or
functions of time denoting a varying rate of gas migration. The diagonal
elements :math:`G_{ii}` are however irrelevant, because this corresponds to
migration within the same zone; VICE forces these values to zero always.

Relevant Source Code:

	- ``vice/core/multizone/_migration.pyx``
	- ``vice/src/multizone/migration.c``
