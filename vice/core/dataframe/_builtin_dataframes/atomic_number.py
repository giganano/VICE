"""
This file implements the atomic_number built-in dataframe
"""

from __future__ import absolute_import
from .._elemental_settings import elemental_settings


class atomic_number(elemental_settings):

	r"""
	The VICE dataframe: atomic numbers

	Stores the proton numbers of each recognized element. Stored values are of
	type ``int``.

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
	>>> vice.atomic_number['o']
	8
	>>> vice.atomic_number['fe']
	26
	>>> vice.atomic_number['sr']
	38
	"""

	def __init__(self):
		super().__init__({
			"he": 		2,
			"c":		6,
			"n":		7,
			"o":		8,
			"f":		9,
			"ne":		10,
			"na": 		11,
			"mg":		12,
			"al": 		13,
			"si":		14,
			"p": 		15,
			"s":		16,
			"cl": 		17,
			"ar":		18,
			"k": 		19,
			"ca": 		20,
			"sc":		21,
			"ti": 		22,
			"v": 		23,
			"cr": 		24,
			"mn": 		25,
			"fe":		26,
			"co": 		27,
			"ni": 		28,
			"cu": 		29,
			"zn": 		30,
			"ga": 		31,
			"ge": 		32,
			"as": 		33,
			"se": 		34,
			"br": 		35,
			"kr": 		36,
			"rb": 		37,
			"sr":		38,
			"y":		39,
			"zr": 		40,
			"nb": 		41,
			"mo": 		42,
			"ru": 		44,
			"rh": 		45,
			"pd": 		46,
			"ag": 		47,
			"cd": 		48,
			"in": 		49,
			"sn": 		50,
			"sb": 		51,
			"te": 		52,
			"i": 		53,
			"xe": 		54,
			"cs": 		55,
			"ba":		56,
			"la":		57,
			"ce": 		58,
			"pr": 		59,
			"nd": 		60,
			"sm": 		62,
			"eu":		63,
			"gd": 		64,
			"tb": 		65,
			"dy": 		66,
			"ho": 		67,
			"er": 		68,
			"tm": 		69,
			"yb": 		70,
			"lu": 		71,
			"hf": 		72,
			"ta": 		73,
			"w": 		74,
			"re": 		75,
			"os": 		76,
			"ir": 		77,
			"pt": 		78,
			"au": 		79,
			"hg": 		80,
			"tl":  		81,
			"pb": 		82,
			"bi": 		83
		})


	def __setitem__(self):
		r"""
		Override the __setitem__ function to throw a TypeError whenever this
		function is called.
		"""
		raise TypeError("This dataframe does not support item assignment.")


atomic_number = atomic_number()

