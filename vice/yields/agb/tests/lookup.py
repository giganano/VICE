"""
Tests the AGB yield grid reader functions at vice/yields/agb/_grid_reader.pyx
"""

from __future__ import print_function
__all__ = [
	"test"
]
from ....core.dataframe._builtin_dataframes import atomic_number
from ...._globals import _RECOGNIZED_ELEMENTS_
from ....testing import moduletest
from ....testing import unittest
from ....testing import generator
from .._grid_reader import yield_grid as grid
from .._grid_reader import _VENTURA13_ELEMENTS_
import numbers


class lookup_generator(generator):

	# Systematically generate unit tests for the AGB yield grid lookup

	@unittest
	def __call__(self):
		def test():
			success = True
			for elem in _RECOGNIZED_ELEMENTS_:
				if (self.kwargs["study"] == "karakas10" and
					atomic_number[elem] > 28): continue
				if (self.kwargs["study"] == "ventura13" and
					elem not in _VENTURA13_ELEMENTS_): continue
				try:
					yields, mass, z = grid(elem, **self.kwargs)
				except:
					return False
				success &= isinstance(mass, tuple)
				success &= isinstance(z, tuple)
				success &= isinstance(yields, tuple)
				success &= all([isinstance(i, tuple) for i in yields])
				success &= all([isinstance(i, numbers.Number) for i in mass])
				success &= all([isinstance(i, numbers.Number) for i in z])
				for i in range(len(yields)):
					success &= all([isinstance(i, numbers.Number) for i in
						yields[i]])
				if not success: break
			return success
		return [self.msg, test]


@moduletest
def test():
	"""
	Run the tests on the AGB yield grid functions
	"""
	return ["vice.yields.agb.grid",
		[
			lookup_generator("Cristallo et al. (2011, 2015)",
				study = "cristallo11")(),
			lookup_generator("Karakas (2010)",
				study = "karakas10")(),
			lookup_generator("Ventura et al. (2013)",
				study = "ventura13")(),
			lookup_generator("Karakas & Lugaro (2016) ; Karakas et al. (2018)",
				study = "karakas16")()
		]
	]

