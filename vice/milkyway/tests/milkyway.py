
from __future__ import absolute_import
__all__ = ["test"]
from ..milkyway import milkyway, mass_from_surface_density
from ..milkyway import _MAX_RADIUS_, _MAX_SF_RADIUS_
from ...toolkit.J21_sf_law import J21_sf_law
from ...toolkit.hydrodisk import hydrodiskstars
from ...toolkit.hydrodisk.data.download import _h277_exists
from ...testing import moduletest
from ...testing import unittest
from ...core.singlezone._singlezone import _RECOGNIZED_MODES_
from ..._globals import _RECOGNIZED_ELEMENTS_
import math as m
import numbers

_TEST_NAME_ = "test"
_TEST_ZONE_WIDTH_ = 0.2


@moduletest
def test():
	r"""
	Run all tests on the milkyway object
	"""
	return ["vice.milkyway",
		[
			test_initialization(),
			test_annuli(),
			test_zone_width(),
			test_mode(),
			test_elements(),
			test_IMF(),
			test_mass_loading(),
			test_dt(),
			test_bins(),
			test_delay(),
			test_RIa(),
			test_smoothing(),
			test_tau_ia(),
			test_m_upper(),
			test_m_lower(),
			test_postMS(),
			test_Z_solar()
		]
	]


@unittest
def test_initialization():
	r"""
	vice.milkyway.__init__ unit test
	"""
	def test():
		if not _h277_exists(): return None
		global _TEST_
		try:
			_TEST_ = milkyway(name = _TEST_NAME_,
				zone_width = _TEST_ZONE_WIDTH_)
		except:
			return False
		status = isinstance(_TEST_, milkyway)
		status &= isinstance(_TEST_.migration.stars, hydrodiskstars)
		if status:
			for i in range(_TEST_.n_zones):
				status &= isinstance(_TEST_.zones[i].func,
					mass_from_surface_density)
				status &= _TEST_.zones[i].Mg0 == 1e-12
				radius = (_TEST_.annuli[i] + _TEST_.annuli[i + 1]) / 2
				if radius <= _MAX_SF_RADIUS_:
					# outside 15.5 kpc, tau_star is just 1.e6
					status &= isinstance(_TEST_.zones[i].tau_star, J21_sf_law)
				else:
					status &= isinstance(_TEST_.zones[i].tau_star,
						numbers.Number)
				for j in _RECOGNIZED_ELEMENTS_:
					status &= _TEST_.zones[i].entrainment.agb[j] == 1 - (
						radius > _MAX_SF_RADIUS_)
					status &= _TEST_.zones[i].entrainment.ccsne[j] == 1 - (
						radius > _MAX_SF_RADIUS_)
					status &= _TEST_.zones[i].entrainment.sneia[j] == 1 - (
						radius > _MAX_SF_RADIUS_)
					if not status: break
				if not status: break
		else: pass
		return status
	return ["vice.milkyway.__init__", test]


@unittest
def test_annuli():
	r"""
	vice.milkyway.annuli unit test
	"""
	def test():
		if not _h277_exists(): return None
		status = True
		for i in range(_TEST_.n_zones - 1):
			# floating point errors cause this to fail with an == comparison
			status &= abs(
				_TEST_.annuli[i + 1] - _TEST_.annuli[i] - _TEST_ZONE_WIDTH_
			) < 1e-10
			if not status: break
		status &= _TEST_.annuli[-1] >= _MAX_RADIUS_
		return status
	return ["vice.milkyway.annuli", test]


@unittest
def test_zone_width():
	r"""
	vice.milkyway.zone_width unit test
	"""
	def test():
		if not _h277_exists(): return None
		return _TEST_.zone_width == _TEST_ZONE_WIDTH_
	return ["vice.milkyway.zone_width", test]


@unittest
def test_mode():
	r"""
	vice.milkyway.mode unit test
	"""
	def test():
		if not _h277_exists(): return None
		status = True
		for i in _RECOGNIZED_MODES_:
			try:
				_TEST_.mode = i
			except:
				status = False
			for j in _TEST_.zones:
				status &= j.mode == i
				if not status: break
			if not status: break
		return status
	return ["vice.milkyway.mode", test]


@unittest
def test_elements():
	r"""
	vice.milkyway.elements unit test
	"""
	def test():
		if not _h277_exists(): return None
		elements = ('n', 'c', 'o')
		try:
			_TEST_.elements = elements
		except:
			return False
		status = True
		for i in _TEST_.zones:
			status &= i.elements == elements
			if not status: break
		return status
	return ["vice.milkyway.elements", test]


@unittest
def test_IMF():
	r"""
	vice.milkyway.IMF unit test
	"""
	def test():
		if not _h277_exists(): return None
		try:
			_TEST_.IMF = "salpeter"
		except:
			return False
		status = True
		for i in _TEST_.zones:
			status &= i.IMF == "salpeter"
			if not status: break
		return status
	return ["vice.milkyway.IMF", test]


@unittest
def test_mass_loading():
	r"""
	vice.milkyway.mass_loading unit test
	"""
	def test():
		if not _h277_exists(): return None
		def testfunc(rgal): # dummy function for testing
			return rgal
		try:
			_TEST_.mass_loading = testfunc
		except:
			return False
		status = _TEST_.mass_loading == testfunc
		for i in range(_TEST_.n_zones):
			status &= _TEST_.zones[i].eta == (
				_TEST_.annuli[i] + _TEST_.annuli[i + 1]) / 2
			if not status: break
		return status
	return ["vice.milkyway.mass_loading", test]


@unittest
def test_dt():
	r"""
	vice.milkyway.dt unit test
	"""
	def test():
		if not _h277_exists(): return None
		test_size = 0.02
		try:
			_TEST_.dt = test_size
		except:
			return False
		status = True
		for i in _TEST_.zones:
			status &= i.dt == test_size
			if not status: break
		return status
	return ["vice.milkyway.dt", test]


@unittest
def test_bins():
	r"""
	vice.milkyway.bins unit test
	"""
	def test():
		if not _h277_exists(): return None
		bins = [-2 + 0.005 * i for i in range(801)]
		try:
			_TEST_.bins = bins
		except:
			return False
		status = True
		for i in _TEST_.zones:
			status &= i.bins == bins
			if not status: break
		return status
	return ["vice.milkyway.bins", test]


@unittest
def test_delay():
	r"""
	vice.milkyway.delay unit test
	"""
	def test():
		if not _h277_exists(): return None
		try:
			_TEST_.delay = 0.05
		except:
			return False
		status = True
		for i in _TEST_.zones:
			status &= i.delay == 0.05
			if not status: break
		return status
	return ["vice.milkyway.delay", test]


@unittest
def test_RIa():
	r"""
	vice.milkyway.RIa unit test
	"""
	def test():
		if not _h277_exists(): return None
		try:
			_TEST_.RIa = "exp"
		except:
			return False
		status = True
		for i in _TEST_.zones:
			status &= i.RIa == "exp"
			if not status: break
		if status:
			def f(t):
				if t < 0.2:
					return 1
				else:
					return m.exp(-(t - 0.2) / 1.4)
			try:
				_TEST_.RIa = f
			except:
				return False
			for i in _TEST_.zones:
				status &= i.RIa == f
				if not status: break
		else: pass
		return status
	return ["vice.milkyway.RIa", test]


@unittest
def test_smoothing():
	r"""
	vice.milkyway.smoothing unit test
	"""
	def test():
		if not _h277_exists(): return None
		try:
			_TEST_.smoothing = 0.5
		except:
			return False
		status = True
		for i in _TEST_.zones:
			status &= i.smoothing == 0.5
			if not status: break
		return status
	return ["vice.milkyway.smoothing", test]


@unittest
def test_tau_ia():
	r"""
	vice.milkyway.tau_ia unit test
	"""
	def test():
		if not _h277_exists(): return None
		try:
			_TEST_.tau_ia = 1.0
		except:
			return False
		status = True
		for i in _TEST_.zones:
			status &= i.tau_ia == 1.0
			if not status: break
		return status
	return ["vice.milkyway.tau_ia", test]


@unittest
def test_m_upper():
	r"""
	vice.milkyway.m_upper unit test
	"""
	def test():
		if not _h277_exists(): return None
		try:
			_TEST_.m_upper = 120
		except:
			return False
		status = True
		for i in _TEST_.zones:
			status &= i.m_upper == 120
			if not status: break
		return status
	return ["vice.milkyway.m_upper", test]


@unittest
def test_m_lower():
	r"""
	vice.milkyway.m_lower unit test
	"""
	def test():
		if not _h277_exists(): return None
		try:
			_TEST_.m_lower = 0.1
		except:
			return False
		status = True
		for i in _TEST_.zones:
			status &= i.m_lower == 0.1
			if not status: break
		return status
	return ["vice.milkyway.m_lower", test]


@unittest
def test_postMS():
	r"""
	vice.milkyway.postMS unit test
	"""
	def test():
		if not _h277_exists(): return None
		try:
			_TEST_.postMS = 0.12
		except:
			return False
		status = True
		for i in _TEST_.zones:
			status &= i.postMS == 0.12
			if not status: break
		return status
	return ["vice.milkyway.postMS", test]


@unittest
def test_Z_solar():
	r"""
	vice.milkyway.Z_solar unit test
	"""
	def test():
		if not _h277_exists(): return None
		try:
			_TEST_.Z_solar = 0.012
		except:
			return False
		status = True
		for i in _TEST_.zones:
			status &= i.Z_solar == 0.012
			if not status: break
		return status
	return ["vice.milkyway.Z_solar", test]

