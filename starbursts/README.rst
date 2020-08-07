
Johnson & Weinberg (2020) Starbursts Paper Code 
+++++++++++++++++++++++++++++++++++++++++++++++

|paper1| |paper2| 

..	|paper1| image:: https://img.shields.io/badge/NASA%20ADS-Johnson%20%26%20Weinberg%20(2020)-red
	:target: https://arxiv.org/abs/1911.02598
	:alt: paper1 

.. 	|paper2| image:: https://img.shields.io/badge/NASA%20ADS-Kirby%20et%20al.%20(2010)-red
	:target: https://ui.adsabs.harvard.edu/abs/2010ApJS..191..352K/abstract 
	:alt: paper2 

Here we provide the python code which runs the simulations and produces 
the figures in `Johnson & Weinberg (2020)`__. Simply running ``make`` in this 
directory will run all the necessary scripts. Alternatively, users can run 
``make starburst`` from the parent directory. The figures will be located 
here once the code is finished. Users may also change the timestep size used 
in these simulations by specifying its value in Gyr directly: 

:: 

	$ make TIMESTEP=<desired timestep size> 

By default, the simulations will run with a timestep of 1 Myr. 

__ jw20_ 
.. _jw20: https://arxiv.org/abs/1911.02598 

Also included here is the employed data from `Kirby et al. (2010)`__. The 
final sample from Appendix A of `Johnson & Weinberg (2020)`__ is located 
here in an ascii text format at ``data/kirby2010processed.dat``. 

__ k10_ 
__ jw20_ 
.. _k10: https://ui.adsabs.harvard.edu/abs/2010ApJS..191..352K/abstract
