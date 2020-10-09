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
vice.yields.sneia.settings['fe'] *= 10**0.1 
from . import migration 
from . import scalings 
from . import models 
from .models.utils import get_bin_number, interpolate 
from .models.gradient import gradient 
import sys 


class diskmodel(vice.milkyway): 

	def __init__(self, zone_width = 0.1, name = "diskmodel", spec = "static", 
		verbose = True, migration_mode = "linear", max_radius = 20, **kwargs): 
		super().__init__(zone_width = zone_width, name = name, 
			verbose = verbose, **kwargs) 
		Nstars = 2 * int(15.5 / zone_width * 12.8 / self.dt * self.n_stars) 
		self.migration.stars = migration.diskmigration(self.annuli, N = Nstars, 
			mode = migration_mode, filename = "%s_analogdata.out" % (name)) 
		self.evolution = star_formation_history(spec = spec, 
			zone_width = zone_width, max_radius = max_radius) 
		self.mode = "sfr" 

	def run(self, *args, **kwargs): 
		out = super().run(*args, **kwargs) 
		self.migration.stars.close_file() 
		return out 

	@classmethod 
	def from_config(cls, config, **kwargs): 
		r""" 
		Obtain a ``diskmodel`` object with the parameters encoded into a 
		``config`` object. 

		**Signature**: diskmodel.from_config(config, **kwargs) 

		Parameters 
		----------
		config : ``config`` 
			The ``config`` object with the parameters encoded as attributes. 
			See src/simulations/config.py. 
		**kwargs : varying types 
			Additional keyword arguments to pass to ``diskmodel.__init__``. 

		Returns 
		-------
		model : ``diskmodel`` 
			The ``diskmodel`` object with the proper settings. 
		""" 
		model = cls(zone_width = config.zone_width, 
			max_radius = config.max_radius, **kwargs) 
		model.dt = config.timestep_size 
		model.n_stars = config.star_particle_density 
		model.tau_star_mol = config.tau_star_mol 
		model.bins = config.bins 
		model.elements = config.elements 
		return model 


class star_formation_history: 

	def __init__(self, spec = "static", zone_width = 0.1, max_radius = 20): 
		self._radii = [] 
		self._evol = [] 
		i = 0 
		while (i + 1) * zone_width < max_radius: 
			self._radii.append((i + 0.5) * zone_width) 
			self._evol.append({
					"static": 		models.static, 
					"insideout": 	models.insideout, 
					"lateburst": 	models.lateburst, 
					"outerburst": 	models.outerburst 
				}[spec.lower()]((i + 0.5) * zone_width)) 
			i += 1 

	def __call__(self, radius, time): 
		# The milkyway object will always call this with a radius in the 
		# self._radii array, but this ensures a continuous function of radius 
		idx = get_bin_number(self._radii, radius) 
		if idx != -1: 
			return gradient(radius) * interpolate(self._radii[idx], 
				self._evol[idx](time), self._radii[idx + 1], 
				self._evol[idx + 1](time), radius) 
		else: 
			return gradient(radius) * interpolate(self._radii[-2], 
				self._evol[-2](time), self._radii[-1], self._evol[-1](time), 
				radius) 

