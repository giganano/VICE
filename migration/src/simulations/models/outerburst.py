r""" 
This file declares the time-dependence of the star formation history at a 
given radius in the outerburst model from Johnson et al. (2021). 
""" 

from .utils import modified_exponential 
from .lateburst import _BURST_TIME_, lateburst 
from .insideout import _TAU_RISE_, insideout 
from .normalize import normalize 
from .gradient import gradient 
import math as m 
import os 

_RADIUS_ = 6 # radius in kpc beyond which there is a late starburst 


class outerburst(lateburst): 

	def __init__(self, radius, dt = 0.01, dr = 0.1): 
		self._burst = radius > _RADIUS_ # whether or not there will be a burst 
		super().__init__(radius, dt = dt, dr = dr) 

	def __call__(self, time): 
		if self._burst: 
			return super().__call__(time) 
		else: 
			return self._prefactor * modified_exponential.__call__(self, time) 

