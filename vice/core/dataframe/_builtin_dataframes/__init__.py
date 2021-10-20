r"""
Built-in instances of the VICE dataframe

atomic_number
-------------
Every element's atomic number (number of protons in the nucleus)

primordial
----------
The abundance by mass of each element in primordial gas following big bang
nucleosynthesis

solar_z
-------
The abundance by mass of each element in the sun

sources
-------
The believed dominant sources of enrichment for each element

stable_isotopes
---------------
The mass number (protons + neutrons) of stable isotopes of each element
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:
	__all__ = [
		"atomic_number",
		"primordial",
		"solar_z",
		"sources",
		"stable_isotopes",
		"test"
	]
	from .atomic_number import atomic_number
	from .primordial import primordial
	from .solar_z import solar_z
	from .sources import sources
	from .stable_isotopes import stable_isotopes
	from .tests import test
else:
	pass

