r""" 
This file implements the W18 explodability engine as a function of stellar 
mass in Msun. 
""" 

from __future__ import absolute_import 
from ....._globals import _DIRECTORY_ 
from ._engine import engine 


class W18(engine): 

	r""" 
	W18 explosion engine from Sukhbold et al. (2016), ApJ, 821, 38 

	Attributes 
	----------
	masses : list 
		The stellar masses in :math:`M_\odot` on which the explosion engine 
		is sampled. 
	frequencies : list 
		The frequencies with which stars whose masses are given by the 
		attribute 'masses' explode as a core collapse supernova. 

	This object can be called or indexed with any stellar mass in 
	:math:`M_\odot`, and it will interpolate between grid elements to 
	estimate the frequency with which a star of that mass will explode as a 
	core collapse supernova (the grid itself being stored by the attributes 
	'masses' and 'frequencies'). 
	""" 

	def __init__(self): 
		super().__init__("%syields/ccsne/S16/engines/W18.dat" % (_DIRECTORY_)) 

	def __call__(self, mass): 
		# This is necessary for inspect.signature to find the call sign. 
		return super().__call__(mass) 
		
