"""
In this file we demonstrate how to change VICE's nucleosynthetic yield
settings.

This file also serves as a demonstration of how these settings can be
declared in a .py file and subsequently imported - run "import yields" in
this directory and your nucleosynthetic yield settings will reflect this file.
"""

import vice

# to modify your yields from ccsne
vice.yields.ccsne.settings["o"] = 0.015
vice.yields.ccsne.settings["fe"] = 0.0012

def f(z):
	"""
	A function of metallicity Z, which we will set as the yield of Sr from
	core-collapse supernovae.
	"""
	return 3.5e-8 * (z / 0.014)

vice.yields.ccsne.settings["sr"] = f

# to modify your yields from sneia
vice.yields.sneia.settings["o"] = 0.0
vice.yields.sneia.settings["fe"] = 0.0017
vice.yields.sneia.settings["sr"] = 0.0

# to modify your yields from agb stars
# these must be either a string for a built-in table or a function of stellar
# mass and metallicity, respectively.
def g(m, z):
	"""
	A function of mass and metallicity which returns 0 always.
	"""
	return 0.0

vice.yields.agb.settings["o"] = g # no oxygen from AGB stars
vice.yields.agb.settings["c"] = "karakas10" # Karakas (2010)
vice.yields.agb.settings["sr"] = "cristallo11" # Cristallo et al. (2011)
vice.yields.agb.settings["fe"] = lambda m, z: 0.0 # The same as the function g

