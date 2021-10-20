"""
This file implements the primordial built-in dataframe
"""

from __future__ import absolute_import
from ...._globals import _RECOGNIZED_ELEMENTS_
from .._elemental_settings import elemental_settings


class primordial(elemental_settings):

	r"""
	The VICE dataframe: primordial abundances

	Stores the abundance by mass of each element following big bang
	nucleosynthesis. Stored values are of type ``float``, and are zero for all
	elements with the exception of helium, which is assigned the standard model
	value of :math:`Y_\text{p} = 0.24672 \pm 0.00017` [1]_ [2]_ [3]_.

	.. versionadded:: 1.1.0

	Indexing
	--------
	- ``str`` [case-insensitive]
		The symbol of a chemical element as it appears on the periodic table.

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
	>>> vice.primordial['o']
	0.0
	>>> vice.primordial['he']
	0.24672
	>>> vice.primordial['c']
	0.0

	.. [1] Planck Collaboration et al. (2016), A&A, 594, A13
	.. [2] Pitrou et al. (2018), Phys. Rep., 754, 1
	.. [3] Pattie et al. (2018), Science, 360, 627
	"""

	def __init__(self):
		data = {}
		for elem in _RECOGNIZED_ELEMENTS_:
			if elem == "he":
				value = 0.24672
			else:
				value = 0.0
			data[elem] = value
		super().__init__(data)


	def __setitem__(self, key, value):
		r"""
		Override the __setitem__ function to throw a TypeError whenever this
		function is called.
		"""
		raise TypeError("This dataframe does not support item assignment.")


primordial = primordial()

