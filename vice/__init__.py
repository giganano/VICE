"""
VICE: Versatile Integrator for Chemical Evolution
=================================================
A software built for numerical integration of single-zone chemical evolution 
models. 

See LICENSE for copyright information and citation requirements. 
Documentation for this package is available in several forms: 
	1) In the docstrings of the objects and functions
	2) In the git repository for this project: URL HERE
	3) In the appendix of the associated publication 
	   Johnson & Weinberg (2018, in prep)
Within the git repository the user will find example and template scripts to 
guide them through getting started with this software. 

In all docstrings, examples of code are represented by three > signs:

	>>> a = 5
	>>> a += 10

The majority of the power of this module is in the "integrator" class, which 
runs numerical simulations of chemical enrichment of galaxies under the single 
zone approximation, and is designed to do so for arbitrarily complex models. 
It is able to do this by allowing the user to specify callable functions of 
time for its attributes. See the docstrings of this class and its attributes 
for details and instructions on how to do so. If the user were to only use the 
integrator object, they would still have the full versatility of the chemical 
evolution functions included here. 

However, in addition to this, the class "output" is included. It is designed 
explicitly for reading in the output of the "integrator" class and presenting 
it to the user in the form of dataframes callable either by column label or 
row number. Calling these dataframes by column labels is case-insensitive. 

Also included in this package are several look-up functions for the convenience 
of the user. They are scaled-down implementations of the same case-insensitive 
dataframes are included in the output class. They are named "solar_z", 
"sources", "ccsne_yields", and "sneia_yields", and they are meant for the user 
to lookup background information on certain elements. "solar_z" will tell the 
user the mass fraction of each element found in the sun. "sources" describes 
the astrophysical channels through which each element is synthesized. 
"ccsne_yields" tell the user the IMF-integrated fractional yield of each 
element produced by core-collapse supernovae (CCSNe). Lastly, "sneia_yields" 
tell the user the IMF-integrated fractional yield of each element produced by 
Type Ia supernovae (SNe Ia). The user may simply call todict() on these 
objects as well to receive them in Pythin dictionary format. 

The interactive visualization features of the output dataframe object (see 
output.show docstring for details) are implemented using matplotlib. 
There for, if the user wishes to use these built-in features, an installation 
of either matplotlib or Anaconda is required. 

The integration features themselves, however, are NumPy- and Pandas- 
compatible, but neither NumPy- nor Pandas-dependent. That is, when imported, 
this software will attempt to import NumPy and Pandas, but if either are not 
found in the user's system, then it will move on assuming that the user will 
not be using their object types. When given NumPy and Pandas object types, it 
will immediately convert them into Python objects or native C-types, depending 
on the attribute being specified. Therefore, the functions that run the 
chemical enrichment integration itself are completely independent of the 
version of Anaconda. 
"""

from __future__ import absolute_import

__version__ = "1.0.0"
__author__ = "James Johnson <giganano9@gmail.com>"

from .core import *
from .data import *
