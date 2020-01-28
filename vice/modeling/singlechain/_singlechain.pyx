# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ..._globals import _VERSION_ERROR_ 
from ..._globals import _DEFAULT_FUNC_ 
from ..._globals import _DEFAULT_BINS_ 
from ...core.singlezone import singlezone 
from ...core import _pyutils 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from ...core.singlezone._singlezone cimport c_singlezone 
from . cimport _singlechain 
from ._fitting_function cimport fitting_function 
from ._dataset cimport dataset 


cdef class c_singlechain: 

	def __init__(self, 
		name = "onezonechain", 
		func = _DEFAULT_FUNC_, 
		mode = "ifr", 
		verbose = False, 
		elements = ("fe", "sr", "o"), 
		IMF = "kroupa", 
		eta = 2.5, 
		enhancement = 1, 
		Zin = 0, 
		recycling = "continuous", 
		bins = _DEFAULT_BINS_, 
		delay = 0.15, 
		RIa = "plaw", 
		Mg0 = 6.0e9, 
		smoothing = 0, 
		tau_ia = 1.5, 
		tau_star = 2.0, 
		dt = 0.01, 
		schmidt = False, 
		MgSchmidt = 6.0e9, 
		schmidt_index = 0.5, 
		m_upper = 100, 
		m_lower = 0.08, 
		postMS = 0.1, 
		Z_solar = 0.014, 
		agb_model = None, 
		which = "stars"): 

		self._sz = c_singlezone() 
		self.name = name 
		self.func = func 
		self.mode = mode 
		self.verbose = verbose 
		self.elements = elements 
		self.IMF = IMF 
		self.eta = eta 
		self.enhancement = enhancement 
		self.Zin = Zin 
		self.recycling = recycling 
		self.bins = bins 
		self.delay = delay 
		self.RIa = RIa 
		self.Mg0 = Mg0 
		self.smoothing = smoothing 
		self.tau_ia = tau_ia 
		self.tau_star = tau_star 
		self.dt = dt 
		self.schmidt = schmidt 
		self.MgSchmidt = MgSchmidt 
		self.schmidt_index = schmidt_index 
		self.m_upper = m_upper 
		self.m_lower = m_lower 
		self.postMS = postMS 
		self.Z_solar = Z_solar 
		self.agb_model = agb_model 
		self._data = dataset(which = which) 

	@property 
	def name(self): 
		""" 
		Type :: str 

		The name of the singlechain fit. 
		""" 
		return self._sz.name 

	@name.setter 
	def name(self, value): 
		self._sz.name = value 

	@property 
	def func(self): 
		""" 
		Type :: <function> 
		Default :: _DEFAULT_FUNC_ 

		A callable python function of time which returns a real number. This 
		attribute may take any number of real numbers as parameters, the 
		first of which will be interpreted as time in Gyr. All subsequent 
		parameters will be treated as numerical values to be fit to the 
		observational data. 
		""" 
		return self._sz.func 

	@func.setter 
	def func(self, value): 
		if callable(value): 
			self._sz.func = fitting_function(value) 
		else: 
			raise TypeError("Must be a callable object. Got: %s" % (
				type(value))) 

	@property 
	def mode(self): 
		return self._sz.mode 

	@mode.setter 
	def mode(self, value): 
		self._sz.mode = value 

	@property 
	def verbose(self): 
		return self._sz.verbose 

	@verbose.setter 
	def verbose(self, value): 
		self._sz.verbose = value 

	@property 
	def elements(self): 
		return self._sz.elements 

	@elements.setter 
	def elements(self, value): 
		self._sz.elements = value 

	@property 
	def IMF(self): 
		return self._sz.IMF 

	@IMF.setter 
	def IMF(self, value): 
		if callable(value): 
			self._sz.IMF = fitting_function(value) 
		else: 
			self._sz.IMF = value 

	@property 
	def eta(self): 
		return self._sz.eta 

	@eta.setter 
	def eta(self, value): 
		if callable(value): 
			self._sz.eta = fitting_function(value) 
		else: 
			self._sz.eta = value 

	@property 
	def enhancement(self): 
		return self._sz.enhancement 

	@enhancement.setter 
	def enhancement(self, value): 
		self._sz.enhancement = value 

	@property 
	def entrainment(self): 
		return self._sz.entrainment 

	@property 
	def Zin(self): 
		return self._sz.Zin 

	@Zin.setter 
	def Zin(self, value): 
		self._sz.Zin = value 

	@property 
	def recycling(self): 
		return self._sz.recycling 

	@recycling.setter 
	def recycling(self, value): 
		self._sz.recycling = value 

	@property 
	def bins(self): 
		return self._sz.bins 

	@bins.setter 
	def bins(self, value): 
		self._sz.bins = value 

	@property 
	def delay(self): 
		return self._sz.delay 

	@delay.setter 
	def delay(self, value): 
		self._sz.delay = value 

	@property 
	def RIa(self): 
		return self._sz.RIa 

	@RIa.setter 
	def RIa(self, value): 
		if callable(value): 
			self._sz.RIa = fitting_function(value) 
		else: 
			self._sz.RIa = value 

	@property 
	def Mg0(self): 
		return self._sz.Mg0 

	@Mg0.setter 
	def Mg0(self, value): 
		self._sz.Mg0 = value 

	@property 
	def smoothing(self): 
		return self._sz.smoothing 

	@smoothing.setter 
	def smoothing(self, value): 
		self._sz.smoothing = value 

	@property 
	def tau_ia(self): 
		return self._sz.tau_ia 

	@tau_ia.setter 
	def tau_ia(self, value): 
		self._sz.tau_ia = value 

	@property 
	def tau_star(self): 
		return self._sz.tau_star 

	@tau_star.setter 
	def tau_star(self, value): 
		if callable(value): 
			self._sz.tau_star = fitting_function(value) 
		else: 
			self._sz.tau_star = value 

	@property 
	def dt(self): 
		return self._sz.dt 

	@dt.setter 
	def dt(self, value): 
		self._sz.dt = value 

	@property 
	def schmidt(self): 
		return self._sz.schmidt 

	@schmidt.setter 
	def schmidt(self, value): 
		self._sz.schmidt = value 

	@property 
	def MgSchmidt(self): 
		return self._sz.MgSchmidt 

	@MgSchmidt.setter 
	def MgSchmidt(self, value): 
		self._sz.MgSchmidt = value 

	@property 
	def schmidt_index(self): 
		return self._sz.schmidt_index 

	@schmidt_index.setter 
	def schmidt_index(self, value): 
		self._sz.schmidt_index = value 

	@property 
	def m_upper(self): 
		return self._sz.m_upper 

	@m_upper.setter 
	def m_upper(self, value): 
		self._sz.m_upper = value 

	@property 
	def m_lower(self): 
		return self._sz.m_lower 

	@m_lower.setter 
	def m_lower(self, value): 
		self._sz.m_lower = value 

	@property 
	def postMS(self): 
		return self._sz.postMS 

	@postMS.setter 
	def postMS(self, value): 
		self._sz.postMS = value 

	@property 
	def Z_solar(self): 
		return self._sz.Z_solar 

	@Z_solar.setter 
	def Z_solar(self, value): 
		self._sz.Z_solar = value 

	@property 
	def agb_model(self): 
		return self._sz.agb_model 

	@agb_model.setter 
	def agb_model(self, value): 
		self._sz.agb_model = value 

	@property 
	def data(self): 
		return self._data 



