
from __future__ import absolute_import 
from ._singlechain import c_singlechain 

class singlechain: 

	def __init__(self, **kwargs): 
		self.__c_version = c_singlechain(**kwargs) 

	def __repr__(self): 
		return self.__c_version.__repr__() 

	def __str__(self): 
		return self.__repr__() 

	def __enter__(self): 
		return self 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		return exc_value is None 

	@property 
	def name(self): 
		""" 
		Type :: str 

		The name of the singlechain fit. 
		""" 
		return self._name 

	@name.setter 
	def name(self, value): 
		self.__c_version.name = value 

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
		return self.__c_version.func 

	@func.setter 
	def func(self, value): 
		self.__c_version.func = value 

	@property 
	def mode(self): 
		return self.__c_version.mode 

	@mode.setter 
	def mode(self, value): 
		self.__c_version.mode = value 

	@property 
	def verbose(self): 
		return self.__c_version.verbose 

	@verbose.setter 
	def verbose(self, value): 
		self.__c_version.verbose = value 

	@property 
	def elements(self): 
		return self.__c_version.elements 

	@elements.setter 
	def elements(self, value): 
		self.__c_version.elements = value 

	@property 
	def IMF(self): 
		return self.__c_version.IMF 

	@IMF.setter 
	def IMF(self, value): 
		self.__c_version.IMF = value 

	@property 
	def eta(self): 
		return self.__c_version.eta 

	@eta.setter 
	def eta(self, value): 
		self.__c_version.eta = value 

	@property 
	def enhancement(self): 
		return self.__c_version.enhancement 

	@enhancement.setter 
	def enhancement(self, value): 
		self.__c_version.enhancement = value 

	@property 
	def entrainment(self): 
		return self.__c_version.entrainment 

	@property 
	def Zin(self): 
		return self.__c_version.Zin 

	@Zin.setter 
	def Zin(self, value): 
		self.__c_version.Zin = value 

	@property 
	def recycling(self): 
		return self.__c_version.recycling 

	@recycling.setter 
	def recycling(self, value): 
		self.__c_version.recycling = value 

	@property 
	def bins(self): 
		return self.__c_version.bins 

	@bins.setter 
	def bins(self, value): 
		self.__c_version.bins = value 

	@property 
	def delay(self): 
		return self.__c_version.delay 

	@delay.setter 
	def delay(self, value): 
		self.__c_version.delay = value 

	@property 
	def RIa(self): 
		return self.__c_version.RIa 

	@RIa.setter 
	def RIa(self, value): 
		self.__c_version.RIa = value 

	@property 
	def Mg0(self): 
		return self.__c_version.Mg0 

	@Mg0.setter 
	def Mg0(self, value): 
		self.__c_version.Mg0 = value 

	@property 
	def smoothing(self): 
		return self.__c_version.smoothing 

	@smoothing.setter 
	def smoothing(self, value): 
		self.__c_version.smoothing = value 

	@property 
	def tau_ia(self): 
		return self.__c_version.tau_ia 

	@tau_ia.setter 
	def tau_ia(self, value): 
		self.__c_version.tau_ia = value 

	@property 
	def tau_star(self): 
		return self.__c_version.tau_star 

	@tau_star.setter 
	def tau_star(self, value): 
		self.__c_version.tau_star = value 

	@property 
	def dt(self): 
		return self.__c_version.dt 

	@dt.setter 
	def dt(self, value): 
		self.__c_version.dt = value 

	@property 
	def schmidt(self): 
		return self.__c_version.schmidt 

	@schmidt.setter 
	def schmidt(self, value): 
		self.__c_version.schmidt = value 

	@property 
	def MgSchmidt(self): 
		return self.__c_version.MgSchmidt 

	@MgSchmidt.setter 
	def MgSchmidt(self, value): 
		self.__c_version.MgSchmidt = value 

	@property 
	def schmidt_index(self): 
		return self.__c_version.schmidt_index 

	@schmidt_index.setter 
	def schmidt_index(self, value): 
		self.__c_version.schmidt_index = value 

	@property 
	def m_upper(self): 
		return self.__c_version.m_upper 

	@m_upper.setter 
	def m_upper(self, value): 
		self.__c_version.m_upper = value 

	@property 
	def m_lower(self): 
		return self.__c_version.m_lower 

	@m_lower.setter 
	def m_lower(self, value): 
		self.__c_version.m_lower = value 

	@property 
	def postMS(self): 
		return self.__c_version.postMS 

	@postMS.setter 
	def postMS(self, value): 
		self.__c_version.postMS = value 

	@property 
	def Z_solar(self): 
		return self.__c_version.Z_solar 

	@Z_solar.setter 
	def Z_solar(self, value): 
		self.__c_version.Z_solar = value 

	@property 
	def agb_model(self): 
		return self.__c_version.agb_model 

	@agb_model.setter 
	def agb_model(self, value): 
		self.__c_version.agb_model = value 

