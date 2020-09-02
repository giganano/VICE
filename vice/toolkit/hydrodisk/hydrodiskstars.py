
from __future__ import absolute_import 
from ._hydrodiskstars import c_hydrodiskstars 


class hydrodiskstars: 

	r""" 
	A stellar migration scheme inspired by a hydrodynamical zoom-in simulation 
	of a Milky Way-like disk galaxy ran at the University of Washington. 

	.. versionadded:: 1.X.0 

	.. note:: The galaxy in the zoom-in hydrodynamical simulation does not 
		have a bar, while the Milky Way is known to have a bar. Radial 
		migration is then driven by resonant interactions with spiral arms, 
		other star particles, etc. rather than dynamical interactions with the 
		bar. 

	.. note:: Simulations which adopt this model that run for longer than 
		12.8 Gyr are not supported. Stellar populations in the built-in 
		hydrodynamical simulation data span 12.8 Gyr of ages. 

	**Signature**: vice.toolkit.hydrodisk.hydrodiskstars(radial_bins, N = 1e5, 
	mode = "linear") 

	Parameters 
	----------
	radial_bins : array-like [elements must be positive real numbers] 
		The bins in galactocentric radius in kpc describing the disk model. 
		This must extend from 0 to at least 30 kpc. Need not be sorted in any 
		way. Will be stored as an attribute. 
	N : int [default : 1e5] 
		An approximate number of star particles from the hydrodynamical 
		simulation to include in the sample of candidate analogs. Their data 
		are not stored in a single file, but split across random subsamples to 
		decrease computational overhead when the full sample is not required. 
		In practice, this number should be slightly larger than the number of 
		(relevant) stellar populations simulated by a multizone model. 

		.. note:: There are 1,017,612 star particles available for this 
			object. Any more stellar populations than this would oversample 
			these data. 

	mode : str [case-insensitive] [default : "linear"] 
		The attribute 'mode', initialized via keyword argument. 

	Attributes 
	----------
	radial_bins : list 
		The bins in galactocentric radius in kpc describing the disk model. 
	analog_data : dataframe 
		The raw star particle data from the hydrodynamical simulation. 
	analog_index : int 
		The index of the star particle acting as the current analog. -1 if the 
		analog has not yet been set (see note below under `Calling`_) or if 
		no analog is found. 
	mode : str or ``None`` 
		The mode of stellar migration, describing the approximation of how 
		stars move from birth to final radii. Either "linear", "sudden", or 
		"diffusion". 

		.. note:: Only subclasses may set this attribute ``None``, in which 
			case it is assumed that a custom migration approximation is 
			employed by an overridden ``__call__`` function. If this attribute 
			is note set to ``None``, multizone simulations will *still* use 
			the approximation denoted by this property. 

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
		acting as the analog, and the data for the corresponding star particle 
		can then be accessed via the attribute ``analog_index``. 

	Raises 
	------
	* ValueError 
		- Minimum radius does not equal zero 
		- Maximum radius < 30 
	* ScienceWarning 
		- This object is called with a time larger than 12.8 Gyr 
		- The number of analog star particles requested is larger than the 
		  number available from the hydrodynamical simulation (1,017,612) 

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
	These constants are declared in vice/src/toolkit/hydrodiskstars.h in the 
	VICE source tree. 

	This object can be subclassed to implement a customized migration 
	approximation by overriding the ``__call__`` function. However, in this 
	case, users must also set the attribute ``mode`` to ``None``. If this 
	requirement is not satisfied, multizone simulations will **still** use the 
	approximation denoted by the ``mode`` attribute, **not** their overridden 
	``__call__`` function. 

	Example Code 
	------------
	>>> from vice.toolkit.hydrodisk import hydrodiskstars 
	>>> import numpy as np 
	>>> example = hydrodiskstars(np.linspace(0, 30, 121)) 
	>>> example.radial_bins 
	[0.0, 
	 0.25, 
	 0.5, 
	 ... 
	 29.5, 
	 29.75, 
	 30.0] 
	>>> example.analog_data.keys() 
	['id', 'tform', 'rform', 'rfinal', 'zfinal', 'vrad', 'vphi', 'vz'] 
	>>> example.analog_index 
	-1 
	>>> example(5, 7.2, 7.2) 
	5 
	>>> example.analog_index 
	200672 
	>>> example.analog_data["vrad"][example.analog_index] 
	5.6577 
	>>> example.mode 
	"linear" 
	""" 

	def __init__(self, rad_bins, N = 1e5, mode = "linear"): 
		self.__c_version = c_hydrodiskstars(rad_bins, N = N) 
		self.mode = mode 

	def __call__(self, zone, tform, time): 
		return self.__c_version.__call__(zone, tform, time) 

	def __enter__(self): 
		# Opens a with statement 
		return self 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		# Raises all exceptions inside a with statement 
		return exc_value is None 

	def __object_address(self): 
		r""" 
		Returns the memory address of the HYDRODISKSTARS object in C. For 
		internal usage only; usage of this function by the user is strongly 
		discouraged. 
		""" 
		return self.__c_version.object_address() 

	@property 
	def radial_bins(self): 
		r""" 
		Type : list [elements are positive real numbers] 

		The bins in galactocentric radius in kpc describing the disk model. 
		Must extend from 0 to at least 30 kpc. Need not be sorted in any way 
		when assigned. 

		Example Code 
		------------
		>>> from vice.toolkit.hydrodisk import hydrodiskstars 
		>>> import numpy as np 
		>>> example = hydrodiskstars([0, 5, 10, 15, 20, 25, 30]) 
		>>> example.radial_bins 
		[0, 5, 10, 15, 20, 25, 30] 
		>>> example.radial_bins = list(range(31)) 
		>>> example.radial_bins 
		[0, 
		 1, 
		 2, 
		 ... 
		 27, 
		 28, 
		 29, 
		 30] 
		""" 
		return self.__c_version.radial_bins 

	@radial_bins.setter 
	def radial_bins(self, value): 
		self.__c_version.radial_bins = value 

	@property 
	def analog_data(self): 
		r""" 
		Type : dataframe 

		The star particle data from the hydrodynamical simulation. The 
		following keys map to the following data: 

			- id:      	The IDs of each star particle 
			- tform:   	The time the star particle formed in Gyr 
			- rform:   	The radius the star particle formed at in kpc 
			- rfinal:  	The radius the star particle ended up at in kpc 
			- zfinal:  	The height above the disk midplane in kpc at the end 
						of the simulation 
			- vrad:     The radial velocity of the star particle at the end of 
						the simulation in km/sec 
			- vphi:     The azimuthal velocity of the star particle at the end 
						of the simulation in km/sec 
			- vz: 		The velocity perpendicular to the disk midplane at the 
						end of the simulation in km/sec 

		Example Code 
		------------
		>>> from vice.toolkit.hydrodisk import hydrodiskstars 
		>>> import numpy as np 
		>>> example = hydrodiskstars(np.linspace(0, 30, 121)) 
		>>> example.analog_data.keys() 
		['id', 'tform', 'rform', 'rfinal', 'zfinal', 'vrad', 'vphi', 'vz'] 
		>>> example.analog_data["rfinal"][:10] 
		[2.0804,
		 14.9953,
		 2.2718,
		 15.1236,
		 2.3763,
		 0.9242,
		 9.0908,
		 0.1749,
		 8.415,
		 20.1452] 
		""" 
		return self.__c_version.analog_data 

	@property 
	def analog_index(self): 
		r""" 
		Type : int 

		The index of the analog in the hydrodynamical simulation star particle 
		data. -1 if no analog is found for a star particle born at a given 
		radius and time. 

		.. note:: Calling this object at a given zone with the formation time 
			and the simulation time equal resets the star particle acting as 
			the analog. 

		Example Code 
		------------
		>>> from vice.toolkit.hydrodisk import hydrodiskstars 
		>>> import numpy as np 
		>>> example = hydrodiskstars(np.linspace(0, 30, 121)) 
		>>> example.analog_index 
		-1 # no analog yet 
		>>> example(2, 1, 1) # final two arguments equal resets analog 
		15745 
		>>> example(10, 4, 4) 
		10 
		>>> example.analog_index 
		101206 
		>>> example.analog_data["rfinal"][example.analog_index] 
		2.6411 
		>>> example.analog_data["vrad"][example.analog_data] 
		92.2085 
		""" 
		return self.__c_version.analog_index 

	@property 
	def mode(self): 
		r""" 
		Type : str [case-insensitive] or ``None`` 

		Default : "linear" 

		Recognized Values 
		-----------------
		The following is a breakdown of how stellar populations migrate in 
		multizone simulations under each approximation. 

		- "linear" 
			Orbital radii at times between birth and 12.8 Gyr are assigned via 
			linear interpolation. Stellar populations therefore spiral 
			uniformly inward or outward from birth to final radii. 
		- "sudden" 
			The time of migration is randomly drawn from a uniform distribution 
			between when a stellar population is born and 12.8 Gyr. At times 
			prior to this, it is at its radius of birth; at subsequent times, 
			it is at its final radius. Stellar populations therefore spend no 
			time at intermediate radii. 
		- "diffusion" 
			The orbital radius at times between birth and 12.8 Gyr are assigned 
			via a sqrt(time) dependence, approximating a random-walk motion. 
			Stellar populations spiral inward or outward, but slightly faster 
			than the linear approximation when they are young. 
		- ``None`` 
			Only supported for subclasses of the hydrodiskstars object, this 
			should be used when the user intends to override the built-in 
			migration assumptions and implement a different one. In these 
			cases, the ``__call__`` method should be overridden in addition to 
			this attribute being set to ``None``. If the ``

		Example Code 
		------------
		>>> from vice.toolkit.hydrodisk import hydrodiskstars 
		>>> import numpy as np 
		>>> example = hydrodiskstars(np.linspace(0, 30, 121)) 
		>>> example.mode 
		'linear' 
		>>> example.mode = "sudden" 
		>>> example.mode = "diffusion" 
		""" 
		return self.__c_version.mode 

	@mode.setter 
	def mode(self, value): 
		if value is None: 
			if type(self) != hydrodiskstars: 
				self.__c_version.mode = None 
			else: 
				raise ValueError("""None-Type value for attribute 'mode' only \
supported for subclasses of hydrodiskstars object.""") 
		else: 
			self.__c_version.mode = value 

