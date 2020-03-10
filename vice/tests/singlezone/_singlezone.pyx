# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import  
__all__ = [
	"singlezone_tester" 
]
from ..._globals import _DEFAULT_FUNC_ 
from ...core.dataframe import base as dataframe 
from ...yields import agb 
from ...yields import ccsne 
from ...yields import sneia 
from .._test_utils import unittest 
import os 
from . cimport _singlezone 


cdef class singlezone_tester: 

	""" 
	This class inherits from the singlezone object at 
	vice/core/singlezone/_singlezone.pyx, and each function here simply 
	tests one of the functions under the hood denoted by the names of each 
	function. 
	""" 

	def __init__(self): 
		super().__init__(**{}) 


	def test_name_setter(self): 
		return unittest("Name setter", self.name_setter) 


	def name_setter(self): 
		""" 
		Tests the name.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.name = "test" 
			return self.name == "test" 
		except: 
			return False 


	def test_func_setter(self): 
		return unittest("Func setter", self.func_setter) 


	def func_setter(self): 
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
			return result 
		except: 
			return False 


	def test_mode_setter(self): 
		return unittest("Mode setter", self.mode_setter) 


	def mode_setter(self): 
		""" 
		Tests the mode.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.mode = "gas" 
			return self.mode == "gas" 
		except: 
			return False 


	def test_verbose_setter(self): 
		return unittest("Verbosity setter", self.verbose_setter) 


	def verbose_setter(self): 
		""" 
		Tests the verbose.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.verbose = True 
			return self.verbose 
		except: 
			return False 


	def test_elements_setter(self): 
		return unittest("Elements setter", self.elements_setter) 


	def elements_setter(self): 
		""" 
		Tests the elements.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.elements = ["c", "n", "o"] 
			return len(self.elements) == 3 and self.elements == ("c", "n", "o") 
		except: 
			return False 


	def test_imf_setter(self): 
		return unittest("IMF setter", self.imf_setter) 


	def imf_setter(self): 
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
			return x and y 
		except: 
			return False 


	def test_eta_setter(self): 
		return unittest("Eta setter", self.eta_setter) 


	def eta_setter(self): 
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
			return x and y 
		except: 
			return False 


	def test_enhancement_setter(self): 
		return unittest("Enhancement setter", self.enhancement_setter) 


	def enhancement_setter(self): 
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
			return x and y 
		except: 
			return False 


	def test_entrainment(self): 
		return unittest("Entrainment settings", self.entrainment_settings) 


	def entrainment_settings(self): 
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


	def test_zin_setter(self): 
		return unittest("Inflow metallicity setter", self.zin_setter) 


	def zin_setter(self): 
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
			return x and y and z 
		except: 
			return False 


	def test_recycling_setter(self): 
		return unittest("Recycling setter", self.recycling_setter) 


	def recycling_setter(self): 
		""" 
		Tests the recycling.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.recycling = 0.4 
			x = self.recycling == 0.4 
			self.recycling = "continuous" 
			y = self.recycling == "continuous" 
			return x and y 
		except: 
			return False 


	def test_bins_setter(self): 
		return unittest("Bins setter", self.bins_setter) 


	def bins_setter(self): 
		""" 
		Tests the bins.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.bins = [-3 + 0.01 * i for i in range(401)] 
			return len(self.bins) == 401 
		except: 
			return False 


	def test_delay_setter(self): 
		return unittest("SN Ia minimum delay setter", self.delay_setter) 


	def delay_setter(self): 
		""" 
		Tests the delay.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.delay = 0.1 
			return self.delay == 0.1 
		except: 
			return False 


	def test_ria_setter(self): 
		return unittest("SN Ia rate setter", self.ria_setter) 


	def ria_setter(self): 
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
			return x and y and z 
		except: 
			return False 


	def test_mg0_setter(self): 
		return unittest("Mg0 setter", self.mg0_setter) 


	def mg0_setter(self): 
		""" 
		Tests the Mg0.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.Mg0 = 0 
			return self.Mg0 == 1e-12 
		except: 
			return False 


	def test_smoothing_setter(self): 
		return unittest("Smoothing time setter", self.smoothing_setter) 


	def smoothing_setter(self): 
		""" 
		Tests the smoothing.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.smoothing = 1 
			return self.smoothing == 1 
		except: 
			return False 


	def test_tau_ia_setter(self): 
		return unittest("SN Ia e-folding timescale setter", self.tau_ia_setter) 


	def tau_ia_setter(self): 
		""" 
		Tests the tau_ia.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.tau_ia = 1.0 
			return self.tau_ia == 1 
		except: 
			return False 


	def test_tau_star_setter(self): 
		return unittest("SFE timescale setter", self.tau_star_setter) 


	def tau_star_setter(self): 
		""" 
		Tests the tau_star.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			custom = lambda t: 2 + 0.01 * t 
			self.tau_star = custom 
			x = self.tau_star == custom 
			self.tau_star = 2
			y = self.tau_star == 2 
			return x and y 
		except: 
			return False 


	def test_dt_setter(self): 
		return unittest("Timestep setter", self.dt_setter) 


	def dt_setter(self): 
		""" 
		Tests the dt.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.dt = 0.05 
			return self.dt == 0.05 
		except: 
			return False 


	def test_schmidt_setter(self): 
		return unittest("Schimdt Law switch", self.schmidt_setter) 


	def schmidt_setter(self): 
		""" 
		Tests the schmidt.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.schmidt = True 
			return self.schmidt 
		except: 
			return False 


	def test_mgschmidt_setter(self): 
		return unittest("Schmidt Law normalization setter", 
			self.mgschmidt_setter) 


	def mgschmidt_setter(self): 
		""" 
		Tests the mgschnidt.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.MgSchmidt = 5.e9 
			return self.MgSchmidt == 5.e9 
		except: 
			return False 


	def test_m_upper_setter(self): 
		return unittest("Upper stellar mass limit setter", self.m_upper_setter) 


	def m_upper_setter(self): 
		""" 
		Tests the m_upper.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.m_upper = 101 
			return self.m_upper == 101 
		except: 
			return False 


	def test_m_lower_setter(self): 
		return unittest("Lower stellar mass limit setter", self.m_lower_setter) 


	def m_lower_setter(self): 
		""" 
		Tests the m_lower.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.m_lower = 0.1 
			return self.m_lower == 0.1 
		except: 
			return False 


	def test_postMS_setter(self): 
		return unittest("Post main-sequence setter", self.postMS_setter) 


	def postMS_setter(self): 
		""" 
		Tests the postMS.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.postMS = 0.15 
			return self.postMS == 0.15 
		except: 
			return False 


	def test_z_solar_setter(self): 
		return unittest("Solar metallicity setter", self.z_solar_setter) 


	def z_solar_setter(self): 
		""" 
		Tests the Z_solar.setter function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.Z_solar = 0.013 
			return self.Z_solar == 0.013 
		except: 
			return False 


	def test_prep(self): 
		return unittest("Simulation prep", self._prep) 


	def _prep(self): 
		""" 
		Tests the prep function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			test_times = [0.1 * i for i in range(11)] 
			super().prep(test_times) 
			return (
				self._sz[0].ism[0].mass == self.Mg0 and 
				self._sz[0].ism[0].eta is not NULL and 
				self._sz[0].ism[0].enh is not NULL and 
				self._sz[0].ism[0].tau_star is not NULL and 
				self._sz[0].ism[0].specified is not NULL 
			) 
		except: 
			return False 


	def test_output_times_check(self): 
		return unittest("Output times refinement", self._output_times_check) 


	def _output_times_check(self): 
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
			return super().output_times_check(test_times) == sorted(test_times) 
		except: 
			return False 


	def test_open_output_dir(self): 
		return unittest("Open output directory", self._open_output_dir) 


	def _open_output_dir(self): 
		""" 
		Tests the output directory opener 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.name = "test" 
			try: 
				super().open_output_dir(True) 
			except RuntimeError: 
				return False 
			if os.path.exists("test.vice"): 
				os.system("rm -rf test.vice/") 
				return True 
			else: 
				return False 
		except: 
			return False 


	def test_setup_elements(self): 
		return unittest("Setup elements", self._setup_elements) 


	def _setup_elements(self): 
		""" 
		Tests the setup_elements function 
		""" 
		try: 
			super().setup_elements() 
			x = True 
			for i in range(self._sz[0].n_elements): 
				if self._sz[0].elements[i][0].ccsne_yields[0].yield_ is NULL:  
					x = False 
				else: pass 
				if self._sz[0].elements[i][0].sneia_yields[0].yield_ is NULL: 
					x = False 
				else: pass 
				if self._sz[0].elements[i][0].agb_grid[0].grid is NULL: 
					x = False 
				else: pass 
				if self._sz[0].elements[i][0].agb_grid[0].m is NULL: 
					x = False 
				else: pass 
				if self._sz[0].elements[i][0].agb_grid[0].z is NULL: 
					x = False 
				else: pass 
				return x 
		except: 
			return False 


	def test_set_ria(self): 
		return unittest("Setup RIa", self._set_ria) 


	def _set_ria(self): 
		""" 
		Tests the set_ria function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			# This function only works with custom RIa's 
			self.RIa = lambda t: t**-1.5 
			super().set_ria() 
			x = True 
			for i in range(self._sz[0].n_elements): 
				if self._sz[0].elements[i][0].sneia_yields[0].RIa is NULL: 
					x = False 
				else: 
					pass 
			self.RIa = "plaw" 
			return x 
		except: 
			return False 


	def test_setup_Zin(self): 
		return unittest("Setup Zin", self._setup_Zin) 


	def _setup_Zin(self): 
		""" 
		Tests the setup_Zin function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		def checker(): 
			x = True 
			for i in range(self._sz[0].n_elements): 
				if self._sz[0].elements[i][0].Zin is NULL: x = False 
			return x 
		try: 
			self.Zin = dict(zip(
				self.elements, 
				self._sz[0].n_elements * [0.001]
			)) 
			self.Zin[self.elements[0]] = lambda t: 0.001 * t 
			super().setup_Zin(1) 
			x = checker() 
			self.Zin = lambda t: 0.001 * t 
			super().setup_Zin(1) 
			y = checker() 
			self.Zin = 0 
			super().setup_Zin(1) 
			z = checker() 
			return x and y and z 
		except: 
			return False 


	def test_save_yields(self): 
		return unittest("Save yields", self._save_yields) 


	def _save_yields(self): 
		""" 
		Tests the save_yields function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.name = "test" 
			os.system("mkdir %s.vice" % (self.name)) 
			super().save_yields() 
			x = (os.path.exists("%s.vice/agb_yields.config" % (self.name)) and 
				os.path.exists("%s.vice/ccsne_yields.config" % (self.name)) and 
				os.path.exists("%s.vice/sneia_yields.config" % (self.name)))  
			os.system("rm -rf %s.vice" % (self.name)) 
			return x 
		except: 
			return False 


	def test_save_attributes(self): 
		return unittest("Save attributes", self._save_attributes) 


	def _save_attributes(self): 
		""" 
		Tests the save_attributes function 

		Returns 
		======= 
		1 on success, 0 on failure 
		""" 
		try: 
			self.name = "test" 
			if os.path.exists("%s.vice" % (self.name)): 
				os.system("rm -rf %s.vice" % (self.name)) 
			else: pass 
			os.system("mkdir %s.vice" % (self.name)) 
			super().save_attributes() 
			x = os.path.exists("%s.vice/params.config" % (self.name)) 
			os.system("rm -rf %s.vice" % (self.name)) 
			return x 
		except: 
			return False 

