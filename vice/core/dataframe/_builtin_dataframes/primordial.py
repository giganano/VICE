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
	elements with the exception of helium, which is assigned a value of
	:math:`Y_\text{p} = 0.24721 \pm 0.00014` (Pitrou et al. 2021 [1]_).

	.. versionadded:: 1.1.0
		Previous versions of VICE did not implement helium, and therefore did
		not require any information on primordial abundances.

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

	Notes
	-----
	In versions >= 1.3.0, the primordial abundance of helium is taken to be
	:math:`Y_\text{p} = 0.24721 \pm 0.00014` (Pitrou et al. 2021), which updates
	the value of :math:`Y_\text{p} = 0.24672 \pm 0.00017` (Planck Collaboration
	et al. 2016 [2]_; Pitrou et al. 2018 [3]_; Pattie et al. 2018 [4]_) from
	previous versions of VICE based on updates to the neutron lifetime and the
	:math:`\text{D}(p, \gamma)^3\text{He}` reaction.

	Example Code
	------------
	>>> import vice
	>>> vice.primordial['o']
	0.0
	>>> vice.primordial['he']
	0.24721
	>>> vice.primordial['c']
	0.0

	.. [1] Pitrou et al. (2021), MNRAS, 502, 2474
	.. [2] Planck Collaboration et al. (2016), A&A, 594, A13
	.. [3] Pitrou et al. (2018), Phys. Rep., 754, 1
	.. [4] Pattie et al. (2018), Science, 360, 627
	"""

	def __init__(self):
		data = {}
		for elem in _RECOGNIZED_ELEMENTS_:
			if elem == "he":
				value = 0.24721
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

