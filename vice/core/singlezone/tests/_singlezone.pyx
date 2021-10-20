# cython: language_level = 3, boundscheck = False, binding = True

from __future__ import absolute_import
__all__ = ["test"]
from ...._globals import _DEFAULT_FUNC_
from ....testing import moduletest
from ....testing import unittest
from ...dataframe import base as dataframe
from ....yields import agb
from ....yields import ccsne
from ....yields import sneia
import os

from libc.string cimport strcmp
from . cimport _singlezone


@moduletest
def test():
	r"""
	vice.core.singlezone module test
	"""
	try:
		_TEST_ = singlezone_tester()
	except:
		return ["vice.core.singlezone", None]
	return ["vice.core.singlezone",
		[
			_TEST_.test_name_setter(),
			_TEST_.test_func_setter(),
			_TEST_.test_mode_setter(),
			_TEST_.test_verbose_setter(),
			_TEST_.test_elements_setter(),
			_TEST_.test_imf_setter(),
			_TEST_.test_eta_setter(),
			_TEST_.test_enhancement_setter(),
			_TEST_.test_entrainment(),
			_TEST_.test_zin_setter(),
			_TEST_.test_recycling_setter(),
			_TEST_.test_bins_setter(),
			_TEST_.test_delay_setter(),
			_TEST_.test_ria_setter(),
			_TEST_.test_mg0_setter(),
			_TEST_.test_smoothing_setter(),
			_TEST_.test_tau_ia_setter(),
			_TEST_.test_tau_star_setter(),
			_TEST_.test_dt_setter(),
			_TEST_.test_schmidt_setter(),
			_TEST_.test_mgschmidt_setter(),
			_TEST_.test_m_upper_setter(),
			_TEST_.test_m_lower_setter(),
			_TEST_.test_postMS_setter(),
			_TEST_.test_z_solar_setter(),
			_TEST_.test_prep(),
			_TEST_.test_output_times_check(),
			_TEST_.test_open_output_dir(),
			_TEST_.test_setup_elements(),
			_TEST_.test_set_ria(),
			_TEST_.test_setup_Zin(),
			_TEST_.test_pickle()
		]
	]


def _timedep_tau_star(t):
	r"""
	A dummy function to act as a time-dependent SFE timescale.
	"""
	return 2.0 * t / 10.0


def _time_and_gasdep_tau_star(t, m):
	r"""
	A dummy function to act as a time- and gas-dependent SFE timescale.
	"""
	return 2.0 * t / 10.0 * (m / 6.0e9)**0.5


cdef class singlezone_tester:

	r"""
	The c_singlezone class is subclassed here to give these routines access to
	the SINGLEZONE *_sz attribute.
	"""

	def __init__(self):
		super().__init__(**{})


	@unittest
	def test_name_setter(self):
		r"""
		vice.core.singlezone.name.setter unit test
		"""
		def test():
			try:
				self.name = "test"
			except:
				return False
			return not strcmp(self._sz[0].name, "test.vice")
		return ["vice.core.singlezone.name.setter", test]


	@unittest
	def test_func_setter(self):
		def test():
			"""
			Tests the func.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				x = lambda t: 9.1
				self.func = x
				result = self.func == x
				self.func = _DEFAULT_FUNC_
			except:
				return False
			return result
		return ["vice.core.singlezone.func.setter", test]


	@unittest
	def test_mode_setter(self):
		def test():
			"""
			Tests the mode.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.mode = "gas"
				assert not strcmp(self._sz[0].ism[0].mode, "gas")
			except:
				return False
			try:
				self.mode = "ifr"
				assert not strcmp(self._sz[0].ism[0].mode, "ifr")
			except:
				return False
			try:
				self.mode = "sfr"
				assert not strcmp(self._sz[0].ism[0].mode, "sfr")
			except:
				return False
			return True
		return ["vice.core.singlezone.mode.setter", test]


	@unittest
	def test_verbose_setter(self):
		def test():
			"""
			Tests the verbose.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.verbose = True
			except:
				return False
			return self.verbose
		return ["vice.core.singlezone.verbosity.setter", test]


	@unittest
	def test_elements_setter(self):
		def test():
			"""
			Tests the elements.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.elements = ["c", "n", "o"]
			except:
				return False
			status = (self._sz[0].n_elements == 3 and
				self.elements == ('c', 'n', 'o'))
			if status:
				for i in range(3):
					if status:
						status = not strcmp(self._sz[0].elements[i][0].symbol,
							self.elements[i].encode())
					else:
						break
			else: pass
			return status
			# return len(self.elements) == 3 and self.elements == ("c", "n", "o")
		return ["vice.core.singlezone.elements.setter", test]


	@unittest
	def test_imf_setter(self):
		def test():
			"""
			Tests the IMF.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				custom = lambda m: m**-2
				self.IMF = custom
				x = self.IMF == custom
				self.IMF = "kroupa"
				y = self.IMF == "kroupa"
			except:
				return False
			return x and y
		return ["vice.core.singlezone.IMF.setter", test]


	@unittest
	def test_eta_setter(self):
		def test():
			"""
			Tests the eta.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				custom = lambda t: 0.5 * t
				self.eta = custom
				x = self.eta == custom
				self.eta = 1
				y = self.eta == 1
			except:
				return False
			return x and y
		return ["vice.core.singlezone.eta.setter", test]


	@unittest
	def test_enhancement_setter(self):
		def test():
			"""
			Tests the enhancement.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				custom = lambda t: 0.5 * t
				self.enhancement = custom
				x = self.enhancement == custom
				self.enhancement = 1
				y = self.enhancement == 1
			except:
				return False
			return x and y
		return ["vice.core.singlezone.enhancement.setter", test]


	@unittest
	def test_entrainment(self):
		def test():
			"""
			Tests the entrainment settings

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				return (isinstance(self.entrainment.ccsne, dataframe) and
					isinstance(self.entrainment.sneia, dataframe) and
					isinstance(self.entrainment.agb, dataframe))
			except:
				return False
		return ["vice.core.singlezone.entrainment", test]


	@unittest
	def test_zin_setter(self):
		def test():
			"""
			Tests the Zin.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				custom = lambda t: 0.01 * t
				self.Zin = custom
				x = self.Zin == custom
				self.Zin = dict(zip(self.elements, len(self.elements) * [0.001]))
				y = isinstance(self.Zin, dataframe)
				self.Zin = 0
				z = not self.Zin
			except:
				return False
			return x and y and z
		return ["vice.core.singlezone.Zin.setter", test]


	@unittest
	def test_recycling_setter(self):
		def test():
			"""
			Tests the recycling.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.recycling = 0.4
				assert self._sz[0].ssp[0].R0 == 0.4
				assert self._sz[0].ssp[0].continuous == 0
			except:
				return False
			try:
				self.recycling = "continuous"
				assert self._sz[0].ssp[0].R0 == 0.0
				assert self._sz[0].ssp[0].continuous == 1
			except:
				return False
			return True
		return ["vice.core.singlezone.recycling.setter", test]


	@unittest
	def test_bins_setter(self):
		def test():
			"""
			Tests the bins.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.bins = [-3 + 0.01 * i for i in range(401)]
				assert self._sz[0].mdf[0].n_bins == 400
				for i in range(self._sz[0].mdf[0].n_bins + 1):
					assert self._sz[0].mdf[0].bins[i] == -3 + 0.01 * i
			except:
				return False
			return True
		return ["vice.core.singlezone.bins.setter", test]


	@unittest
	def test_delay_setter(self):
		def test():
			"""
			Tests the delay.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.delay = 0.1
				for i in range(self._sz[0].n_elements):
					assert self._sz[0].elements[i][0].sneia_yields[0].t_d == 0.1
			except:
				return False
			return True
		return ["vice.core.singlezone.delay.setter", test]


	@unittest
	def test_ria_setter(self):
		def test():
			"""
			Tests the RIa.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				custom = lambda t: t**-1.5
				self.RIa = custom
				x = self.RIa == custom
				self.RIa = "exp"
				y = self.RIa == "exp"
				self.RIa = "plaw"
				z = self.RIa == "plaw"
			except:
				return False
			return x and y and z
		return ["vice.core.singlezone.RIa.setter", test]


	@unittest
	def test_mg0_setter(self):
		def test():
			"""
			Tests the Mg0.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.Mg0 = 10
				assert self._Mg0 == 10
				self.Mg0 = 0
				assert self._Mg0 == 1e-12
			except:
				return False
			return True
		return ["vice.core.singlezone.Mg0.setter", test]


	@unittest
	def test_smoothing_setter(self):
		def test():
			"""
			Tests the smoothing.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.smoothing = 1
				assert self._sz[0].ism[0].smoothing_time == 1
			except:
				return False
			return True
		return ["vice.core.singlezone.smoothing.setter", test]


	@unittest
	def test_tau_ia_setter(self):
		def test():
			"""
			Tests the tau_ia.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.tau_ia = 1.0
				for i in range(self._sz[0].n_elements):
					assert (
						self._sz[0].elements[i][0].sneia_yields[0].tau_ia == 1.0
					)
			except:
				return False
			return True
		return ["vice.core.singlezone.tau_ia.setter", test]


	@unittest
	def test_tau_star_setter(self):
		def test():
			"""
			Tests the tau_star.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.tau_star = _timedep_tau_star
				x = self.tau_star == _timedep_tau_star
				self.tau_star = _time_and_gasdep_tau_star
				y = self.tau_star == _time_and_gasdep_tau_star
				self.tau_star = 2
				z = self.tau_star == 2
			except:
				return False
			return x and y and z
		return ["vice.core.singlezone.tau_star.setter", test]


	@unittest
	def test_dt_setter(self):
		def test():
			"""
			Tests the dt.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.dt = 0.05
				assert self._sz[0].dt == 0.05
			except:
				return False
			return True
		return ["vice.core.singlezone.dt.setter", test]


	@unittest
	def test_schmidt_setter(self):
		def test():
			"""
			Tests the schmidt.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.schmidt = True
				assert self._sz[0].ism[0].schmidt == 1
				self.schmidt = False
				assert self._sz[0].ism[0].schmidt == 0
			except:
				return False
			return True
		return ["vice.core.singlezone.schmidt.setter", test]


	@unittest
	def test_mgschmidt_setter(self):
		def test():
			"""
			Tests the mgschmidt.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.MgSchmidt = 5.e9
				assert self._sz[0].ism[0].mgschmidt == 5.e9
			except:
				return False
			return True
		return ["vice.core.singlezone.MgSchmidt.setter", test]


	@unittest
	def test_m_upper_setter(self):
		def test():
			"""
			Tests the m_upper.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.m_upper = 101
				assert self._sz[0].ssp[0].imf[0].m_upper == 101
			except:
				return False
			return True
		return ["vice.core.singlezone.m_upper.setter", test]


	@unittest
	def test_m_lower_setter(self):
		def test():
			"""
			Tests the m_lower.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.m_lower = 0.1
				assert self._sz[0].ssp[0].imf[0].m_lower == 0.1
			except:
				return False
			return True
		return ["vice.core.singlezone.m_lower.setter", test]


	@unittest
	def test_postMS_setter(self):
		def test():
			"""
			Tests the postMS.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.postMS = 0.15
				assert self._sz[0].ssp[0].postMS == 0.15
			except:
				return False
			return True
		return ["vice.core.singlezone.postMS.setter", test]


	@unittest
	def test_z_solar_setter(self):
		def test():
			"""
			Tests the Z_solar.setter function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.Z_solar = 0.013
				assert self._sz[0].Z_solar == 0.013
			except:
				return False
			return True
		return ["vice.core.singlezone.Z_solar.setter", test]


	@unittest
	def test_prep(self):
		def test():
			"""
			Tests the prep function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				test_times = [0.1 * i for i in range(11)]
				self.prep(test_times)
			except:
				return False
			return (
				self._sz[0].ism[0].mass == self.Mg0 and
				<void *> self._sz[0].ism[0].eta is not NULL and
				<void *> self._sz[0].ism[0].enh is not NULL and
				<void *> self._sz[0].ism[0].tau_star is not NULL and
				<void *> self._sz[0].ism[0].specified is not NULL
			)
		return ["vice.core.singlezone.prep", test]


	@unittest
	def test_output_times_check(self):
		def test():
			"""
			Tests the output_times_check function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				"""
				flip two of the times on purpose, ensure they come back in the
				right order
				"""
				test_times = [
					0.0, 0.2, 0.1, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0
				]
				return self.output_times_check(test_times) == sorted(test_times)
			except:
				return False
		return ["vice.core.singlezone.output_times_check", test]


	@unittest
	def test_open_output_dir(self):
		def test():
			"""
			Tests the output directory opener

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				self.name = "test"
				self.open_output_dir(True)
			except:
				return False
			if os.path.exists("test.vice"):
				os.system("rm -rf test.vice/")
				return True
			else:
				return False
		return ["vice.core.singlezone.open_output_dir", test]


	@unittest
	def test_setup_elements(self):
		cdef ELEMENT **e
		def test():
			"""
			Tests the setup_elements function
			"""
			try:
				self.setup_elements()
				e = self._sz[0].elements
				x = True
				for i in range(self._sz[0].n_elements):
					if <void *> e[i][0].ccsne_yields[0].yield_ is NULL:
						x = False
						break
					else: pass
					if <void *> e[i][0].sneia_yields[0].yield_ is NULL:
						x = False
						break
					else: pass
					if (<void *> e[i][0].agb_grid[0].interpolator[0].xcoords is
						NULL):
						x = False
						break
					else: pass
					if (<void *> e[i][0].agb_grid[0].interpolator[0].ycoords is
						NULL):
						x = False
						break
					else: pass
					if (<void *> e[i][0].agb_grid[0].interpolator[0].zcoords is
						NULL):
						x = False
						break
					else: pass
			except:
				return False
			return x
		return ["vice.core.singlezone.setup_elements", test]


	@unittest
	def test_set_ria(self):
		cdef ELEMENT **e
		def test():
			"""
			Tests the set_ria function

			Returns
			=======
			1 on success, 0 on failure
			"""
			try:
				# This function only works with custom RIa's
				self.RIa = lambda t: t**-1.5
				self.set_ria()
				e = self._sz[0].elements
				x = True
				for i in range(self._sz[0].n_elements):
					if <void *> e[i][0].sneia_yields[0].RIa is NULL:
						x = False
						break
					else:
						pass
				self.RIa = "plaw"
			except:
				return False
			return x
		return ["vice.core.singlezone.setup_ria", test]


	@unittest
	def test_setup_Zin(self):
		def test():
			"""
			Tests the setup_Zin function

			Returns
			=======
			1 on success, 0 on failure
			"""
			def checker():
				x = True
				for i in range(self._sz[0].n_elements):
					if <void *> self._sz[0].elements[i][0].Zin is NULL:
						x = False
					else: pass
				return x
			try:
				self.Zin = dict(zip(
					self.elements,
					self._sz[0].n_elements * [0.001]
				))
				self.Zin[self.elements[0]] = lambda t: 0.001 * t
				self.setup_Zin(1)
				x = checker()
				self.Zin = lambda t: 0.001 * t
				self.setup_Zin(1)
				y = checker()
				self.Zin = 0
				self.setup_Zin(1)
				z = checker()
			except:
				return False
			return x and y and z
		return ["vice.core.singlezone.setup_zin", test]


	@unittest
	def test_pickle(self):
		def test():
			"""
			Tests the pickle function

			Returns
			=======
			1 on success, 0 on failure
			"""
			self.name = "test"
			if os.path.exists("%s.vice" % (self.name)):
				os.system("rm -rf %s.vice" % (self.name))
			else: pass
			os.system("mkdir %s.vice" % (self.name))
			try:
				self.pickle()
			except:
				return False
			x = (
				os.path.exists("%s.vice/yields/agb" % (self.name)) and
				os.path.exists("%s.vice/yields/ccsne" % (self.name)) and
				os.path.exists("%s.vice/yields/sneia" % (self.name)) and
				os.path.exists("%s.vice/attributes" % (self.name)) and
				len(os.listdir("%s.vice/yields/agb" % (self.name))) == len(
					self.elements) and
				len(os.listdir("%s.vice/yields/ccsne" % (self.name))) == len(
					self.elements) and
				len(os.listdir("%s.vice/yields/sneia" % (self.name))) == len(
					self.elements) and
				len(os.listdir("%s.vice/attributes" % (self.name))) == 28
			)
			os.system("rm -rf %s.vice" % (self.name))
			return x
		return ["vice.core.singlezone.pickle", test]

