
__all__ = [
	"test",
	"test_powerlaw",
	"test_vincenzo2016",
	"test_hpt2000",
	"test_ka1997",
	"test_pm1993",
	"test_mm1989",
	"test_larson1974"
]
from ...testing import moduletest
from ...testing import unittest
from ..mlr import mlr

_POSTMS_TEST_VALUES_ = [0.01 * _ for _ in range(16)]
_Z_TEST_VALUES_ = [0.001 * _ for _ in range(21)]
_TEST_MASSES_ = [0.01 * i for i in range(1, 1001)]
_TEST_TIMES_ = [0.01 * i for i in range(751)]


@moduletest
def test():
	r"""
	Runs the unit tests on VICE's mass-lifetime relation calculations.
	"""
	return ["vice.mlr",
		[
			test_setting(),
			test_powerlaw(run = False),
			test_vincenzo2016(run = False),
			test_hpt2000(run = False),
			test_ka1997(run = False),
			test_pm1993(run = False),
			test_mm1989(run = False),
			test_larson1974(run = False)
		]
	]


@unittest
def test_setting():
	r"""
	Tests the mass-lifetime relation global setting assignment function.
	"""
	def test():
		result = True
		try:
			current = mlr.setting # don't modify the current setting
		except:
			return False
		for value in mlr.recognized:
			try:
				mlr.setting = value
			except:
				return False
			result &= mlr.setting == value
			if not result: break
		try:
			mlr.setting = current # don't modify the current setting
		except:
			return False
		return result
	return ["vice.mlr.setting", test]


@moduletest
def test_powerlaw():
	r"""
	Tests the power-law mass lifetime relation.
	"""
	return ["vice.mlr.powerlaw",
		[
			test_powerlaw_turnoffmass_monotonicity(),
			test_powerlaw_lifetime_monotonicity()
		]
	]


@unittest
def test_powerlaw_turnoffmass_monotonicity():
	r"""
	Tests the power-law mass-lifetime relation for monotonicity in the turnoff
	mass as a function of age.
	"""
	def test():
		result = True
		for postMS in _POSTMS_TEST_VALUES_:
			result &= turnoffmass_monotonicity(mlr.powerlaw, postMS = postMS)
			if not result: break
		return result
	return ["vice.mlr.powerlaw [turnoff mass monotonicity]", test]


@unittest
def test_powerlaw_lifetime_monotonicity():
	r"""
	Tests the power-law mass-lifetime relation for monotonicity in the lifetime
	as a function of stellar mass.
	"""
	def test():
		result = True
		for postMS in _POSTMS_TEST_VALUES_:
			result &= lifetime_monotonicity(mlr.powerlaw, postMS = postMS)
			if not result: break
		return result
	return ["vice.mlr.powerlaw [lifetime monotonicity]", test]


@moduletest
def test_vincenzo2016():
	r"""
	Tests on the Vincenzo et al. (2016) [1]_ mass-lifetime relation.

	.. [1] Vincenzo et al. (2016), MNRAS, 460, 2238
	"""
	return ["vice.mlr.vincenzo2016",
		[
			test_vincenzo2016_turnoffmass_monotonicity(),
			test_vincenzo2016_lifetime_monotonicity(),
			test_vincenzo2016_lifetime_minimum()
		]
	]


@unittest
def test_vincenzo2016_turnoffmass_monotonicity():
	r"""
	Test the Vincenzo et al. (2016) [1]_ mass-lifetime relation for
	monotonicity in the turnoff mass as a function of age.

	.. [1] Vincenzo et al. (2016), MNRAS, 460, 2238
	"""
	def test():
		result = True
		for Z in _Z_TEST_VALUES_:
			result &= turnoffmass_monotonicity(mlr.vincenzo2016, Z = Z)
			if not result: break
		return result
	return ["vice.mlr.vincenzo2016 [turnoff mass monotonicity]", test]


@unittest
def test_vincenzo2016_lifetime_monotonicity():
	r"""
	Test the Vincenzo et al. (2016) [1]_ mass-lifetime relation for
	monotonicity in the stellar lifetimes as a function of mass.

	.. [1] Vincenzo et al. (2016), MNRAS, 460, 2238
	"""
	def test():
		result = True
		for Z in _Z_TEST_VALUES_:
			result &= lifetime_monotonicity(mlr.vincenzo2016, Z = Z)
			if not result: break
		return result
	return ["vice.mlr.vincenzo2016 [lifetime monotonicity]", test]


@unittest
def test_vincenzo2016_lifetime_minimum():
	r"""
	Test the Vincenzo et al. (2016) [1]_ mass-lifetime relation against the
	minimum lifetime of 3 Myr.

	.. [1] Vincenzo et al. (2016), MNRAS, 460, 2238
	"""
	def test():
		result = True
		for Z in _Z_TEST_VALUES_:
			# Vincenzo et al. (2016) predict t -> 1 Myr at high masses at
			# Z = 0 as opposed to t -> 3 Myr.
			result &= lifetime_minimum(mlr.vincenzo2016,
				minimum = 0.003 if Z else 0.001, Z = Z)
		return result
	return ["vice.mlr.vincenzo2016 [minimum lifetime]", test]


@moduletest
def test_hpt2000():
	r"""
	Tests on the Hurley, Pols & Tout (2000) [1]_ mass-lifetime relation.

	.. [1] Hurley, Pols & Tout (2000), MNRAS, 315, 543
	"""
	return ["vice.mlr.hpt2000",
		[
			test_hpt2000_turnoffmass_monotonicity(),
			test_hpt2000_lifetime_monotonicity(),
			test_hpt2000_lifetime_minimum()
		]
	]


@unittest
def test_hpt2000_turnoffmass_monotonicity():
	r"""
	Test the Hurley, Pols & Tout (2000) [1]_ mass-lifetime relation for
	monotonicity in the turnoff mass as a function of stellar age.

	.. [1] Hurley, Pols & Tout (2000), MNRAS, 315, 543
	"""
	def test():
		result = True
		for Z in _Z_TEST_VALUES_:
			for postMS in _POSTMS_TEST_VALUES_:
				result &= turnoffmass_monotonicity(mlr.hpt2000, Z = Z,
					postMS = postMS)
				if not result: break
			if not result: break
		return result
	return ["vice.mlr.hpt2000 [turnoff mass monotonicity]", test]


@unittest
def test_hpt2000_lifetime_monotonicity():
	r"""
	Test the Hurley, Pols & Tout (2000) [1]_ mass-lifetime relation for
	monotonicity in the lifetimes as a function of stellar mass.

	.. [1] Hurley, Pols & Tout (2000), MNRAS, 315, 543
	"""
	def test():
		result = True
		for Z in _Z_TEST_VALUES_:
			for postMS in _POSTMS_TEST_VALUES_:
				result &= lifetime_monotonicity(mlr.hpt2000, Z = Z,
					postMS = postMS)
				if not result: break
			if not result: break
		return result
	return ["vice.mlr.hpt2000 [lifetime monotonicity]", test]


@unittest
def test_hpt2000_lifetime_minimum():
	r"""
	Test the Hurley, Pols & Tout (2000) [1]_ mass-lifetime relation against
	the minimum lifetime of 3 Myr.

	.. [1] Hurley, Pols & Tout (2000), MNRAS, 315, 543
	"""
	def test():
		result = True
		for Z in _Z_TEST_VALUES_:
			for postMS in _POSTMS_TEST_VALUES_:
				result &= lifetime_minimum(mlr.hpt2000, Z = Z, postMS = postMS)
				if not result: break
			if not result: break
		return result
	return ["vice.mlr.hpt2000 [lifetime minimum]", test]


@moduletest
def test_ka1997():
	r"""
	Tests on the Kodama & Arimoto (1997) [1]_ mass-lifetime relation.

	.. [1] Kodama & Aritmoto (1997), A&A, 320, 41
	"""
	return ["vice.mlr.ka1997",
		[
			test_ka1997_turnoffmass_monotonicity(),
			test_ka1997_lifetime_monotonicity(),
			test_ka1997_lifetime_minimum()
		]
	]


@unittest
def test_ka1997_turnoffmass_monotonicity():
	r"""
	Test the Kodama & Arimoto (1997) [1]_ mass-lifetime relation for
	monotonicity in the turnoff mass as a function of stellar age.

	.. [1] Kodama & Arimoto (1997), A&A, 320, 41
	"""
	def test():
		result = True
		for Z in _Z_TEST_VALUES_:
			result &= turnoffmass_monotonicity(mlr.ka1997, Z = Z)
			if not result: break
		return result
	return ["vice.mlr.ka1997 [turnoff mass monotonicity]", test]


@unittest
def test_ka1997_lifetime_monotonicity():
	r"""
	Test the Kodama & Arimoto (1997) [1]_ mass-lifetime relation for
	monotonicity in the stellar lifetimes as a function of mass.

	.. [1] Kodama & Arimoto (1997), A&A, 320, 41
	"""
	def test():
		result = True
		for Z in _Z_TEST_VALUES_:
			result &= lifetime_monotonicity(mlr.ka1997, Z = Z)
			if not result: break
		return result
	return ["vice.mlr.ka1997 [lifetime monotonicity]", test]


@unittest
def test_ka1997_lifetime_minimum():
	r"""
	Test the Kodama & Arimoto (1997) [1]_ mass-lifetime relation against the
	minimum lifetime of 3 Myr.

	.. [1] Kodama & Arimoto (1997), A&A, 320, 41
	"""
	def test():
		result = True
		for Z in _Z_TEST_VALUES_:
			result &= lifetime_minimum(mlr.ka1997, Z = Z,
				minimum = 0.001 if Z <= 0.003 else 0.003)
			if not result: break
		return result
	return ["vice.mlr.ka1997 [lifetime minimum]", test]


@moduletest
def test_pm1993():
	r"""
	Tests on the Padovani & Matteucci (1993) [1]_ mass-lifetime relation.

	.. [1] Padovani & Matteucci (1993), ApJ, 416, 26
	"""
	return ["vice.mlr.pm1993",
		[
			test_pm1993_turnoffmass_monotonicity(),
			test_pm1993_lifetime_monotonicity(),
			test_pm1993_lifetime_minimum()
		]
	]


@unittest
def test_pm1993_turnoffmass_monotonicity():
	r"""
	Test the Padovani & Matteucci (1993) [1]_ mass-lifetime relation for
	monotonicity in the turnoff masses as a function of stellar age.

	.. [1] Padovani & Matteucci (1993), ApJ, 416, 26
	"""
	def test():
		result = True
		for postMS in _POSTMS_TEST_VALUES_:
			result &= turnoffmass_monotonicity(mlr.pm1993, postMS = postMS)
			if not result: break
		return result
	return ["vice.mlr.pm1993 [turnoff mass monotonicity]", test]


@unittest
def test_pm1993_lifetime_monotonicity():
	r"""
	Test the Padovani & Matteucci (1993) [1]_ mass-lifetime relation for
	monotonicity in the lifetimes as a function of stellar mass.

	.. [1] Padovani & Matteucci (1993), ApJ, 416, 26
	"""
	def test():
		result = True
		for postMS in _POSTMS_TEST_VALUES_:
			result &= lifetime_monotonicity(mlr.pm1993, postMS = postMS)
			if not result: break
		return result
	return ["vice.mlr.pm1993 [lifetime monotonicity]", test]


@unittest
def test_pm1993_lifetime_minimum():
	r"""
	Test the Padovani & Matteucci (1993) [1]_ mass-lifetime relation against
	the minimum lifetime of 3 Myr.

	.. [1] Padovani & Matteucci (1993), ApJ, 416, 26
	"""
	def test():
		result = True
		for postMS in _POSTMS_TEST_VALUES_:
			result &= lifetime_minimum(mlr.pm1993, postMS = postMS)
			if not result: break
		return result
	return ["vice.mlr.pm1993 [lifetime minimum]", test]


@moduletest
def test_mm1989():
	r"""
	Tests on the Maeder & Meynet (1989) [1]_ mass-lifetime relation.

	.. [1] Maeder & Meynet (1989), A&A, 210, 155
	"""
	return ["vice.mlr.mm1989",
		[
			test_mm1989_turnoffmass_monotonicity(),
			test_mm1989_lifetime_monotonicity(),
			test_mm1989_lifetime_minimum()
		]
	]


@unittest
def test_mm1989_turnoffmass_monotonicity():
	r"""
	Test the Maeder & Meynet (1989) [1]_ mass-lifetime relation for
	monotonicity in the turnoff mass as a function of stellar age.

	.. [1] Maeder & Meynet (1989), A&A, 210, 155
	"""
	def test():
		result = True
		for postMS in _POSTMS_TEST_VALUES_:
			result &= turnoffmass_monotonicity(mlr.mm1989, postMS = postMS)
			if not result: break
		return result
	return ["vice.mlr.mm1989 [turnoffmass monotonicity]", test]


@unittest
def test_mm1989_lifetime_monotonicity():
	r"""
	Test the Maeder & Meynet (1989) [1]_ mass-lifetime relation for
	monotonicity in the lifetime as a function of stellar mass.

	.. [1] Maeder & Meynet (1989), A&A, 210, 155
	"""
	def test():
		result = True
		global _TEST_MASSES_ # prevents UnboundLocalError
		# positions of known breaks in the monotonicity, small enough to not
		# worry about in chemical evolution models as implemented in VICE
		_TEST_MASSES_ = [_ for _ in _TEST_MASSES_ if not (
			7.0 <= _ <= 7.16 or _ >= 60.0)]
		for postMS in _POSTMS_TEST_VALUES_:
			result &= lifetime_monotonicity(mlr.mm1989, postMS = postMS)
			if not result: break
		_TEST_MASSES_ = [0.01 * i for i in range(1, 10001)]
		return result
	return ["vice.mlr.mm1989 [lifetime monotonicity]", test]


@unittest
def test_mm1989_lifetime_minimum():
	r"""
	Test the Maeder & Meynet [1]_ mass-lifetime relation against the
	minimum lifetime of 3 Myr.

	.. [1] Maeder & Meynet (1989), A&A, 210, 155
	"""
	def test():
		result = True
		for postMS in _POSTMS_TEST_VALUES_:
			result &= lifetime_minimum(mlr.mm1989, postMS = postMS)
			if not result: break
		return result
	return ["vice.mlr.mm1989 [lifetime minimum]", test]


@moduletest
def test_larson1974():
	r"""
	Tests on the Larson (1974) [1]_ mass-lifetime relation.

	.. [1] Larson (1974), MNRAS, 166, 585
	"""
	return ["vice.mlr.larson1974",
		[
			test_larson1974_turnoffmass_monotonicity(),
			test_larson1974_lifetime_monotonicity(),
			test_larson1974_lifetime_minimum()
		]
	]


@unittest
def test_larson1974_turnoffmass_monotonicity():
	r"""
	Test the Larson (1974) [1]_ mass-lifetime relation for monotonicity in the
	turnoff mass as a function of stellar age.

	.. [1] Larson (1974), MNRAS, 166, 585
	"""
	def test():
		result = True
		for postMS in _POSTMS_TEST_VALUES_:
			result &= turnoffmass_monotonicity(mlr.larson1974, postMS = postMS)
			if not result: break
		return result
	return ["vice.mlr.larson1974 [turnoff mass monotonicity]", test]


@unittest
def test_larson1974_lifetime_monotonicity():
	r"""
	Test the Larson (1974) [1]_ mass-lifetime relation for monotonicity in the
	lifetimes of stars as a function of stellar mass.

	.. [1] Larson (1974), MNRAS, 166, 585
	"""
	def test():
		result = True
		global _TEST_MASSES_ # prevents UnboundLocalError
		# A parabola in log(t)-log(m) space, the Larson (1974) form has a known
		# minimum at ~87.74 Msun.
		_TEST_MASSES_ = [_ for _ in _TEST_MASSES_ if _ < 87.74]
		for postMS in _POSTMS_TEST_VALUES_:
			result &= lifetime_monotonicity(mlr.larson1974, postMS = postMS)
			if not result: break
		_TEST_MASSES_ = [0.01 * i for i in range(1, 10001)]
		return result
	return ["vice.mlr.larson1974 [lifetime monotonicity", test]


@unittest
def test_larson1974_lifetime_minimum():
	r"""
	Test the Larson (1974) [1]_ mass-lifetime relation against the minimum
	lifetime of 3 Myr.

	.. [1] Larson (1974), MNRAS, 166, 585
	"""
	def test():
		result = True
		for postMS in _POSTMS_TEST_VALUES_:
			result &= lifetime_minimum(mlr.larson1974, postMS = postMS)
			if not result: break
		return result
	return ["vice.mlr.larson1974 [lifetime minimum]", test]


def turnoffmass_monotonicity(func, **kwargs):
	r"""
	Test a turnoff mass function by asserting that it should predict masses
	which decrease monotonically with increasing age.

	Parameters
	----------
	func : <function>
		The function to apply the minimum lifetime test to
	kwargs : real numbers
		Additional keyword arguments to pass onto ``func``.

	Returns
	-------
	True on success, False on failure
	"""
	result = True
	masses = len(_TEST_TIMES_) * [0.]
	for i in range(len(_TEST_TIMES_)):
		try:
			masses[i] = func(_TEST_TIMES_[i], which = "age", **kwargs)
		except:
			return False
		# turnoff mass at any timestep should be slightly smaller than previous
		if i: result &= masses[i] <= masses[i - 1]
		if not result: break
	return result


def lifetime_monotonicity(func, **kwargs):
	r"""
	Test a lifetime function by asserting that it should predict lifetimes
	which decrease monotonically with increasing stellar mass.

	Parameters
	----------
	func : <function>
		The function to apply the minimum lifetime test to
	kwargs : real numbers
		Additional keyword arguments to pass onto ``func``.

	Returns
	-------
	True on success, False on failure
	"""
	result = True
	lifetimes = len(_TEST_MASSES_) * [0.]
	for i in range(len(_TEST_MASSES_)):
		try:
			lifetimes[i] = func(_TEST_MASSES_[i], which = "mass", **kwargs)
		except:
			return False
		# lifetime at a given mass should be slightly smaller than previous mass
		# Padovani & Matteucci (1993) mlr flattens off at low masses, so use
		# the <= sign as opposed to < sign.
		if i: result &= lifetimes[i] <= lifetimes[i - 1]
		if not result: break
	return result


def lifetime_minimum(func, minimum = 0.003, **kwargs):
	r"""
	Test a lifetime function by asserting that it should predict lifetimes
	larger than that of the most massive stars. At very high masses
	(:math:`\gtrsim 100 M_\odot`), the mass-luminosity relation becomes linear,
	and as a consequence they all have similar lifetimes (:math:`\sim` 3 Myr at
	solar metallicity).

	Parameters
	----------
	func : <function>
		The function to apply the minimum lifetime test to
	minimum : real number [default : 0.003]
		The minimum lifetime to adopt, in Gyr.
	kwargs : real numbers
		Additional keyword arguments to pass onto ``func``.

	Returns
	-------
	True on success, False on failure
	"""
	result = True
	for mass in _TEST_MASSES_:
		try:
			result &= func(mass, which = "mass", **kwargs) > minimum
		except:
			return False
		if not result: break
	return result

