r""" 
This file declares the time-dependence of the star formation history at a 
given radius in the static disk model from Johnson et al. (2021). 
""" 

from .utils import constant 
from .normalize import normalize 
from .gradient import gradient 
import math as m 
import os 


class static(constant): 

	def __init__(self, radius, dt = 0.01, dr = 0.1): 
		super().__init__() 
		self.amplitude *= normalize(self, gradient, radius, dt = dt, dr = dr) 

