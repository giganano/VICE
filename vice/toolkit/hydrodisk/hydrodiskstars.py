
from __future__ import absolute_import
from ._hydrodiskstars import c_hydrodiskstars
from . import data


class hydrodiskstars:

	r"""
	A stellar migration scheme informed by the ``h277`` simulation, a zoom-in
	hydrodynamic simulation of a Milky Way like galaxy ran from cosmological
	initial conditions (a part of the ``g14`` simulation suite, Christensen et
	al 2012 [1]_).

	**Signature**: vice.toolkit.hydrodisk.hydrodiskstars(radial_bins, N = 1e5,
	mode = "diffusion")

	.. versionadded:: 1.2.0

	.. warning:: Simulations which adopt this model that run for longer than
		13.2 Gyr are not supported. Stellar populations in the built-in
		hydrodynamical simulation data span 13.2 Gyr of ages; simulations on
		longer timescales are highly likely to produce a
		``segmentation fault``.

	Parameters
	----------
	radial_bins : array-like [elements must be positive real numbers]
		The bins in galactocentric radius in kpc describing the disk model.
		This must extend from 0 to at least 20. Need not be sorted in any
		way. Will be stored as an attribute.
	N : int [default : 1e5]
		An approximate number of star particles from the hydrodynamical
		simulation to include in the sample of candidate analogs. Their data
		are not stored in a single file, but split across random subsamples to
		decrease computational overhead when the full sample is not required.
		In practice, this number should be slightly larger than the number of
		(relevant) stellar populations simulated by a multizone model.

		.. note:: There are 3,102,519 star particles available for this
			object. Any more stellar populations than this would oversample
			these data.

	mode : str [case-insensitive] or ``None`` [default : "diffusion"]
		The attribute 'mode', initialized via keyword argument.

	Attributes
	----------
	radial_bins : list
		The bins in galactocentric radius in kpc describing the disk model.
	analog_data : dataframe
		The raw star particle data from the hydrodynamical simulation.
	analog_index : int
		The index of the star particle acting as the current analog. -1 if the
		analog has not yet been set (see note below under `Calling`_).
	mode : str or ``None``
		The mode of stellar migration, describing the approximation of how
		stars move from birth to final radii. Either "diffusion", "sudden", or
		"linear". See property docstring for more details.

		.. note:: Only subclasses may set this attribute ``None``, in which
			case it is assumed that a custom migration approximation is
			employed by an overridden ``__call__`` function. In this case,
			if this attribute is not set to ``None``, multizone simulations
			will *still* use the approximation denoted by this property.

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

	Functions
	---------
	decomp_filter : [instancemethod]
		Filter the star particles based on their kinematic decomposition.

	Raises
	------
	* ValueError
		- Minimum radius does not equal zero
		- Maximum radius < 20
	* ScienceWarning
		- This object is called with a time larger than 13.2 Gyr
		- The number of analog star particles requested is larger than the
		  number available from the hydrodynamical simulation (3,102,519)

	Notes
	-----
	This object requires VICE's supplementary data sample, available in its
	GitHub repository at ./vice/toolkit/hydrodisk/data.  The first time a
	``hydrodiskstars`` object is constructed, VICE will download
	the additional data automatically. If this process fails, it may be due to
	not having administrator's privileges on your system; in this event, users
	should speak with their administrator, who would then be able to download
	their data by running the following on their system:

	>>> import vice
	>>> vice.toolkit.hydrodisk.data.download()

	This migration scheme works by assigning each stellar population in the
	simulation an analog star particle from the hydrodynamical simulation. The
	analog is randomly drawn from a sample of star particles which formed at
	a similar radius and time, and the stellar population then assumes the
	change in orbital radius of its analog.

	VICE first searches for analogs in the ``h277`` data for star particles
	which formed at a radius of :math:`R \pm` 250 pc and at a time of
	:math:`T \pm` 250 Myr. If no analogs are found that satisfy this
	requirement, the search is widened to :math:`R \pm` 500 pc and
	:math:`T \pm` 500 Myr. If still no analog is found, then the time
	restriction of :math:`T \pm` 500 Myr is maintained, and VICE finds the star
	particle with the smallest difference in birth radius, assigning it as the
	analog. These values parameterizing this search algorithm are declared in
	``vice/src/toolkit/hydrodiskstars.h`` in the VICE source tree. For further
	details, see "Milky Way-Like Galaxies" under VICE's science documentation.

	This object can be subclassed to implement a customized migration
	approximation by overriding the ``__call__`` function. However, in this
	case, users must also set the attribute ``mode`` to ``None``. If this
	requirement is not satisfied, multizone simulations will **still** use the
	approximation denoted by the ``mode`` attribute, **not** their overridden
	``__call__`` function.

	The ``h277`` galaxy had a weak and transient bar, but does not have one at
	the present day. This is one notable difference between it and the Milky
	Way.

	Example Code
	------------
	>>> from vice.toolkit.hydrodisk import hydrodiskstars
	>>> import numpy as np
	>>> example = hydrodiskstars(np.linspace(0, 20, 81), N = 5e5)
	>>> example.radial_bins
	[0.0,
	 0.25,
	 0.5,
	 ...
	 19.5,
	 19.75,
	 20.0]
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
	"diffusion"

	.. [1] Christensen et al. (2012), MNRAS, 425, 3058
	"""

	def __init__(self, rad_bins, N = 1e5, mode = "diffusion"):
		if not data._h277_exists():
			print("VICE supplementary data required, downloading now.")
			print("You will not need to repeat this process.")
			data.download()
		else: pass
		self.__c_version = c_hydrodiskstars(rad_bins, N = N, mode = mode)

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
		Must extend from 0 to at least 20 kpc. Need not be sorted in any way
		when assigned.

		Example Code
		------------
		>>> from vice.toolkit.hydrodisk import hydrodiskstars
		>>> import numpy as np
		>>> example = hydrodiskstars([0, 5, 10, 15, 20])
		>>> example.radial_bins
		[0, 5, 10, 15, 20]
		>>> example.radial_bins = list(range(31))
		>>> example.radial_bins
		[0,
		 1,
		 2,
		 ...
		 17,
		 18,
		 19,
		 20]
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
			- zform: 	The disk midplane distance in kpc at the time of
			  formation.
			- zfinal:  	The disk midplane distance in kpc at the end of the
			  simulation
			- vrad:     The radial velocity of the star particle at the end of
			  the simulation in km/sec
			- vphi:     The azimuthal velocity of the star particle at the end
			  of the simulation in km/sec
			- vz: 		The velocity perpendicular to the disk midplane at the
			  end of the simulation in km/sec
			- decomp: 	An integer denoting which kinematic subclass the star
			  particle belongs to (1: thin disk, 2: thick disk, 3: bulge,
			  4: pseudobulge, 5: halo).

		Example Code
		------------
		>>> from vice.toolkit.hydrodisk import hydrodiskstars
		>>> import numpy as np
		>>> example = hydrodiskstars(np.linspace(0, 20, 81))
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
		data. -1 if it has not yet been assigned.

		.. note:: Calling this object at a given zone with the formation time
			and the simulation time equal resets the star particle acting as
			the analog.

		Example Code
		------------
		>>> from vice.toolkit.hydrodisk import hydrodiskstars
		>>> import numpy as np
		>>> example = hydrodiskstars(np.linspace(0, 20, 81))
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

		Default : "diffusion"

		Recognized Values
		-----------------
		The following is a breakdown of how stellar populations migrate in
		multizone simulations under each approximation.

		- "diffusion"
			The orbital radius at times between birth and 13.2 Gyr are assigned
			via a sqrt(time) dependence, the mean displacement if stars
			migrated according to a random walk. Stellar populations spiral
			inward or outward with a smooth time dependence in this model.
		- "linear"
			Orbital radii at times between birth and 13.2 Gyr are assigned via
			linear interpolation. Stellar populations therefore spiral
			uniformly inward or outward from birth to final radii, with orbital
			radius changing more slowly for young stars than in the diffusion
			model, but more quickly for old stars.
		- "sudden"
			The time of migration is randomly drawn from a uniform distribution
			between when a stellar population is born and 13.2 Gyr. At times
			prior to this, it is at its radius of birth; at subsequent times,
			it is at its final radius. Stellar populations therefore spend no
			time at intermediate radii.
		- ``None``
			Only supported for subclasses of the hydrodiskstars object, this
			should be used when the user intends to override the built-in
			migration assumptions and implement a different one. In these
			cases, the ``__call__`` method should be overridden in addition to
			this attribute being set to ``None``.

		.. note:: The "post-processing" model from Johnson et al. (2021) [1]_
			corresponds to setting the attribute ``simple = True`` in the
			``milkyway`` object, inherited from the base class ``multizone``.

		Example Code
		------------
		>>> from vice.toolkit.hydrodisk import hydrodiskstars
		>>> import numpy as np
		>>> example = hydrodiskstars(np.linspace(0, 20, 81))
		>>> example.mode
		'diffusion'
		>>> example.mode = "sudden"
		>>> example.mode = "linear"

		.. [1] Johnson et al. (2021), 2103.09838
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


	def decomp_filter(self, values):
		r"""
		Filter the star particles from the hydrodynamic simulation based on
		the kinematic decomposition.

		Parameters
		----------
		values : ``list`` [elements of type ``int``]
			The integer values of the "decomp" column in the ``analog_data``
			attribute to base the filter on. Those with a decomposition tag
			equal to one of the values in this list will pass the filter and
			remain in the sample.

			.. note:: The integer values mean that an individual star particle
				has kinematics associated with the following sub-populations:
				
					- 1: thin disk
					- 2: thick disk
					- 3: bulge
					- 4: pseudobulge
					- 5: halo

		Example Code
		------------
		>>> from vice.toolkit.hydrodisk import hydrodiskstars
		>>> import numpy as np
		>>> example = hydrodiskstars(np.linspace(0, 20, 81))
		>>> len(example.analog_data['id'])
		102857
		>>> example.decomp_filter([1, 2]) # disk stars only
		>>> len(example.analog_data['id'])
		57915
		>>> all([i in [1, 2] for i in example.analog_data['decomp']])
		True
		>>> example = hydrodiskstars(np.linspace(0, 20, 81))
		>>> len(example.analog_data['id'])
		102857
		>>> example.decomp_filter([3, 4]) # bulge stars only
		>>> len(example.analog_data['id'])
		44942
		>>> all([i in [3, 4] for i in example.analog_data['decomp']])
		True
		"""
		self.__c_version.decomp_filter(values)

