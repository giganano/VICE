
Recycling 
---------
As stars produce remnants, the mass that does not end up in the remnant is 
returned to the interstellar medium (ISM). The net effect of this from all 
previous episodes of star formation quantifies the rate of recycling: 

.. math:: \dot{M}_\text{r} = \int_0^t \dot{M}_\star(t - t') \dot{r}(t') dt' 

where :math:`r(\tau)` is the :ref:`cumulative return fraction <crf>` from 
a single stellar population of age :math:`\tau`. This is approximated 
numerically according to 

.. math:: \dot{M}_\text{r} \approx 
	\sum_i \dot{M}_\star(t - i\Delta t) 
	\left[r((i + 1)\Delta t) - r(i\Delta t)\right] 

This is an instance where the quantization of star forming episodes due to the 
Forward Euler solution simplifies the implementation; the stars that form in 
previous timesteps contribute :math:`\Delta r` of their mass back to the ISM. 

In the case of instantaneous recycling, this simplifies further to 

.. math:: \dot{M}_\text{r} \approx r_\text{inst}\dot{M}_\star 

Weinberg, Andrews & Freudenburg (2017) [2]_ demonstrate that 
:math:`r_\text{inst}` = 0.4 (0.2) for a Kroupa [3]_ (Salpeter [4]_) IMF are 
good approximations. 

.. note:: Instantaneous recycling refers only previously produced 
	nucleosynthetic products. While this term has been used to refer to 
	instantaneous production of new heavy nuclei in the astronomical literature 
	in the past, VICE retains this approximation only for enrichment from 
	core collapse supernovae. 

Relevant Source Code: 

	- ``vice/src/singlezone/recycling.c`` 

.. [2] Weinberg, Andrews & Freudenburg (2017), ApJ, 837, 183 

.. [3] Kroupa (2001), MNRAS, 322, 231 

.. [4] Salpeter (1955), ApJ, 121, 161 
