
.. _ssp: 

Single Stellar Populations
==========================
As discussed in our section on :ref:`implementation <implementation>`, VICE's 
simulations are implemented with a Forward Euler timestep solution, an 
approximation made possible by numerics not being the dominant source of 
error. The quantization of timesteps necessitates the quantization of the 
episodes of star formation. This allows VICE to model enrichment in both 
singlezone and multizone models by using summations over a sample of 
discretized stellar populations. 

For this reason, we implement a treatment of two quantities particularly 
useful in the mass evolution of single stellar populations: the 
:ref:`cumulative return fraction <crf>` (CRF) and the 
:ref:`main sequence mass fraction <msmf>` (MSMF). The :ref:`CRF <crf>` 
represents the fraction of a single stellar population's mass that is returned 
to the interstellar medium as gas. The :ref:`MSMF <msmf>` is the fraction of 
its mass that is still in the form of main sequence stars. These quantities 
are of particular use in calculating the rate of mass recycling and the rate 
of enrichment from asymptotic giant branch stars. 

.. _mlr: 
.. include:: stellar_lifetimes.rst 

.. _fig_mlr: 
.. include:: stellar_lifetimes.fig.rst 

.. _crf: 
.. include:: crf.rst 

.. _fig_crf: 
.. include:: crf.fig.rst 

.. _msmf: 
.. include:: msmf.rst 

.. _fig_msmf:
.. include:: msmf.fig.rst 

.. _ssp_enr: 
.. include:: enrichment.rst 

.. _ssp_multizone: 
.. include:: multizone.rst 

