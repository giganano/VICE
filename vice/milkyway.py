
from __future__ import absolute_import 
__all__ = ["milkyway"] 
from .core.multizone import multizone 
from .core import _pyutils 
from .toolkit.hydrodisk import hydrodiskstars 
import numbers 

_MIN_RADIUS_ = 0 # The minimum radius of the radial bins in kpc 
_MAX_RADIUS_ = 20 # The maximum radius of the radial bins in kpc 


class milkyway(multizone): 

	r""" 
	An object designed for running chemical evolution models of Milky Way-like 
	spiral galaxies. Inherits from vice.multizone. 

	**Signature**: vice.milkyway(radial_bins, name = "milkyway", n_stars = 1, 
	simple = False, verbose = False) 
	""" 

	def __new__(cls, zone_width = 0.5, **kwargs): 
		radial_bins = _get_radial_bins(zone_width) 
		return super().__new__(cls, n_zones = len(radial_bins) - 1) 


	def __init__(self, zone_width = 0.5, name = "milkyway", n_stars = 1, 
		simple = False, verbose = False, N = 1e5, mode = "linear"): 
		radial_bins = _get_radial_bins(zone_width) 
		super().__init__(name = name, n_zones = len(radial_bins) - 1, 
			n_stars = n_stars, simple = simple, verbose = verbose) 
		self.migration.stars = hydrodiskstars(radial_bins, N = N, mode = mode) 

	@property 
	def annuli(self): 
		r""" 
		Type : list 

		The radii representing divisions between annuli in the disk model in 
		kpc. This property is determined by the ``zone_width`` attribute, and 
		can only be set at initialize of the ``milkyway`` object. 

		Example Code 
		------------
		>>> import vice 
		>>> example = vice.milkyway(name = "example", zone_width = 0.2) 
		>>> example.annuli 
		[0.0, 
		 0.2, 
		 0.4, 
		 ..., 
		 19.6, 
		 19.8, 
		 20.0] 
		""" 
		return self.migration.stars.radial_bins 

	@property 
	def zone_width(self): 
		r""" 
		Type : float [default : 0.5] 

		The width of each annulus in kpc. This value can only be set at 
		initialization of the ``milkyway`` object. 

		Example Code 
		------------
		>>> import vice
		>>> example = vice.milkyway(name = "example", zone_width = 0.2) 
		>>> example.zone_width 
		0.2 
		""" 
		return self.annuli[1] - self.annuli[0] 

	@property 
	def dt(self): 
		r""" 
		Type : float 

		The timestep size in Gyr. 

		Example Code 
		------------
		>>> import vice 
		>>> example = vice.milkyway(name = "example", zone_width = 0.2) 
		>>> example.dt 
		0.01 
		>>> example.dt = 0.02 
		>>> example.dt 
		0.02 
		""" 
		return self.zones[0].dt 

	@dt.setter 
	def dt(self, value): 
		# Let the singlezone object do the error handling 
		for i in range(self.n_zones): 
			self.zones[i].dt = value 


def _get_radial_bins(zone_width): 
	r""" 
	Get the radial bins associated with a multizone model. 

	Parameters 
	----------
	zone_width : float 
		The width of each zone in kpc. 

	Returns 
	-------
	radii : list 
		The least-to-greatest sorted list of radii that serve as the divisions 
		between annuli in the multizone disk model. 

	Raises 
	------ 
	* ValueError 
		- zone_width is not positive 
	* TypeError 
		- zone_width is not a numerical value 

	Notes 
	-----
	If the zone_width is any larger than the difference between maximum and 
	minimum radii (declared in this file), then the returned radii will be 
	a list containing only those two values. 
	""" 
	if isinstance(zone_width, numbers.Number): 
		if zone_width > _MAX_RADIUS_ - _MIN_RADIUS_: 
			return [_MIN_RADIUS_, _MAX_RADIUS_] 
		elif zone_width > 0: 
			return _pyutils.range_(_MIN_RADIUS_, _MAX_RADIUS_, zone_width) 
		else: 
			raise ValueError("Zone width must be positive. Got: %g" % (
				zone_width)) 
	else: 
		raise TypeError("Zone width must be a numerical value. Got: %s" % (
			type(zone_width))) 

