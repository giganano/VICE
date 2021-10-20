r"""
This file declares the time-dependence of the star formation history at a
given radius in the lateburst model from Johnson et al. (2021).
"""

from ..._globals import END_TIME
from .utils import modified_exponential, gaussian
from .insideout import _TAU_RISE_, insideout
from .normalize import normalize
from .gradient import gradient
import math as m
import os

_BURST_TIME_ = END_TIME - 2 # Gyr


class lateburst(modified_exponential, gaussian):

	r"""
	The late-burst SFH model from Johnson et al. (2021).

	Parameters
	----------
	radius : float
		The galactocentric radius in kpc of a given annulus in the model.
	dt : float [default : 0.01]
		The timestep size of the model in Gyr.
	dr : float [default : 0.1]
		The width of the annulus in kpc.

	All attributes and functionality are inherited from ``modified_exponential``
	and ``gaussian`` declared in ``src/simulations/models/utils.py``.
	"""

	def __init__(self, radius, dt = 0.01, dr = 0.1):
		modified_exponential.__init__(self,
			timescale = insideout.timescale(radius),
			rise = _TAU_RISE_)
		gaussian.__init__(self, mean = _BURST_TIME_, amplitude = 1.5)
		self._prefactor = 1
		self._prefactor = normalize(self, gradient, radius, dt = dt, dr = dr)

	def __call__(self, time):
		return self._prefactor * modified_exponential.__call__(self, time) * (
			1 + gaussian.__call__(self, time)
		)

