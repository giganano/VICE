r""" 
The diskmodel objects employed in the Johnson et al. (2021) study. 
""" 

try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 
try: 
	import vice 
except (ModuleNotFoundError, ImportError): 
	raise ModuleNotFoundError("Could not import VICE.") 
if vice.version[:2] < (1, 2): 
	raise RuntimeError("""VICE version >= 1.2.0 is required to produce \
Johnson et al. (2021) figures. Current: %s""" % (vice.__version__)) 
else: pass 
from vice.yields.presets import JW20 
from vice.toolkit import hydrodisk 
from .config import config 
from . import scalings 
from . import stars 
import sys 


class diskmodel(vice.multizone): 

	# evolutionary parameters need added to this before it can be ran properly 
	def __init__(self, name = "diskmodel", mode = "linear"): 
		super().__init__(
			name = name, 
			n_zones = len(config.radial_bins) - 1, 
			n_stars = config.star_particle_density, 
			verbose = True, 
			simple = False 
		) 
		self.migration.stars = stars.diskmigration(config.radial_bins, 
			mode = mode, filename = "%s_analogdata.out" % (name)) 
		for i in range(self.n_zones): 
			self.zones[i].mode = "sfr" 
			self.zones[i].bins = [-3 + 0.01 * i for i in range(401)] 
			self.zones[i].elements = ["fe", "o"] 
			self.zones[i].dt = config.timestep_size 
			self.zones[i].Mg0 = 0 
			self.zones[i].schmidt = True 
			if i > 61: 
				self.zones[i].func = lambda t: 0 
				self.zones[i].tau_star = 100 
				self.zones[i].eta = 100 
				for j in self.zones[i].elements: 
					self.zones[i].entrainment.agb[j] = 0 
					self.zones[i].entrainment.ccsne[j] = 0 
					self.zones[i].entrainment.sneia[j] = 0 
			else: 
				self.zones[i].tau_star = scalings.tau_star(
					config.zone_width * (i + 0.5), 
					norm = config.tau_star_norm, 
					scale = config.scale_radius)  


	def run(self): 
		super().run(config.output_times, overwrite = True) 

		# diskmigration object used here has this function 
		self.migration.stars.close_file() 


# class linear(diskmodel): 

# 	def __init__(self, name = "diskmodel"): 
# 		super().__init__(self, name = name) 
# 		self.migration.stars = stars.diskmigration(config.radial_bins, 
# 			mode = "linear", filename = "%s_analogdata.out" % (name)) 


# class sudden(diskmodel): 

# 	def __init__(self, name = "diskmodel"): 
# 		super().__init__(self, name = name) 
# 		self.migration.stars = stars.diskmigration(config.radial_bins, 
# 			mode = "sudden", filename = "%s_analogdata.out" % (name)) 


# class diffusion(diskmodel): 

# 	def __init__(self, name = "diskmodel"): 
# 		super().__init__(self, name = name) 
# 		self.migration.stars = stars.diskmigration(config.radial_bins, 
# 			mode = "diffusion", filename = "%s_analogdata.out" % (name)) 

