r""" 
This file implements star formation efficiency timescales. 
""" 

import numbers 

class sfe: 

	r""" 
	Star formation efficiency timescale as a function of simulation time. 

	Parameters 
	----------
	**kwargs : real numbers 
		Both attributes can be assigned via keyword arguments. See below. 

	Attributes 
	----------
	baseline : real number 
		The depletion time of molecular gas at the present day in Gyr. 
		Positive definite. 
	index : real number 
		The power-law index on the time-dependence. 

	Calling 
	-------
	This object can be called with simulation time as required for the 
	Johnson et al. (2021) simulations to determine the star formation 
	efficiency at that time. 

	Notes 
	-----
	The depletion time due to star formation of molecular gas 
	:math:`\tau_\star^\text{mol}` is defined according to the following 
	scaling: 

	.. math:: \tau_\star^\text{mol} = \tau_{\star,0}^\text{mol} 
		\left(t/t_0\right)^\beta 

	where :math:`t_0` is the age of the universe today and :math:`t` is the 
	age of the universe at some time in the simulation. Because the 
	simulations run for 12.8 Gyr, the relation between age of the universe and 
	simulation time is a simple linear translation of 1 Gyr: 

	.. math:: t = t_\text{sim} + 1 \text{Gyr} 

	This class assumes :math:`t_0` = 13.8 Gyr as the age of the universe at 
	the present day. 
	""" 

	def __init__(self, baseline = 2, index = 0): 
		self.baseline = baseline 
		self.index = index 

	def __call__(self, time): 
		return self.baseline * ((time + 1) / 13.8)**self.index 

	@property 
	def baseline(self): 
		r""" 
		Type : float 

		Default : 2 

		The depletion timescale of molecular gas at the present day, in Gyr. 
		""" 
		return self._baseline 

	@baseline.setter 
	def baseline(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				self._baseline = float(value) 
			else: 
				raise ValueError("Baseline must be positive. Got: %g" % (
					value)) 
		else: 
			raise TypeError("Baseline must be a numerical value. Got: %s" % (
				type(value))) 

	@property 
	def index(self): 
		r""" 
		Type : float 

		Default : 0 (time-independent) 

		The power-law index on the time-dependence of the molecular gas 
		depletion time. 
		""" 
		return self._index 

	@index.setter 
	def index(self, value): 
		if isinstance(value, numbers.Number): 
			self._index = float(value) 
		else: 
			raise TypeError("Index must be a numerical value. Got: %s" % (
				type(value))) 

