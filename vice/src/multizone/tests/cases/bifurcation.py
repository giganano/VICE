r"""
This file implements the gas bifurcation test, which is a two-zone case in
which half of the gas from zone one migrates to zone zero in one timestep
always. Zone one is not star forming, while zone zero is.
"""

from .....core.multizone import multizone
from .....testing import moduletest
from .....testing import unittest

_DT_ = 0.05
_TIMES_ = [0.05 * i for i in range(201)]


@moduletest
def bifurcation_test():
	r"""
	Runs a test in which there is infall onto a quiescent zone and half the gas
	migrates to a star forming zone each timestep. After many timesteps, very
	near one timestep's worth of infall remains in the infalling zone, but
	no stars.
	"""
	msg = "vice.core.multizone edge case : bifurcation"
	try:
		_TEST_ = bifurcation()
	except:
		return [msg, None]
	return [msg,
		[
			_TEST_.mgas(),
			_TEST_.mstar()
		]
	]


class bifurcation(multizone):

	r"""
	Implements the bifurcation test.
	"""

	def __init__(self):
		super().__init__(name = "test", n_zones = 2)
		for i in range(self.n_zones): self.zones[i].dt = _DT_
		self.migration.gas[1][0] = 0.5 / (self.zones[0].dt / 0.01)
		self.zones[1].tau_star = float('inf')
		self.zones[0].func = lambda t: 0
		self.zones[1].func = lambda t: 1
		self.zones[0].Mg0 = 0
		self.zones[1].Mg0 = 0
		self.out = self.run(_TIMES_, overwrite = True, capture = True)


	@unittest
	def mgas(self):
		r"""
		Ensures that the gas mass in zone one at the end of the simulation
		reflects one timestep's worth of infall, and that the final gas mass in
		zone zero is large. After many timesteps of getting half of its gas
		removed, zone 1 should have very near this amount of gas.
		"""
		def test():
			mgas = self.out.zones["zone1"].history["mgas"][-1]
			ifr = 1.e9 * self.out.zones["zone1"].history["ifr"][-1]
			pct_diff = abs((mgas - ifr * self.zones[1].dt) / mgas)
			status = pct_diff <= 1e-3
			status &= (self.out.zones["zone0"].history["mgas"][-1] > 10 *
				self.out.zones["zone1"].history["mgas"][-1])
			return status
		return ["vice.src.multizone.migration.migrate_gas_element", test]


	@unittest
	def mstar(self):
		r"""
		Ensures that the stellar mass in zone zero is non-zero while the
		stellar mass in zone 1 is zero.
		"""
		def test():
			status = self.out.zones["zone0"].history["mstar"][-1] > 1e9
			status &= self.out.zones["zone1"].history["mstar"][-1] == 0
			return status
		return ["vice.src.multizone.multizone.multizone_stellar_mass", test]

