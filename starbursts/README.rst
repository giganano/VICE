
Johnson & Weinberg (2019) Starbursts Paper Code 
+++++++++++++++++++++++++++++++++++++++++++++++

|paper1| 

..	|paper1| image:: https://img.shields.io/badge/NASA%20ADS-Johnson%20%26%20Weinberg%20(2020)-red
	:target: https://ui.adsabs.harvard.edu/abs/2019arXiv191102598J/abstract 
	:alt: paper1 

Here we provide the python code which runs the simulations and produces 
the figures in `Johnson & Weinberg (2020)`__. Simply running ``make`` in this 
directory will run all the necessary scripts. Alternatively, users can run 
``make starburst`` from VICE's source directory. The figures will be located 
here once the code is finished. Users may also change the timestep size used 
in these simulations by specifying it directly: 

:: 

	$ make TIMESTEP=<desired timestep size> 

By default, the simulations will run with a timestep of 1 Myr. 

__ jw20_ 
.. _jw20: https://ui.adsabs.harvard.edu/abs/2019arXiv191102598J/abstract 

Users are welcome to use the scripts provided here as examples of how to use 
VICE. 
