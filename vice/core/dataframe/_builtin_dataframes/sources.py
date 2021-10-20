"""
This file implements the sources built-in dataframe
"""

from __future__ import absolute_import
from .._elemental_settings import elemental_settings


class sources(elemental_settings):

	r"""
	The VICE dataframe: nucleosynthetic sources

	Stores the dominant astrophysical enrichment channels of each element.
	These values are adopted from Johnson (2019) [1]_. Stored values are of
	type ``list``, elements of which are of type ``str``.

		- "BBN": Big Bang Nucleosynthesis
			A statistically significant portion of this element's present-day
			abundances was present prior to the onset of star formation in the
			universe.
		- "CCSNE": Core Collapse Supernovae
			A statistically significant portion of this element's present-day
			abundances is due to massive star explosions.
		- "SNEIA": Type Ia Supernovae
			A statistically significant portion of this element's present-day
			abundances is due to white dwarf explosions.
		- "AGB": Asymptotic Giant Branch Stars
			A statistically significant portion of this element's present-day
			abundances is due to synthesis in AGB stars.
		- "NSNS": Neutron Star Mergers, R-process Nucleosynthesis
			A statistically significant portion of this element's present-day
			abundances is due to neutron star mergers, or other astrophysical
			sites of r-process nucleosynthesis.

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
	>>> vice.sources['o']
	["CCSNE"]
	>>> vice.sources['he']
	["BBN", "CCSNE", "AGB"]
	>>> vice.sources['fe']
	["CCSNE", "SNEIA"]

	.. [1] Johnson (2019), Science, 363, 474
	"""

	def __init__(self):
		super().__init__({
			"he": 		["BBN", "CCSNE", "AGB"],
			"c":		["CCSNE", "AGB"],
			"n":		["CCSNE", "AGB"],
			"o":		["CCSNE"],
			"f": 		["CCSNE"],
			"ne":		["CCSNE"],
			"na":		["CCSNE"],
			"mg":		["CCSNE"],
			"al":		["CCSNE"],
			"si":		["CCSNE", "SNEIA"],
			"p":		["CCSNE", "SNEIA"],
			"s":		["CCSNE", "SNEIA"],
			"cl":		["CCSNE", "SNEIA"],
			"ar":		["CCSNE", "SNEIA"],
			"k": 		["CCSNE", "SNEIA"],
			"ca": 		["CCSNE", "SNEIA"],
			"sc": 		["CCSNE", "SNEIA"],
			"ti": 		["CCSNE", "SNEIA"],
			"v": 		["CCSNE", "SNEIA"],
			"cr": 		["CCSNE", "SNEIA"],
			"mn": 		["CCSNE", "SNEIA"],
			"fe":		["CCSNE", "SNEIA"],
			"co": 		["CCSNE", "SNEIA"],
			"ni": 		["CCSNE", "SNEIA"],
			"cu": 		["CCSNE", "SNEIA"],
			"zn": 		["CCSNE", "SNEIA"],
			"ga": 		["CCSNE"],
			"ge": 		["CCSNE"],
			"as": 		["CCSNE"],
			"se": 		["CCSNE"],
			"br":		["CCSNE"],
			"kr": 		["CCSNE"],
			"rb": 		["CCSNE"],
			"sr":		["CCSNE", "AGB"],
			"y":		["CCSNE", "AGB"],
			"zr": 		["CCSNE", "AGB"],
			"nb": 		["AGB", "NSNS"],
			"mo": 		["AGB", "NSNS"],
			"ru": 		["AGB", "NSNS"],
			"rh":		["AGB", "NSNS"],
			"pd": 		["AGB", "NSNS"],
			"ag": 		["AGB", "NSNS"],
			"cd": 		["AGB", "NSNS"],
			"in": 		["AGB", "NSNS"],
			"sn": 		["AGB", "NSNS"],
			"sb":		["AGB", "NSNS"],
			"te": 		["AGB", "NSNS"],
			"i": 		["AGB", "NSNS"],
			"xe": 		["AGB", "NSNS"],
			"cs": 		["AGB", "NSNS"],
			"ba":		["AGB", "NSNS"],
			"la":		["AGB", "NSNS"],
			"ce": 		["AGB", "NSNS"],
			"pr": 		["AGB", "NSNS"],
			"nd": 		["AGB", "NSNS"],
			"sm": 		["AGB", "NSNS"],
			"eu":		["AGB", "NSNS"],
			"gd": 		["AGB", "NSNS"],
			"tb": 		["AGB", "NSNS"],
			"dy": 		["AGB", "NSNS"],
			"ho": 		["AGB", "NSNS"],
			"er": 		["AGB", "NSNS"],
			"tm": 		["AGB", "NSNS"],
			"yb": 		["AGB", "NSNS"],
			"lu": 		["AGB", "NSNS"],
			"hf": 		["AGB", "NSNS"],
			"ta": 		["AGB", "NSNS"],
			"w": 		["AGB", "NSNS"],
			"re": 		["AGB", "NSNS"],
			"os": 		["AGB", "NSNS"],
			"ir": 		["AGB", "NSNS"],
			"pt": 		["AGB", "NSNS"],
			"au": 		["AGB", "NSNS"],
			"hg":		["AGB", "NSNS"],
			"tl": 		["AGB", "NSNS"],
			"pb": 		["AGB", "NSNS"],
			"bi": 		["AGB", "NSNS"]
		})


	def __setitem__(self, key, value):
		r"""
		Override the __setitem__ function to throw a TypeError whenever this
		function is called.
		"""
		raise TypeError("This dataframe does not support item assignment.")


sources = sources()

