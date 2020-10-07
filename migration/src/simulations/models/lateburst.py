r""" 
This file declares the time-dependence of the star formation history at a 
given radius in the lateburst model from Johnson et al. (2021). 
""" 

from .utils import modified_exponential, gaussian 
from .insideout import _TAU_RISE_, insideout
from .normalize import normalize 
from .gradient import gradient 
import math as m 
import os 

_BURST_TIME_ = 10.8 # Gyr 


class lateburst(modified_exponential, gaussian): 

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

