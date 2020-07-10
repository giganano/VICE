
from __future__ import absolute_import 
from ._hydrodiskstars import c_linear, c_sudden, c_diffusion 

""" 
Subclass each of the C-implementation objects, overwriting the init call 
signature, and letting them inherit everything else. 
""" 

class linear(c_linear): 

	r""" 
	A stellar migration scheme inspired by a hydrodynamical zoom-in simulation 
	of a Milky Way-like disk galaxy ran at the University of Washington. This 
	setting moves stellar populations from their initial to final radii 
	linearly with time. 

	Parameters 
	----------
	rad_bins : array-like [elements must be positive real numbers] 
		The bins in galactocentric radius in kpc describing the disk model. 
		This must extend from 0 to at least 30 kpc, or else the multizone 
		simulation will raise an error. 

	Calling 
	-------
	As all stellar migration prescriptions must, this object can be called 
	with three parameters, in the following order: 

		zone : int 
			The zone index of formation of the stellar population. Must be 
			non-negative. 
		tform : float 
			The time of formation of the stellar population in Gyr. 
		time : float 
			The simulation time in Gyr (i.e. not the age of the star particle). 

	.. note:: The search for analog star particles is ran when the formation 
		time and simulation time are equal. Therefore, calling this object 
		with the second and third parameters equal resets the star particle 
		acting as the analog. 

	Notes 
	-----
	This migration scheme works by assigning each stellar population in the 
	simulation an analog star particle from the hydrodynamical simulation. The 
	analog is randomly drawn from a sample of star particles which formed at 
	a similar radius and time, and the stellar population then assumes the 
	final orbital radius of its analog. Stellar populations that do not find 
	an analog stay at their radius of birth. In modeling a Milky Way-like disk, 
	the vast majority of stellar populations will find an analog. 

	If no analogs which formed within 300 pc of the stellar population in 
	radius and 250 Myr in formation time, then the search is widened to star 
	particles forming within 600 pc in radius and 500 Myr in formation time. 
	These constants are declared in vice/src/toolkit/hydrodiskstars.h. 
	""" 

	def __init__(self, rad_bins): 
		super().__init__(rad_bins) 

	# Signtaure not supported by cdef classes, hence seemingly redundant code 
	def __call__(self, zone, tform, time): 
		return super().__call__(zone, tform, time) 


class sudden(c_sudden): 

	r""" 
	A stellar migration scheme inspired by a hydrodynamical zoom-in simulation 
	of a Milky Way-like disk galaxy ran at the University of Washington. This 
	setting moves stellar populations from their initial to final radii 
	at a time randomly drawn between their birth time and the end of the 
	simulation. 

	Parameters 
	----------
	rad_bins : array-like [elements must be positive real numbers] 
		The bins in galactocentric radius in kpc describing the disk model. 
		This must extend from 0 to at least 30 kpc, or else the multizone 
		simulation will raise an error. 

	Calling 
	-------
	As all stellar migration prescriptions must, this object can be called 
	with three parameters, in the following order: 

		zone : int 
			The zone index of formation of the stellar population. Must be 
			non-negative. 
		tform : float 
			The time of formation of the stellar population in Gyr. 
		time : float 
			The simulation time in Gyr (i.e. not the age of the star particle). 

	.. note:: The search for analog star particles is ran when the formation 
		time and simulation time are equal. Therefore, calling this object 
		with the second and third parameters equal resets the star particle 
		acting as the analog. 

	Notes 
	-----
	This migration scheme works by assigning each stellar population in the 
	simulation an analog star particle from the hydrodynamical simulation. The 
	analog is randomly drawn from a sample of star particles which formed at 
	a similar radius and time, and the stellar population then assumes the 
	final orbital radius of its analog. Stellar populations that do not find 
	an analog stay at their radius of birth. In modeling a Milky Way-like disk, 
	the vast majority of stellar populations will find an analog. 

	If no analogs which formed within 300 pc of the stellar population in 
	radius and 250 Myr in formation time, then the search is widened to star 
	particles forming within 600 pc in radius and 500 Myr in formation time. 
	These constants are declared in vice/src/toolkit/hydrodiskstars.h. 
	""" 

	def __init__(self, rad_bins): 
		super().__init__(rad_bins) 

	# Signtaure not supported by cdef classes, hence seemingly redundant code 
	def __call__(self, zone, tform, time): 
		return super().__call__(zone, tform, time) 


class diffusion(c_diffusion): 

	r""" 
	A stellar migration scheme inspired by a hydrodynamical zoom-in simulation 
	of a Milky Way-like disk galaxy ran at the University of Washington. This 
	setting moves stellar populations from their initial to final radii 
	with a sqrt(time) dependence, approximating a random-walk motion. 	

	Parameters 
	----------
	rad_bins : array-like [elements must be positive real numbers] 
		The bins in galactocentric radius in kpc describing the disk model. 
		This must extend from 0 to at least 30 kpc, or else the multizone 
		simulation will raise an error. 

	Calling 
	-------
	As all stellar migration prescriptions must, this object can be called 
	with three parameters, in the following order: 

		zone : int 
			The zone index of formation of the stellar population. Must be 
			non-negative. 
		tform : float 
			The time of formation of the stellar population in Gyr. 
		time : float 
			The simulation time in Gyr (i.e. not the age of the star particle). 

	.. note:: The search for analog star particles is ran when the formation 
		time and simulation time are equal. Therefore, calling this object 
		with the second and third parameters equal resets the star particle 
		acting as the analog. 

	Notes 
	-----
	This migration scheme works by assigning each stellar population in the 
	simulation an analog star particle from the hydrodynamical simulation. The 
	analog is randomly drawn from a sample of star particles which formed at 
	a similar radius and time, and the stellar population then assumes the 
	final orbital radius of its analog. Stellar populations that do not find 
	an analog stay at their radius of birth. In modeling a Milky Way-like disk, 
	the vast majority of stellar populations will find an analog. 

	If no analogs which formed within 300 pc of the stellar population in 
	radius and 250 Myr in formation time, then the search is widened to star 
	particles forming within 600 pc in radius and 500 Myr in formation time. 
	These constants are declared in vice/src/toolkit/hydrodiskstars.h. 
	""" 

	def __init__(self, rad_bins): 
		super().__init__(rad_bins) 

	# Signtaure not supported by cdef classes, hence seemingly redundant code 
	def __call__(self, zone, tform, time): 
		return super().__call__(zone, tform, time) 

