r"""
This file declares the time-dependence of the star formation history at a
given radius in the constant SFH model from Johnson et al. (2021).
"""

from .utils import constant
from .normalize import normalize
from .gradient import gradient
import math as m
import os


class static(constant):

	r"""
	The constant SFH model from Johnson et al. (2021).

	Parameters
	----------
	radius : float
		The galactocentric radius in kpc of a given annulus in the model.
	dt : float [default : 0.01]
		The timestep size of the model in Gyr.
	dr : float [default : 0.1]
		The width of the annulus in kpc.

	All attributes and functionality are inherited from ``constant`` declared
	in ``src/simulations/models/utils.py``.
	"""

	def __init__(self, radius, dt = 0.01, dr = 0.1):
		super().__init__()
		self.amplitude *= normalize(self, gradient, radius, dt = dt, dr = dr)

