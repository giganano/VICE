# cython: language_level = 3, boundscheck = False, binding = True

from __future__ import absolute_import
from ....._globals import _VERSION_ERROR_
from .....testing import moduletest
from .....testing import unittest
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from libc.stdlib cimport malloc, free
from . cimport _zero_age_ssp

_TIMES_ = [0.01 * i for i in range(1001)]


@moduletest
def single_zero_age_ssp():
	r"""
	Runs a zero age SSP edge-case test in which the attribute tau_star is set
	to infinity for all timesteps except the final one.
	"""
	return [
		"""vice.core.singlezone edge case : single zero age stellar population \
[tau_star = 2 if t = %g Gyr else infinity]""" % (_TIMES_[-1]),
		zero_age_ssp_test(tau_star = tau_star)
	]


def tau_star(t):
	r"""
	The attribute tau_star as a function of time for the fiducial zero age SSP
	edge-case test.
	"""
	if t > _TIMES_[-1]:
		return 2
	else:
		return float("inf")


def zero_age_ssp_test(**kwargs):
	r"""
	Run a zero-age ssp edge-case test. These are defined as parameter spaces
	which produce a non-zero star formation rate only at the final timestep,
	and zero until then.

	Parameters
	----------
	kwargs : varying types
		The keyword arguments to set as attributes of the singlezone class.
		Assumed to produce quiescence at times up to the final timestep.

	Returns
	-------
	tests : list
		The unit tests to return as a part of the moduletest object.
		None if the zero_age_ssp class cannot be instantiated.
	"""
	try:
		_TEST_ = zero_age_ssp(**kwargs)
	except:
		return None
	return [
		_TEST_.test_m_AGB(),
		_TEST_.test_m_ccsne(),
		_TEST_.test_update_element_mass(),
		_TEST_.test_onH(),
		_TEST_.test_update_gas_evolution(),
		_TEST_.test_get_outflow_rate(),
		_TEST_.test_singlezone_unretained(),
		_TEST_.test_MDF(),
		_TEST_.test_mass_recycled(),
		_TEST_.test_singlezone_stellar_mass(),
		_TEST_.test_m_sneia()
	]


cdef class zero_age_ssp:

	r"""
	A class intended to run unit tests for a zero age SSP edge case. These are
	cases which should always produce star formation at only the final
	timestep and thus elemental production only at the end of the simulation.
	"""

	# def __init__(self, **kwargs):
	# 	if "name" in kwargs.keys(): del kwargs["name"]
	# 	super().__init__(name = "test", **kwargs)
	# 	self.prep(_TIMES_)
	# 	self.open_output_dir(True)
	# 	self._sz[0].n_outputs = len(_TIMES_)
	# 	self._sz[0].output_times = <double *> malloc (self._sz[0].n_outputs *
	# 		sizeof(double))
	# 	for i in range(self._sz[0].n_outputs):
	# 		self._sz[0].output_times[i] = _TIMES_[i]
	# 	_zero_age_ssp.singlezone_setup(self._sz)
	# 	_zero_age_ssp.singlezone_evolve_no_setup_no_clean(self._sz)
	# 	_zero_age_ssp.normalize_MDF(self._sz)
	# 	_zero_age_ssp.write_mdf_output(self._sz[0])

	@unittest
	def test_m_AGB(self):
		r"""
		vice.src.singlezone.agb.m_AGB zero age SSP edge-case test
		"""
		def test():
			return _zero_age_ssp.zero_age_ssp_test_m_AGB(self._sz)
		return ["vice.src.singlezone.agb.m_agb", test]

	@unittest
	def test_m_ccsne(self):
		r"""
		vice.src.singlezone.ccsne.mdot_ccsne zero age SSP edge-case test
		"""
		def test():
			return _zero_age_ssp.zero_age_ssp_test_m_ccsne(self._sz)
		return ["vice.src.singlezone.ccsne.m_ccsne", test]

	@unittest
	def test_update_element_mass(self):
		r"""
		vice.src.singlezone.element.update_element_mass zero age SSP test
		"""
		def test():
			return _zero_age_ssp.zero_age_ssp_test_update_element_mass(self._sz)
		return ["vice.src.singlezone.element.update_element_mass", test]

	@unittest
	def test_onH(self):
		r"""
		vice.src.singlezone.element.onH zero age SSP test
		"""
		def test():
			return _zero_age_ssp.zero_age_ssp_test_onH(self._sz)
		return ["vice.src.singlezone.element.onH", test]

	@unittest
	def test_update_gas_evolution(self):
		r"""
		vice.src.singlezone.ism.update_gas_evolution zero age SSP test
		"""
		def test():
			return _zero_age_ssp.zero_age_ssp_test_update_gas_evolution(
				self._sz)
		return ["vice.src.singlezone.ism.update_gas_evolution", test]

	@unittest
	def test_get_outflow_rate(self):
		r"""
		vice.src.singlezone.ism.get_outflow rate zero age SSP test
		"""
		def test():
			return _zero_age_ssp.zero_age_ssp_test_get_outflow_rate(self._sz)
		return ["vice.src.singlezone.ism.get_outflow_rate", test]

	@unittest
	def test_singlezone_unretained(self):
		r"""
		vice.src.singlezone.ism.singlezone_unretained zero age SSP test
		"""
		def test():
			return _zero_age_ssp.zero_age_ssp_test_singlezone_unretained(
				self._sz)
		return ["vice.src.singlezone.ism.singlezone_unretained", test]

	@unittest
	def test_MDF(self):
		r"""
		vice.src.singlezone.mdf zero age SSP test
		"""
		def test():
			return _zero_age_ssp.zero_age_ssp_test_MDF(self._sz)
		return ["vice.src.singlezone.mdf", test]

	@unittest
	def test_mass_recycled(self):
		r"""
		vice.src.singlezone.recycling.mass_recycled zero age SSP test
		"""
		def test():
			return _zero_age_ssp.zero_age_ssp_test_mass_recycled(self._sz)
		return ["vice.src.singlezone.recycling.mass_recycled", test]

	@unittest
	def test_singlezone_stellar_mass(self):
		r"""
		vice.src.singlezone.singlezone.singlezone_stellar_mass zero age SSP test
		"""
		def test():
			return _zero_age_ssp.zero_age_ssp_test_singlezone_stellar_mass(
				self._sz)
		return ["vice.src.singlezone.singlezone.singlezone_stellar_mass",
			test]

	@unittest
	def test_m_sneia(self):
		r"""
		vice.src.singlezone.sneia.mdot_sneia zero age SSP test
		"""
		def test():
			return _zero_age_ssp.zero_age_ssp_test_mdot_sneia(self._sz)
		return ["vice.src.singlezone.sneia.m_sneia", test]


