""" 
Built-in instances of the VICE dataframe 

atomic_number 
============= 
Every element's atomic number (number of protons in the nucleus) 

primordial 
========== 
The abundance by mass of each element in primordial gas following big bang 
nucleosynthesis 

solar_z 
======= 
The abundance by mass of each element in the sun 

sources 
======= 
The believed dominant sources of enrichment for each element 

stable_isotopes 
=============== 
The mass number (protons + neutrons) of stable isotopes of each element 
""" 

from __future__ import absolute_import 
__all__ = ["atomic_number", "primordial", "solar_z", "sources"] 
from ._atomic_number import atomic_number 
from ._primordial import primordial 
from ._solar_z import solar_z 
from ._sources import sources 
from ._stable_isotopes import stable_isotopes 

