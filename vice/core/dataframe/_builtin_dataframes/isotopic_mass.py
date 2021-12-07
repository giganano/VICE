"""
This file implements the isotopic_mass built-in dataframe
"""

from __future__ import absolute_import
from ...._globals import _RECOGNIZED_ELEMENTS_
from ...._globals import _RECOGNIZED_ISOTOPES_
from .._elemental_settings import elemental_settings
from .._base import base
import os


class isotopic_mass(elemental_settings):

	r"""
	The VICE dataframe: isotopic masses

	Stores the mass of each recognized isotope. Stored values are of
	type ``float``.

	Indexing
	--------
	- ``str`` [case-insensitive]
		The symbol of a chemical element as it appears on the periodic table.
	- ``str`` [case-insensitive]
		The symbol of a chemical element as it appears on the periodic table,
		followed by its mass number.

	Item Assignment
	---------------
	This instance of the VICE dataframe does not support item assignment.

	Functions
	---------
	- keys
	- todict

	Example Code
	------------
	>>> import vice
	>>> vice.isotopic_mass['he']
	vice.dataframe{
		he3 ------------> 3.0160293201
		he4 ------------> 4.00260325413
		he5 ------------> 5.012057
		he6 ------------> 6.018885891
		he7 ------------> 7.0279907
		he8 ------------> 8.03393439
		he9 ------------> 9.043946
		he10 -----------> 10.05279
	}
	>>> vice.isotopic_mass['o']['o16']
	15.99491461957
	>>> vice.isotopic_mass['fe']['fe52']
	51.9481131

	.. [1] Wang et al. (2012), Chinese Phys. C, 36, 1603
	"""

	def __init__(self):
		fname = "%s/isotopic_mass.dat" % (os.path.dirname(os.path.abspath(__file__)))
		out = {ele: {} for ele in _RECOGNIZED_ELEMENTS_}
		with open(fname, 'r') as f:
			for line in f:
				if line.startswith("#"):
					continue
				data = line.split()
				iso = data[0].lower()
				if iso not in _RECOGNIZED_ISOTOPES_:
					continue
				ele = "".join(["" if c in "0123456789" else c for c in iso])
				mass = float(data[1])
				out[ele][iso] = mass
		super().__init__(out)
		for ele in _RECOGNIZED_ELEMENTS_:
			super().__setitem__(ele, base(self[ele]))


	def __setitem__(self):
		r"""
		Override the __setitem__ function to throw a TypeError whenever this
		function is called.
		"""
		raise TypeError("This dataframe does not support item assignment.")


isotopic_mass = isotopic_mass()
