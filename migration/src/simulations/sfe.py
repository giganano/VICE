r""" 
This file implements star formation efficiency timescales. 
""" 

import numbers 

class sfe: 

	# Sigma_g2 = 2.e7 # Msun kpc^-2 
	# Sigma_g1 = 5.e6 # Msun kpc^-2 
	# beta1 = -1.6 # unitless power-law index 
	# beta2 = -0.7 # unitless power-law index 

	r""" 
	Star formation efficiency timescale as a function of simulation time and 
	star formation rate. 

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
	simulations run for 12.2 Gyr, the relation between age of the universe and 
	simulation time is a simple linear translation of 1 Gyr: 

	.. math:: t = t_\text{sim} + 1.5 \text{Gyr} 

	This class assumes :math:`t_0` = 13.7 Gyr as the age of the universe at 
	the present day. 
	""" 

	def __init__(self, area, present_day_molecular = 2, molecular_index = 0.5, 
		Sigma_g2 = 2.0e+07, Sigma_g1 = 5.0e+06, index2 = 3.6, index1 = 1.7): 
		self.area = area 
		self.present_day_molecular = present_day_molecular 
		self.molecular_index = molecular_index 
		self.Sigma_g2 = Sigma_g2 
		self.Sigma_g1 = Sigma_g1 
		self.index2 = index2 
		self.index1 = index1 

	def __call__(self, time, sfr): 
		Sigma_sfr = sfr / self.area # convert to surface density 
		Sigma_sfr *= 1e9 # yr^-1 -> Gyr^-1 
		molecular = self.molecular(time) 
		Sigma_sfr2 = self.Sigma_g2 / molecular 
		Sigma_sfr1 = (self.Sigma_g1 / self.Sigma_g2)**(
				self._index2 * (1 - self._index2) / 
				(self._index2 - self._index1) 
			) / molecular * self.Sigma_g2**(
				self._index2 * (1 - self._index1) / 
				(self._index2 - self._index1) 
			) * self.Sigma_g1**(
				-self._index1 * (1 - self._index2) / 
				(self._index2 - self._index1) 
			) 
		if Sigma_sfr >= Sigma_sfr2: 
			return molecular 
		elif Sigma_sfr1 <= Sigma_sfr <= Sigma_sfr2: 
			return molecular**(1 / (1 - self._index2)) * (
				Sigma_sfr / self.Sigma_g2
			)**(self._index2 / (1 - self._index2)) 
		elif Sigma_sfr: 
			return (self.Sigma_g1 / self.Sigma_g2)**(
				self._index2 / (1 - self._index1) 
			) * molecular**(1 / (1 - self._index1)) * (
				Sigma_sfr / self.Sigma_g1 
			)**(self._index1 / (1 - self._index1)) 
		else: 
			# avoid ZeroDivisionError if sfr == 0 
			return 1.e-12 # will result in mgas = 0 regardless 


	@property 
	def area(self): 
		r""" 
		Type : float 

		The surface area of the star forming disk in kpc:math:`^{-2}` for 
		which this object represents the star formation efficiency timescale. 
		""" 
		return self._area 

	@area.setter 
	def area(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				self._area = float(value) 
			else: 
				raise ValueError("Must be positive. Got: %g" % (value)) 
		else: 
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value))) 

	def molecular(self, time): 
		r""" 
		Calculate the star formation efficiency timescale at a given 
		simulation time. 

		Parameters 
		----------
		time : float 
			The simulation time in Gyr. 

		Returns 
		-------
		tau_star_mol : float 
			The star formation efficiency timescale :math:`\tau_\star` for 
			molecular gas only, defined accordingly: 

			.. math:: \tau_\star^\text{mol} = \tau_{\star,0}^\text{mol} 
				\left(\frac{1 + t}{t_0}\right)^\beta 

			where :math:`\tau_{\star,0}` is the value of 
			:math:`\tau_\star^\text{mol}` at the present day, :math:`t_0` is 
			the present-day age of the universe (assumed to be 13.7 Gyr), 
			:math:`\beta` is the power-law index, and :math:`t` is the 
			parameter ``time`` passed to this function. A value of 1 is added, 
			because the onset of star formation is assumed to be 1 Gyr 
			following the Big Bang in the Johnson et al. (2021) models. 
		""" 
		return self.present_day_molecular * (
			(1.5 + time) / 13.7)**self.molecular_index 

	@property 
	def present_day_molecular(self): 
		r""" 
		Type : float 

		Default : 2 

		The star formation efficiency timescale of molecular gas at the 
		present day, in Gyr. Scales with time according to a power-law whose 
		index is given by the value of the attribute ``molecular_index``. 
		""" 
		return self._present_day_molecular 

	@present_day_molecular.setter 
	def present_day_molecular(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				self._present_day_molecular = float(value) 
			else: 
				raise ValueError("Must be positive. Got: %g" % (value)) 
		else: 
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value))) 

	@property 
	def molecular_index(self): 
		r""" 
		Type : float 

		Default: 0.5 

		The power-law index on the time-dependence of the molecular gas star 
		formation efficiency timescale. It will scale such that the value at 
		t = 12.2 Gyr is equal to the value of the attribute 
		``present_day_molecular``. 
		""" 
		return self._molecular_index 

	@molecular_index.setter 
	def molecular_index(self, value): 
		if isinstance(value, numbers.Number): 
			self._molecular_index = float(value) 
		else: 
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value))) 

	@property 
	def Sigma_g2(self): 
		r""" 
		Type : float 

		Default: 2.0e+07 

		The surface density of gas in M:math:`\odot` kpc:math:`^{-2}` above 
		which the Kennicutt-Schmidt relation (surface density of star 
		formation as a function of gas surface density) is linear. 

		.. note:: The value of this attribute should be greater than that of 
			the attribute ``Sigma_g1``, though this is not enforced. 
		""" 
		return self._Sigma_g2 

	@Sigma_g2.setter 
	def Sigma_g2(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				self._Sigma_g2 = float(value) 
			else: 
				raise ValueError("Must be positive. Got: %g" % (value)) 
		else: 
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value))) 

	@property 
	def Sigma_g1(self): 
		r""" 
		Type : float 

		Default : 5.0e+06 

		The surface density of gas in M:math:`\odot` kpc:math:`^{-2}`, above 
		which the Kennicutt-Schmidt relation (surface density of star 
		formation as a function of gas surface density) has the power-law 
		index of the attribute ``index2``. This power-law index will be 
		effective in the range between this attribute and ``Sigma_g```. Below 
		this value, the power-law index is the value of the attribute 
		``index1``. 

		.. note:: The value of this attribute should be smaller than that of 
			the attribute ``Sigma_g2``, though this is not enforced. 
		""" 
		return self._Sigma_g1 

	@Sigma_g1.setter 
	def Sigma_g1(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				self._Sigma_g1 = float(value) 
			else: 
				raise ValueError("Must be positive. Got: %g" % (value)) 
		else: 
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value))) 

	@property 
	def index2(self): 
		r""" 
		Type : float 

		Default : 3.6 

		The power-law index of the Kennicutt-Schmidt relation (surface density 
		of star formation as a function of the gas surface density) between 
		the gas surface densities of the attributes ``Sigma_g1`` and 
		``Sigma_g2``. 

		.. note:: This attribute stores a different value under the hood 
			for the purpose of optimizing the Johnson et al. (2021) model 
			simulations. 
		""" 
		return -self._index2 + 1 

	@index2.setter 
	def index2(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				# Store the index of the \tau_\star-\Sigma_gas relation 
				self._index2 = -(float(value) - 1) 
			else: 
				raise ValueError("Must be positive. Got: %g" % (value)) 
		else: 
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value))) 

	@property 
	def index1(self): 
		r""" 
		Type : float 

		Default : 1.7 

		The power-law index of the Kennicutt-Schmidt relation (surface density 
		of star formation as a function of the gas surface density) below the 
		gas surface density of the attribute ``Sigma_g1``. 

		.. note:: This attribute sotres a different value under the hood 
			for the purpose of optimizing the Johnson et al. (2021) model 
			simulations. 
		""" 
		return -self._index1 + 1 

	@index1.setter 
	def index1(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				# Store the index of the \tau_\star-\Sigma_gas relation 
				self._index1 = -(float(value) - 1) 
			else: 
				raise ValueError("Must be positive. Got: %g" % (value)) 
		else: 
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value))) 

