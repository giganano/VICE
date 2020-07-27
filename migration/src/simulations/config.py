
from vice import ScienceWarning 
import warnings 
import numbers 

class config: 

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
	def radial_bins(self): 
		r""" 
		Type : list 

		The radial bin edges in kpc describing the multizone disk model. 
		""" 
		return [self.zone_width * i for i in range(int(self.max_radius / 
			self.zone_width) + 1)] 

	@property 
	def max_radius(self): 
		r""" 
		Type : float 

		The outermost radius for the multizone model annuli in kpc. 
		""" 
		return 30. 

	@property 
	def scale_radius(self): 
		r""" 
		Type : float 

		The scale radius of the stellar disk in kpc. 
		""" 
		return self._scale_radius 

	@scale_radius.setter 
	def scale_radius(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				self._scale_radius = float(value) 
			else: 
				raise ValueError("Scale radius must be positive.") 
		else: 
			raise TypeError("Scale radius must be a numerical value.") 

	@property 
	def tau_star_norm(self): 
		r""" 
		Type : float 

		The value of the star formation efficiency timescale at the center of 
		the galaxy disk (i.e. at R = 0). 
		""" 
		return self._tau_star_norm 

	@tau_star_norm.setter 
	def tau_star_norm(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				self._tau_star_norm = float(value) 
			else: 
				raise ValueError("SFE timescale normalization must be positive.") 
		else: 
			raise TypeError("""SFE timescale normalization must be a \
numerical value.""") 


config = config() 
config.timestep_size = 0.05 
config.star_particle_density = 1 
config.zone_width = 0.25 
config.scale_radius = 3 
config.tau_star_norm = 0.05 

