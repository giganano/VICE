"""
This file implements the stable_isotopes built-in dataframe
"""

from __future__ import absolute_import
from .._elemental_settings import elemental_settings
import os


class stable_isotopes(elemental_settings):

	r"""
	The VICE dataframe: stable isotopes

	The mass number (protons and neutrons) of the stable isotopes of each
	element. Stored values are of type ``list``, elements of which are of type
	``int``.

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
	>>> vice.stable_isotopes['he']
	[3, 4]
	>>> vice.stable_isotopes['o']
	[16, 17, 18]
	>>> vice.stable_isotopes['fe']
	[54, 56, 57, 58]
	"""

	def __init__(self):
		fname = "%s/stable_isotopes.dat" % (os.path.dirname(os.path.abspath(__file__)))
		out = {}
		with open(fname, 'r') as f:
			for line in f:
				if line.startswith("#"):
					continue
				data = line.split()
				ele = data[0].lower()
				masses = [int(m) for m in data[1:]]
				out[ele] = masses
		super().__init__(out)


	def __setitem__(self, key, value):
		r"""
		Override the __setitem__ function to throw a TypeError whenever this
		function is called.
		"""
		raise TypeError("This dataframe does not support item assignment.")


stable_isotopes = stable_isotopes()

