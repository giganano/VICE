
from vice import ScienceWarning 
import warnings 
import numbers 

class config: 

	def __init__(self, **kwargs): 
		defaults = {
			"timestep_size": 			0.01, 
			"star_particle_density":	2, 
			"zone_width": 				0.1, 
			"elements": 				["fe", "o"], 
			"tau_star_mol": 			2, 
			"bins": 					[-3 + 0.01 * i for i in range(601)] 
		} 
		for i in kwargs.keys(): defaults[i] = kwargs[i] 
		self.timestep_size = 			defaults["timestep_size"] 
		self.star_particle_density = 	defaults["star_particle_density"] 
		self.zone_width = 				defaults["zone_width"] 
		self.elements = 				defaults["elements"] 
		self.tau_star_mol = 			defaults["tau_star_mol"] 
		self.bins = 					defaults["bins"] 

	@property 
	def timestep_size(self): 
		r""" 
		Type : float 

		The timestep size of the simulations in Gyr. 
		""" 
		return self._timestep_size 

	@timestep_size.setter 
	def timestep_size(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0.05: warnings.warn("""\
Large timestep size: %g. This may cause numerical artifacts.\
""" % (value), ScienceWarning) 
			if value > 0: 
				self._timestep_size = value 
			else: 
				raise ValueError("Timestep size must be positive.") 
		else: 
			raise TypeError("Timestep size must be a real number. Got: %s" % (
				type(value))) 

	@property 
	def output_times(self): 
		r""" 
		Type : list 

		The output times of the simulation in Gyr. 
		""" 
		return [self.timestep_size * i for i in range(int(self.endtime / 
			self.timestep_size) + 1)] 

	@property 
	def endtime(self): 
		r""" 
		Type : float 

		The amount of time to run the simulation for in Gyr. 
		""" 
		return 12.8 

	@property 
	def star_particle_density(self): 
		r""" 
		Type : int 

		The number of star particles per zone per timestep in each simulation. 
		""" 
		return self._star_particle_density 

	@star_particle_density.setter 
	def star_particle_density(self, value): 
		if isinstance(value, numbers.Number) and value % 1 == 0: 
			if value > 0: 
				self._star_particle_density = int(value) 
			else: 
				raise ValueError("Star particle density must be positive.") 
		else: 
			raise TypeError("""\
Star particle density must be an integer. Got: %s""" % (type(value))) 

	@property 
	def zone_width(self): 
		r""" 
		Type : float 

		The width of each annulus in the multizone models in kpc. 
		""" 
		return self._zone_width 

	@zone_width.setter 
	def zone_width(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				self._zone_width = value 
			else: 
				raise ValueError("Zone width must be positive.") 
		else: 
			raise TypeError("Zone width must be a real number. Got: %s" % (
				type(value))) 

	@property 
	def max_radius(self): 
		r""" 
		Type : real number 

		The maximum radius in kpc of the disk model. 
		""" 
		return 20. 

	@property 
	def elements(self): 
		r""" 
		Type : list 

		The symbols of the elements to simulate the enrichment for. 
		""" 
		return self._elements 

	@elements.setter 
	def elements(self, value): 
		if isinstance(value, list): 
			if all([isinstance(i, str) for i in value]): 
				self._elements = value 
			else: 
				raise ValueError("All elements must be of type str.") 
		else: 
			raise TypeError("Expected type list. Got: %s" % (type(value))) 

	@property 
	def tau_star_mol(self): 
		r""" 
		Type : real number or <function> 

		The depletion time of molecular gas due to star formation. Either a 
		constant, time-independent value, or a function of time in Gyr. 
		""" 
		return self._tau_star_mol 

	@tau_star_mol.setter 
	def tau_star_mol(self, value): 
		if isinstance(value, numbers.Number) or callable(value): 
			self._tau_star_mol = value 
		else: 
			raise TypeError("Expected a real number or function. Got: %s" % (
				type(value))) 

	@property 
	def bins(self): 
		r""" 
		Type : list 

		The bins to sort metallicity distribution functions into. This will 
		be assigned as the 'bins' attribute to the ``milkyway`` object. 
		""" 
		return self._bins 

	@bins.setter 
	def bins(self, value): 
		if isinstance(value, list): 
			if all([isinstance(i, numbers.Number) for i in value]): 
				self._bins = value 
			else: 
				raise ValueError("Non-numerical value detected.") 
		else: 
			raise TypeError("Must be of type list. Got: %s" % (type(value))) 

