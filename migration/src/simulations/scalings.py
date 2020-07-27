r""" 
Scaling relations of evolutionary parameters with galactocentric radius as 
adopted in the Johnson et al. (2021) study. 
""" 

import math as m 
import vice 


def tau_star(rgal, norm = 2, scale = 3): 
	r""" 
	Star formation efficiency timescale :math:`\tau_\star` as a function of 
	galactocentric radius. 

	Parameters 
	----------
	rgal : real number 
		Galactocentric radius in kpc 
	norm : real number [default : 2] 
		The value of :math:`\tau_\star` when rgal = 0 
	scale : real number [default : 3] 
		The scale radius in kpc 

	Returns 
	-------
	t : real number 
		:math:`\tau_\star` at the specified radius in Gyr. 

	Notes 
	-----
	The mathematical relation describing :math:`\tau_\star`: 

	.. math:: \tau_\star = A e^{-r/2r_\text{s}} 

	where :math:`r_\text{s}` is the scale radius, :math:`A` is the norm, and 
	:math:`r` is the galactocentric radius. 
	""" 
	return norm * m.exp(rgal / (2 * scale)) 


def eta(rgal, corrective = 0): 
	r""" 
	The mass loading factor :math:`\dot{M}_\text{out}/\dot{M}_\star` as a 
	function of galactocentric radius. 

	Parameters 
	----------
	rgal : real number 
		Galactocentric radius in kpc 
	corrective : real number [default : 0] 
		The additive corrective term 

	Returns 
	-------
	eta : real number 
		The mass loading factor at that radius. 

	Notes 
	-----
	The corrective term should be, roughly, :math:`\tau_\star/\tau_\text{sfh}` 
	where :math:`\tau_\star` is the SFE timescale and :math:`\tau_\text{sfh}` 
	is the star formation history e-folding timescale, both at that 
	galactocentric radius. 
	""" 
	return vice.yields.ccsne.settings['o'] / vice.solar_z['o'] * (
		10**(0.06 * (rgal - 4) - 0.3)) - 0.6 + corrective 

