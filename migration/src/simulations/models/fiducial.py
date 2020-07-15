r""" 
The fiducial model simulation. 
""" 

from ..disks import linear, sudden, diffusion 
from ..utils import linear_exponential 
from ..config import config 
import math as m 
import numbers 


class sfh(linear_exponential): 

	def __init__(self, rgal, scale = 3): 
		self.scale = scale 
		self.timescale = sfh.tau_sfh(rgal) # needed to self.norm 
		super().__init__(
			norm = self.norm(rgal), 
			timescale = sfh.tau_sfh(rgal) 
		) 

	@property 
	def scale(self): 
		r""" 
		Type : float 

		The scale radius of the resultant stellar disk in the multizone 
		simulation. 
		""" 
		return self._scale 

	@scale.setter 
	def scale(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				self._scale = value 
			else: 
				raise ValueError("Scale radius must be positive.") 
		else: 
			raise TypeError("Scale radius must be a real number. Got: %s" % (
				type(value))) 

	def norm(self, rgal): 
		r""" 
		The normalization of the star formation history as a function of 
		galactocentric radius. 

		Parameters 
		----------
		rgal : real number 
			Galactocentric radius in kpc 

		Returns 
		-------
		norm : real number 
			The normalization of the star formation history in 
			:math:`M_\odot/yr`. 
		""" 
		return self.timescale**(-2) * (
			1 - (1 + config.endtime / self.timescale) * m.exp(
				-config.endtime / self.timescale
			) 
		)**(-1) * rgal * m.exp(-rgal / self.scale) 


	@staticmethod 
	def tau_sfh(rgal): 
		r""" 
		Star formation history timescale as a function of galactocentric 
		radius. 

		Parameters 
		----------
		rgal : real number  
			Galactocentric radius in kpc 

		Returns 
		-------
		tau_sfh : real number  
			The e-folding timescale of the star formation history at that 
			radius in Gyr. 
		""" 
		return 3 + (rgal + 1e-12) / 2.5 


def main(mode = "linear"): 
	r""" 
	Runs the fiducial model under one of the three adopted migration schemes. 

	Parameters 
	----------
	mode : str [case-insensitive] [default : "linear"] 
		The mode of radial migration. Either "linear", "sudden", or "diffusion" 
	""" 
	model = {
		"linear": 		linear, 
		"sudden": 		sudden, 
		"diffusion": 	diffusion 
	}[mode.lower()](name = "fiducial_%s" % (mode)) 
	for i in range(model.n_zones): 
		model.zones[i].func = sfh(
			(config.radial_bins[i] + config.radial_bins[i + 1]) / 2
		)  
	model.run() 

