r"""
Implements testing of the interpolator object in the parent directory.
"""

__all__ = ["test"]
from ...._globals import _RECOGNIZED_ELEMENTS_
from ..interpolator import interpolator
from ....core.dataframe._builtin_dataframes import atomic_number
from ....testing import unittest
from .._grid_reader import _RECOGNIZED_STUDIES_
from .._grid_reader import _VENTURA13_ELEMENTS_


@unittest
def test():
	r"""
	vice.yields.agb.interpolator unit test
	"""
	def test_():
		status = True
		for elem in _RECOGNIZED_ELEMENTS_:
			for study in _RECOGNIZED_STUDIES_:
				# karakas (2010) only goes up to nickel
				if study == "karakas10" and atomic_number[elem] > 28: continue
				# Ventura et al. (2013) only has a few elements
				if (study == "ventura13" and
					elem not in _VENTURA13_ELEMENTS_): continue
				try:
					interp = interpolator(elem, study = study)
				except:
					return None
				for i in range(len(interp.masses)):
					for j in range(len(interp.metallicities)):
						interpolated = interp(interp.masses[i],
							interp.metallicities[j])
						if interp.yields[i][j]:
							percent_diff = abs(
								(interpolated - interp.yields[i][j]) /
								interp.yields[i][j])
						else:
							percent_diff = abs(interpolated)
						status &= percent_diff <= 1.e-10
						if not status: break
					if not status: break
				if not status: break
			if not status: break
		return status
	return ["vice.yields.agb.interpolator", test_]

