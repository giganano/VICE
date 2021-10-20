r"""
This file implements the config object, which is used to store the user's
model parameters before creating a ``diskmodel`` object from them.
"""

from vice import ScienceWarning
from vice import milkyway
import warnings
import numbers

class config:

	r"""
	Stores model parameters before creation of a ``diskmodel`` object.

	Parameters
	----------
	kwargs : varying types
		Attributes can be initialized via keyword arguments. See below.

	Attributes
	----------
	timestep_size : float [default : 0.01]
		The timestep size of the model in Gyr.
	star_particle_density : int [default : 2]
		The number of stellar populations per zone per timestep in the model.
	zone_width : float [default : 0.1]
		The width of each annulus in kpc in the model. Must be positive.
	elements : list [default : ["fe", "o"]]
		The elements to calculate the enrichment for. Components must be of
		type ``str`` and correspond to elements recognized by VICE.
	bins : list [default : [-3, -2.99, -2.98, ... , 2.98, 2.99, 3.00]]
		The bins within which to sort the dN/d[X/Y] abundance distributions
		into.
	"""

	def __init__(self, **kwargs):
		defaults = {
			"timestep_size": 			0.01,
			"star_particle_density":	2,
			"zone_width": 				0.1,
			"elements": 				["fe", "o"],
			"bins": 					[-3 + 0.01 * i for i in range(601)],
		}
		for i in kwargs.keys(): defaults[i] = kwargs[i]
		self.timestep_size = 			defaults["timestep_size"]
		self.star_particle_density = 	defaults["star_particle_density"]
		self.zone_width = 				defaults["zone_width"]
		self.elements = 				defaults["elements"]
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

	# @property
	# def max_radius(self):
	# 	r"""
	# 	Type : real number

	# 	The maximum radius in kpc of the disk model.
	# 	"""
	# 	return 20.

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

