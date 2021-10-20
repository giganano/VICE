"""
This file implements the stable_isotopes built-in dataframe
"""

from __future__ import absolute_import
from .._elemental_settings import elemental_settings


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
		super().__init__({
			"he": 		[3, 4],
			"c":		[12, 13],
			"n":		[14, 15],
			"o":		[16, 17, 18],
			"f":		[19],
			"ne":		[20, 21, 22],
			"na":		[23],
			"mg":		[24, 25, 26],
			"al":		[27],
			"si":		[28, 29, 30],
			"p":		[31],
			"s":		[32, 33, 34, 36],
			"cl":		[35, 37],
			"ar":		[36, 38, 40],
			"k":		[39, 41],
			"ca":		[40, 42, 43, 44, 46],
			"sc":		[45],
			"ti":		[46, 47, 48, 49, 50],
			"v":		[51],
			"cr":		[50, 52, 53, 54],
			"mn":		[55],
			"fe":		[54, 56, 57, 58],
			"co":		[59],
			"ni":		[58, 60, 61, 62, 64],
			"cu":		[63, 65],
			"zn":		[64, 66, 67, 68, 70],
			"ga":		[69, 71],
			"ge":		[70, 72, 73, 74],
			"as":		[75],
			"se":		[74, 76, 77, 78, 80],
			"br":		[79, 81],
			"kr":		[80, 82, 83, 84, 86],
			"rb":		[85],
			"sr":		[84, 86, 87, 88],
			"y":		[89],
			"zr":		[90, 91, 92, 94],
			"nb":		[93],
			"mo":		[92, 94, 95, 96, 97, 98],
			"ru":		[96, 98, 99, 100, 101, 102, 104],
			"rh":		[103],
			"pd":		[102, 104, 105, 106, 108, 110],
			"ag":		[107, 109],
			"cd":		[106, 108, 110, 111, 112, 114],
			"in":		[113],
			"sn":		[112, 114, 115, 116, 117, 118, 119, 120, 122, 124],
			"sb":		[121, 123],
			"te":		[120, 122, 123, 124, 125, 126],
			"i":		[127],
			"xe":		[126, 128, 129, 130, 131, 132, 134],
			"cs":		[133],
			"ba":		[132, 134, 135, 136, 137, 138],
			"la":		[139],
			"ce":		[136, 138, 140, 142],
			"pr":		[141],
			"nd":		[142, 143, 145, 146, 148],
			"sm":		[144, 149, 150, 152, 154],
			"eu":		[153],
			"gd":		[154, 155, 156, 157, 158, 160],
			"tb":		[159],
			"dy":		[156, 158, 160, 161, 162, 163, 164],
			"ho":		[165],
			"er":		[162, 164, 166, 167, 168, 170],
			"tm":		[169],
			"yb":		[168, 170, 171, 172, 173, 174, 176],
			"lu":		[175],
			"hf":		[176, 177, 178, 179, 180],
			"ta":		[181],
			"w":		[182, 183, 184, 186],
			"re":		[185],
			"os":		[184, 187, 188, 189, 190, 192],
			"ir":		[191, 193],
			"pt":		[192, 194, 195, 196, 198],
			"au":		[197],
			"hg":		[196, 198, 199, 200, 201, 202, 204],
			"tl":		[203, 205],
			"pb":		[204, 206, 207, 208],
			"bi":		[209]
		})


	def __setitem__(self, key, value):
		r"""
		Override the __setitem__ function to throw a TypeError whenever this
		function is called.
		"""
		raise TypeError("This dataframe does not support item assignment.")


stable_isotopes = stable_isotopes()

