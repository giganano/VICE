
VICE Example Code 
+++++++++++++++++

First time users of VICE should first go through the `quick start tutorial`__ 
to familiarize themselves with how to use VICE's basic features. 

__ tutorial_ 
.. _tutorial: https://github.com/astrobeard/VICEdev/blob/master/examples/QuickStartTutorial.ipynb

Here we also provide example scripts to help users further familiarize 
themselves with VICE. 

1. `A Simple Example`__: Run a simple onezone model and plot the results 
2. **yields.py**: Modify nucleosynthetic yield settings 
3. **yield_import.py**: Import nucleosynthetic yield settings from another file 
4. **generate_functions.py**: Generate functions for use in simulations 

__ example_ 

Johnson & Weinberg (2020) Starbursts Paper Code 
===============================================

|paper1| 

..	|paper1| image:: https://img.shields.io/badge/NASA%20ADS-Johnson%20%26%20Weinberg%20(2020)-red
	:target: https://ui.adsabs.harvard.edu/abs/2019arXiv191102598J/abstract 
	:alt: paper1 

Included in VICE's source tree is the `code`__ which runs the simulations and 
produces all of the figures in `Johnson & Weinberg (2020)`__. While not 
located in this directory, users are welcome to use it as examples of how to 
use VICE. This code can also be ran by running ``make starburst`` from VICE's 
source directory. 

__ starbursts_ 
__ jw20_ 
.. _starbursts: https://github.com/giganano/VICE/tree/master/starbursts 
.. _jw20: https://ui.adsabs.harvard.edu/abs/2019arXiv191102598J/abstract 

.. _example: 

A Simple Example: A Simulation of a Galaxy with Known Star Formation History 
============================================================================
.. code:: python 

	import matplotlib.pyplot as plt 
	import numpy as np 
	import vice 

	def f(t): 
		"""
		The galaxy's star formation rate in Msun/yr as a function of 
		cosmic time in Gyr. 
		""" 
		return 8.7 * np.exp( -t / 5.2 ) 

	# Give a singlezone object the star formation history, some elements, and 
	# an array of output times in Gyr. 
	sz = vice.singlezone() 
	sz.name = "known_sfh" 
	sz.mode = "sfr" # f now represents star formation rate 
	sz.func = f 
	sz.tau_star = 1.7 # star formation per unit gas supply in yr^-1
	sz.elements = ["mg", "fe", "c", "n", "o", "s", "sr"] 
	sz.run(np.linspace(0, 10, 1001)) 

	# Read in the output holding the time-evolution of the ISM metallicity  
	hist = vice.history("known_sfh") 

	# plot the track in the [Mg/Fe]-[Fe/H] plane 
	plt.plot(hist["[fe/h]"], hist["[mg/fe]"], c = 'k') 
	plt.show() 
	plt.clf() 

	# plot the track in the [N/Mg]-[Mg/H] plane 
	plt.plot(hist["[mg/h]"], hist["[n/mg]"], c = 'k') 
	plt.show()
	plt.clf() 

	# Read in the output holding the stellar metallicity distribution 
	zdist = vice.mdf("known_sfh") 

	# Plot the [O/Fe] stellar probability density 
	bin_centers = [np.mean(i) for i in zip(zdist["bin_edge_left"], 
		zdist["bin_edge_right"])] 
	plt.plot(bin_centers, zdist["dn/d[o/fe]"], c = 'k') 
	plt.show() 
	plt.clf() 

