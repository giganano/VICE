
Scaling of the Total Metallicity 
--------------------------------
VICE quantifies the total metallicity by mass of both gas and stars in VICE 
according to: 

.. math:: Z = Z_\odot \frac{\sum_i Z_i}{\sum_i Z_{i,\odot}} 

where the summation is taken over all elements tracked by the simulation. This 
is motivated by numerical artifacts that would be introduced into metallicity 
dependent quantities when only a small number of elements are being simulated. 
For example, if there are only three elements in a simulation and they are all 
near the solar abundance, this scaling ensures that metallicity dependent 
yields will behave as if the metallicity is near solar, as opposed to the 
much lower total metallicity of only three elements. 

This is where the user's adopted solar metallicity :math:`Z_\odot` enters in 
their simulations. Because the element-by-element breakdown of the solar 
composition :math:`Z_{i,\odot}` is taken from Asplund et al. (2009) [1]_, we 
recommend adopting :math:`Z_\odot = 0.014` from their findings for a 
self-consistent scaling. 

The total logarithmic metallicity :math:`[M/H]` relative to the sun is then 
evaluated according to: 

.. math:: [M/H] = \log_{10}\left(\frac{Z}{Z_\odot}\right) = 
	\log_{10}\left(\sum_i Z_i\right) - \log_{10}\left(\sum_i Z_{i,\odot}\right) 

.. note:: These quantities are not recorded with outputs in order to minimize 
	write-out time when the number of elements is high. Instead, ``history`` 
	and ``tracer`` objects evaluate these equations automatically for gas 
	and stars, respectively. 

.. [1] Asplund et al. (2009), ARA&A, 47, 481 

