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


	@unittest 
	def test_name_setter(self): 
		def test(): 
			""" 
			Tests the name.setter function 

			Returns 
			======= 
			1 on success, 0 on failure 
			""" 
			try: 
				self.name = "test" 
			except: 
				return False 
			return self.name == "test" 
		return ["Name setter", test] 


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
		return ["Func setter", test] 


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
			except: 
				return False 
			return self.mode == "gas" 
		return ["Mode setter", test] 


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
		return ["Verbosity setter", test] 


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
			return len(self.elements) == 3 and self.elements == ("c", "n", "o") 
		return ["Elements setter", test] 


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
		return ["IMF setter", test] 


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
		return ["Eta setter", test]  


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
		return ["Enhancement setter", test] 


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
		return ["Entrainment settings", test] 


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
		return ["Inflow metallicity setter", test] 


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
				x = self.recycling == 0.4 
				self.recycling = "continuous" 
				y = self.recycling == "continuous" 
			except: 
				return False 
			return x and y 
		return ["Recycling setter", test] 


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
			except: 
				return False 
			return len(self.bins) == 401 and self.bins == sorted(self.bins) 
		return ["Bins setter", test] 


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
			except: 
				return False 
			return self.delay == 0.1 
		return ["SN Ia minimum delay setter", test] 


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
		return ["SN Ia rate setter", test] 


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
				self.Mg0 = 0 
			except: 
				return False 
			return self.Mg0 == 1e-12 
		return ["Mg0 setter", test] 


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
			except: 
				return False 
			return self.smoothing == 1 
		return ["Smoothing time setter", test] 


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
			except: 
				return False 
			return self.tau_ia == 1 
		return ["SN Ia e-folding timescale setter", test] 


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
				custom = lambda t: 2 + 0.01 * t 
				self.tau_star = custom 
				x = self.tau_star == custom 
				self.tau_star = 2
				y = self.tau_star == 2 
			except: 
				return False 
			return x and y 
		return ["SFE timescale setter", test] 


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
			except: 
				return False 
			return self.dt == 0.05 
		return ["Timestep setter", test] 


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
				return self.schmidt 
			except: 
				return False 
		return ["Schimdt Law switch", test] 


	@unittest 
	def test_mgschmidt_setter(self): 
		def test(): 
			""" 
			Tests the mgschnidt.setter function 

			Returns 
			======= 
			1 on success, 0 on failure 
			""" 
			try: 
				self.MgSchmidt = 5.e9 
			except: 
				return False 
			return self.MgSchmidt == 5.e9 
		return ["Schmidt Law normalization setter", test] 


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
			except: 
				return False 
			return self.m_upper == 101 
		return ["Upper stellar mass limit setter", test] 


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
			except: 
				return False 
			return self.m_lower == 0.1 
		return ["Lower stellar mass limit setter", test] 


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
			except: 
				return False 
			return self.postMS == 0.15 
		return ["Post main-sequence setter", test] 


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
			except: 
				return False 
			return self.Z_solar == 0.013 
		return ["Solar metallicity setter", test] 


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
		return ["Simulation prep", test]  


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
		return ["Output times refinement", test] 


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
				try: 
					self.open_output_dir(True) 
				except RuntimeError: 
					return False 
			except: 
				return False 
			if os.path.exists("test.vice"): 
				os.system("rm -rf test.vice/") 
				return True 
			else: 
				return False 
		return ["Open output directory", test] 


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
					if <void *> e[i][0].agb_grid[0].grid is NULL: 
						x = False 
						break 
					else: pass 
					if <void *> e[i][0].agb_grid[0].m is NULL: 
						x = False 
						break 
					else: pass 
					if <void *> e[i][0].agb_grid[0].z is NULL: 
						x = False 
						break 
					else: pass 
			except: 
				return False 
			return x 
		return ["Setup elements", test] 


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
					else: 
						pass 
				self.RIa = "plaw" 
			except: 
				return False 
			return x 
		return ["Setup RIa", test] 


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
		return ["Setup Zin", test] 


	@unittest 
	def test_save_yields(self): 
		def test(): 
			""" 
			Tests the save_yields function 

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
				self.save_yields()   
			except: 
				return False 
			x = (
				os.path.exists("%s.vice/yields/agb" % (self.name)) and 
				os.path.exists("%s.vice/yields/ccsne" % (self.name)) and 
				os.path.exists("%s.vice/yields/sneia" % (self.name))
			) 
			os.system("rm -rf %s.vice" % (self.name)) 
			return x 
		return ["Save yields", test] 


	@unittest 
	def test_save_attributes(self): 
		def test(): 
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
				self.save_attributes() 
			except: 
				return False 
			x = (os.path.exists("%s.vice/attributes" % (self.name)) and 
				len(os.listdir("%s.vice/attributes" % (self.name))) == 28) 
			os.system("rm -rf %s.vice" % (self.name)) 
			return x 
		return ["Save attributes", test] 

