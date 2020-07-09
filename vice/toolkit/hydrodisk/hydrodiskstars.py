
from __future__ import absolute_import 
from ._hydrodiskstars import c_linear, c_sudden, c_diffusion 

""" 
Subclass each of the C-implementation objects, overwriting the init call 
signature, and letting them inherit everything else, including docstrings. For 
documetation, see implementation in _hydrodiskstars.pyx in this directory. 
""" 

class linear(c_linear): 

	def __init__(self, rad_bins): 
		super().__init__(rad_bins) 


class sudden(c_sudden): 

	def __init__(self, rad_bins): 
		super().__init__(rad_bins) 


class diffusion(c_diffusion): 

	def __init__(self, rad_bins): 
		super().__init__(rad_bins) 

