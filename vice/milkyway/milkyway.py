
from __future__ import absolute_import
__all__ = ["milkyway"]
from .._globals import _RECOGNIZED_ELEMENTS_
from ..core.multizone import multizone
from ..core.dataframe._builtin_dataframes import solar_z
from ..core import _pyutils
from ..toolkit.hydrodisk import hydrodiskstars
from ..toolkit.J21_sf_law import J21_sf_law
from .. import yields
from .utils import mass_from_surface_density
import numbers
import math as m

_MIN_RADIUS_ = 0 # The minimum radius of the radial bins in kpc
_MAX_RADIUS_ = 20 # The maximum radius of the radial bins in kpc
_MAX_SF_RADIUS_ = 15.5 # The maximum radius of star formation in kpc


class milkyway(multizone):

	r"""
	An object designed for running chemical evolution models of Milky Way-like
	spiral galaxies. Inherits from ``vice.multizone``.

	This object models the Milky Way as a series of concentric annuli of
	uniform width. A prescription for stellar migration based on the ``h277``
	hydrodynamical simulation (a part of the ``g14`` simulation suite,
	Christensen et al. 2012) [1]_, an observationally motivated star formation
	law, and a scaling of the outflow mass loading factor :math:`\eta` with
	radius tuned to predict an observationally motivated radial abundance
	gradient are included by default. For details, see discussion in
	Johnson et al. (2021) [2]_.

	**Signature**: vice.milkyway(zone_width = 0.5, name = "milkyway",
	n_stars = 1, simple = False, verbose = False, N = 1e5,
	migration_mode = "diffusion")

	.. versionadded:: 1.2.0

	.. seealso::

		- ``vice.multizone``
		- ``vice.toolkit.J21_sf_law``
		- ``vice.toolkit.hydrodisk.hydrodiskstars``
		- ``vice.singlezone``

	Parameters
	----------
	zone_width : ``float`` [default : 0.5]
		The radial width of each annulus in kpc.
	name : ``str`` [default : "milkyway"]
		The name of the simulation. Output will be stored in a directory under
		this name with a ".vice" extension.
	n_stars : ``int`` [default : 1]
		The number of stellar populations forming in each zone at each timestep.
	simple : ``bool`` [default : False]
		If True, VICE will run the model as a series of one-zone models. If
		False, information at intermediate timesteps will be taken into
		account.
	verbose : ``bool`` [default : False]
		Run the model with verbose output.
	N : ``int`` [default : 1e5]
		An estimate of the number of total stellar populations that will be
		simulated. This keyword will be passed to the ``hydrodiskstars``
		object implementing the stellar migration scheme.
	migration_mode : ``str`` [default : "diffusion"]
		A string denoting the time-dependence of stellar migration. This
		keyword will be passed to the ``hydrodiskstars`` object implementing
		the stellar migration scheme.

	Attributes
	----------
	annuli : ``list``
		The radii representing divisions between annuli in the disk model in
		kpc.
	zone_width : ``float`` [default : 0.5]
		The radial width of each annulus in kpc.
	evolution : ``<function>`` [default : milkyway.default_evolution]
		A function of galactocentric radius in kpc and time in Gyr,
		respectively. Returns either the surface density of gas in
		:math:`M_\odot`, the surface density of infall, or the surface density
		of star formation in :math:`M_\odot yr^{-1} kpc^{-2}`. The
		interpretation of the return value is set by the attribute ``mode``.

		.. note:: This is the **only** object in the current version of VICE
			which formulates an evolutionary parameter in terms of surface
			densities. This is done because many physical quantities are
			reported as surface densities in the astronomical literature. The
			``singlezone`` and ``multizone`` objects, however, formulate
			parameters in terms of mass, out of necessity for the
			implementation.

	mode : ``str`` [case-insensitive] [default : "ifr"]
		The interpretation of the attribute ``evolution``. Either "sfr" for
		star formation rate, "ifr" for infall rate, or "gas" for the ISM
		gas supply.
	elements : ``tuple`` [elements of type str] [default : ("fe", "sr", "o")]
		The elements to calculate abundances for in running the model.
	IMF : ``str`` or ``<function>`` [default : "kroupa"]
		The stellar initial mass function to assume. Strings denote built-in
		IMFs from the literature. Functions will be interpreted as a custom
		distribution of zero-age main sequence masses in :math:`M_\odot`.

		Built-in IMFs:

			- "kroupa": Kroupa (2001) [3]_
			- "salpeter": Salpeter (1955) [4]_

	mass_loading : ``<function>`` [default : milkyway.default_mass_loading]
		The mass loading factor as a function of galactocentric radius in kpc
		describing the efficiency of outflows.
	dt : ``float`` [default : 0.01]
		The timestep size in Gyr to use when running the model.
	bins : ``list`` [default : [-3.0, -2.95, -2.9, ... , 0.9, 0.95, 1.0]]
		The bins within which to sort the normalized stellar metallicity
		distribution function in each [X/H] and [X/Y] abundance ratio
		measurement.
	delay : real number [default : 0.15]
		The minimum delay time in Gyr before the onset of type Ia supernovae
		associated with a single stellar population.
	RIa : ``str`` [case-insensitive] or ``<function>`` [default : "plaw"]
		The SN Ia delay-time distribution (DTD) to adopt. Strings denote
		built-in DTDs and functions must accept time in Gyr as a parameter.
	smoothing : ``float`` [default : 0.0]
		The outflow smoothing timescale in Gyr. See discussion in Johnson &
		Weinberg (2020) [5]_.
	tau_ia : ``float`` [default : 1.5]
		The e-folding timescale of the SN Ia DTD. Only relevant when the
		attribute ``RIa == "exp"``.
	m_upper : ``float`` [default : 100]
		The upper mass limit on star formation in :math:`M_\odot`.
	m_lower : ``float`` [default : 0.08]
		The lower mass limit on star formation in :math:`M_\odot`.
	postMS : real number [default : 0.1]
		The lifetime ratio of the post main sequence to main sequence phases
		of stellar evolution.
	Z_solar : real number [default : 0.14]
		The adopted metallicity by mass of the sun.

	Other attributes are inherited from ``vice.multizone``.

	.. note:: The ``h277`` data is not included in VICE's distribution, but is
		available in its GitHub repository. When users first create a
		``milkyway`` object, it will download the data automatically and store
		it internally for future use. With a good internet connection, this
		process takes about 1 minute to complete, and need not be repeated.
		If the download fails, it's likely it has to do with not having
		administrator's privileges over your system. Users in this situation
		should speak with their administrator, who would then be able to
		download their data by running the following on their system:

		>>> import vice
		>>> vice.toolkit.hydrodisk.data.download()

	.. note:: This object, by default, will shut off star formation at
		:math:`R` > 15.5 kpc by setting the star formation efficiency timescale
		to a very large number. This can be overridden at any time by resetting
		the attribute ``tau_star`` of each zone.

	.. note:: See documentation of ``vice.multizone`` base class for
		information on the implementation and required computational overhead
		of this and other applications of VICE's multizone capabilities. In
		theory, the data involved can be arbitrarily large provided the system
		has the space, but coarse versions of finely sampled models often
		require only minutes to fully integrate, simplifying the debugging
		process.

	Functions
	---------
	run : [instancemethod]
		Run the simulation.
	default_evolution : [staticmethod]
		The default value of the functional attribute ``evolution``.
	default_mass_loading : [staticmethod]
		The default value of the functional attribute ``mass_loading``.

	Example Code
	------------
	>>> import vice
	>>> import numpy as np
	>>> mw = vice.milkyway(name = "example", zone_width = 1)
	>>> mw.n_zones
	20
	>>> mw.n_stars
	1
	>>> mw.name
	"example"
	>>> mw.run(np.linspace(0, 13.2, 1321), overwrite = True)

	.. [1] Christensen et al. (2012), MNRAS, 425, 3058
	.. [2] Johnson et al. (2021), arxiv:2103.09838
	.. [3] Kroupa (2001), MNRAS, 322, 231
	.. [4] Salpeter (1955), ApJ, 121, 161
	.. [5] Johnson & Weinberg (2020), MNRAS, 498, 1364
	"""

	def __new__(cls, zone_width = 0.5, **kwargs):
		radial_bins = _get_radial_bins(zone_width)
		return super().__new__(cls, n_zones = len(radial_bins) - 1)


	def __init__(self, zone_width = 0.5, name = "milkyway", n_stars = 1,
		simple = False, verbose = False, N = 1e5, migration_mode = "diffusion"):
		radial_bins = _get_radial_bins(zone_width)
		super().__init__(name = name, n_zones = len(radial_bins) - 1,
			n_stars = n_stars, simple = simple, verbose = verbose)
		
		# set default values
		self.migration.stars = hydrodiskstars(radial_bins, N = N,
			mode = migration_mode)
		self.evolution = milkyway.default_evolution
		self.mass_loading = milkyway.default_mass_loading
		for i in range(self.n_zones):
			# set the entrainment to zero beyond 15.5 kpc
			if (self.annuli[i] + self.annuli[i + 1]) / 2 > _MAX_SF_RADIUS_:
				self.zones[i].tau_star = 1.e6
				for j in _RECOGNIZED_ELEMENTS_:
					self.zones[i].entrainment.agb[j] = 0
					self.zones[i].entrainment.ccsne[j] = 0
					self.zones[i].entrainment.sneia[j] = 0
			else:
				self.zones[i].tau_star = J21_sf_law(
					m.pi * (self.annuli[i + 1]**2 - self.annuli[i]**2)
				)
			# in case running in infall mode, set initial gas mass to zero
			self.zones[i].Mg0 = 0


	def __repr__(self):
		r"""
		Prints in the format: vice.singlezone{
			attr1 -----------> value
			attribute2 ------> value
		}
		"""
		attrs = {
			"name": 			self.name,
			"n_zones": 			self.n_zones,
			"n_stars": 			self.n_stars,
			"verbose": 			self.verbose,
			"simple": 			self.simple,
			"annuli": 			self.annuli,
			"evolution": 		self.evolution,
			"mode": 			self.mode,
			"elements": 		self.elements,
			"IMF": 				self.IMF,
			"mass_loading": 	self.mass_loading,
			"dt": 				self.dt,
			"bins": 			self.bins,
			"delay": 			self.delay,
			"RIa": 				self.RIa,
			"smoothing": 		self.smoothing,
			"tau_ia": 			self.tau_ia,
			"m_upper": 			self.m_upper,
			"m_lower": 			self.m_lower,
			"postMS": 			self.postMS,
			"Z_solar": 			self.Z_solar
		}
		rep = "vice.milkyway{\n"
		for i in attrs.keys():
			rep += "    %s " % (i)
			for j in range(15 - len(i)):
				rep += '-'
			if isinstance(attrs[i], list) and len(attrs[i]) > 10:
				rep += "> [%g, %g, %g, ... , %g, %g, %g]\n" % (
					attrs[i][0], attrs[i][1], attrs[i][2],
					attrs[i][-3], attrs[i][-2], attrs[i][-1])
			else:
				rep += "> %s\n" % (str(attrs[i]))
		rep += '}'
		return rep


	@classmethod
	def from_output(cls, arg):
		r"""
		This function, inherited from the ``multizone`` object, is not
		supported for the ``milkyway`` model.
		"""
		raise TypeError("""This function is not supported for the milkyway \
object.""")


	@property
	def annuli(self):
		r"""
		Type : ``list`` [elements of type ``float``]

		The radii representing divisions between annuli in the disk model in
		kpc. This property is determined by the ``zone_width`` attribute, and
		cannot be modified after initialization of a ``milkyway`` object.

		.. seealso:: vice.milkyway.zone_width

		While this attribute stores the radii representing bounds between
		annuli, the ``singlezone`` object corresponding to each individual
		annulus is stored as an array in the ``zones`` attribute, inherited
		from the ``multizone`` class.

		By default, they will be named where "zone0" is the zero'th element of
		the ``zones`` attribute, corresponding to the innermost zone. The
		second innermost zone will be the first element of the ``zones``
		attribute, and by default will be named "zone1", and so on.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example", zone_width = 0.2)
		>>> mw.annuli
		[0.0,
		 0.2,
		 0.4,
		 ...,
		 19.6,
		 19.8,
		 20.0]
		"""
		return self.migration.stars.radial_bins

	@property
	def zone_width(self):
		r"""
		Type : ``float``

		Default : 0.5

		The width of each annulus in kpc. This value can only be set at
		initialization of the ``milkyway`` object.

		.. seealso:: vice.milkyway.annuli

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example", zone_width = 0.2)
		>>> mw.zone_width
		0.2
		"""
		return self.annuli[1] - self.annuli[0]

	@property
	def evolution(self):
		r"""
		Type : ``<function>``

		Default : vice.milkyway.default_evolution

		As a function of radius in kpc and time in Gyr, respectively, either
		the surface density of gas in :math:`M_\odot kpc^{-2}`, the surface
		density of star formation in :math:`M_\odot kpc^{-2} yr^{-1}`, or the
		surface density of infall in :math:`M_\odot kpc^{-2} yr^{-1}`. As in
		the ``singlezone`` object, the interpretation is set by the attribute
		``mode``.

		.. seealso:: vice.milkyway.default_evolution

		.. note:: This attribute will always be expected to accept radius in
			kpc and time in Gyr as parameters, in that order. However, surface
			densities of star formation and infall will always be interpreted
			as having units of :math:`M_\odot yr^{-1} kpc^{-2}` according to
			convention.

		.. note:: This is the **only** object in the current version of VICE
			which formulates an evolutionary parameter in terms of surface
			densities. This is done because many physical quantities are
			reported as surface densities in the astronomical literature. The
			``singlezone`` and ``multizone`` objects, however, formulate
			parameters in terms of mass, out of necessity for the
			implementation.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		"""
		return self._evolution

	@evolution.setter
	def evolution(self, value):
		# Error handling in the mass_from_surface_density and singlezone objects
		for i in range(self.n_zones):
			self.zones[i].func = mass_from_surface_density(
				value,
				(self.annuli[i] + self.annuli[i + 1]) / 2,
				m.pi * (self.annuli[i + 1]**2 - self.annuli[i]**2)
			)
		# If the code gets here, the surface density passes error handling
		self._evolution = value

	@staticmethod
	def default_evolution(radius, time):
		r"""
		The default evolutionary function of the ``milkyway`` object.

		**Signature**: vice.milkyway.default_evolution(radius, time)

		Parameters
		----------
		radius : float
			Galactocentric radius in kpc.
		time : float
			Simulation time in Gyr.

		Returns
		-------
		value : float
			Always returns the value of 1.0. The interpretation of this is set
			by the attribute ``mode``. With the default value of "ifr", this
			represents a uniform surface of infall of 1.0
			:math:`M_\odot yr^{-1} kpc^{-2}`.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.evolution
		<function vice.milkyway.milkyway.milkyway.default_evolution(radius, time)>
		>>> vice.milkyway.default_evolution(10, 1)
		1.0
		>>> vice.milkyway.default_evolution(5, 4)
		1.0
		"""
		return 1.0

	@property
	def mode(self):
		r"""
		Type : ``str`` [case-insensitive]

		Default : "ifr"

		The interpretation of the attribute ``evolution``.

		* 	mode = "ifr": The value returned from the attribute ``evolution``
			represents the surface density of gas infall into the interstellar
			medium in :math:`M_\odot kpc^{-2} yr^{-1}``.

		* 	mode = "sfr": The value returned from the attribute ``evolution``
			represents the surface density of star formation in
			:math:`M_\odot kpc^{-2} yr^{-1}`.

		* 	mode = "gas": The value returned from the attribute ``evolution``
			represents the surface density of the interstellar medium in
			:math:`M_\odot kpc^{-2}`.

		.. note:: The attribute ``evolution`` will always be expected to accept
			radius in kpc and time in Gyr as the first and second parameters,
			respectively. However, infall and star formation histories will be
			interpreted as having units of :math:`M_\odot yr^{-1}` according
			to convention.

		.. note:: Updating the value of this attribute also updates the
			corresponding attribute of the ``J21_sf_law`` star formation law
			where it has been assigned the attribute ``tau_star``.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.mode
		"ifr"
		>>> mw.mode = "sfr"
		>>> mw.mode
		"sfr"
		"""
		return self.zones[0].mode

	@mode.setter
	def mode(self, value):
		# Let the singlezone object do the error handling
		for i in range(len(self.zones)):
			self.zones[i].mode = value

			# The star formation law needs to know the mode changed too
			if isinstance(self.zones[i].tau_star, J21_sf_law):
				# it will be a string if the previous line passed
				self.zones[i].tau_star._mode = value.lower()
			else: pass

	@property
	def elements(self):
		r"""
		Type : ``tuple`` [elements of type str [case-insensitive]]

		Default : ("fe", "sr", "o")

		The symbols of the elements to track the enrichment for
		(case-insensitive). The more elements that are tracked, the longer the
		simulation will take, but the better calibrated is the total
		metallicity of the ISM in handling metallicity-dependent yields.

		.. tip::

			The order in which the elements appear in this tuple will dictate
			the abundance ratios that are quoted in the final stellar
			metallicity distribution function. That is, if element X appears
			before element Y, then VICE will determine the MDF in
			:math:`dN/d[Y/X]` as opposed to :math:`dN/d[X/Y]`. The elements
			that users intend to use as "reference elements" should come
			earliest in this list.

		.. note::

			All versions of VICE support the simulation of all 76
			astrophysically produced elements between carbon ("c") and
			bismuth ("bi"). Versions >= 1.1.0 also support helium ("he").

		.. note::

			Some of the heaviest elements that VICE recognizes have
			statistically significant enrichment from r-process
			nucleosynthesis [1]_. Simulations of these elements with realistic
			parameters and realistic nucleosynthetic yields will underpredict
			the absolute abundances of these elements. However, if these
			nuclei are assumed to be produced promptly following the formation
			of a single stellar population, the yield can be added to the
			yield from core collapse supernovae, which in theory can describe
			the total yield from all prompt sources [2]_.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.elements
		("fe", "sr", "o")
		>>> mw.elements = ["mg", "fe", "n", "c", "o"]
		>>> mw.elements
		("mg", "fe", "n", "c", "o")

		.. [1] Johnson (2019), Science, 363, 474
		.. [2] Johnson & Weinberg (2020), MNRAS, 498, 1364
		"""
		return self.zones[0].elements

	@elements.setter
	def elements(self, value):
		# Let the singlezone object do the error handling
		for i in range(self.n_zones):
			self.zones[i].elements = value

	@property
	def IMF(self):
		r"""
		Type : ``str`` [case-insensitive] or ``<function>``

		Default : "kroupa"

		.. versionadded:: 1.2.0
			In version >= 1.2.0, users may construct a function of mass to
			describe the IMF.

		The assumed stellar initial mass function (IMF). If assigned a string,
		VICE will adopt a built-in IMF. Functions must accept stellar mass as
		the only parameter and are expected to return the value of the IMF at
		that mass (it need not be normalized).

		Built-in IMFs:

			- "kroupa" [1]_
			- "salpeter" [2]_

		.. note::

			VICE has analytic solutions to the
			:ref:`cumulative return fraction <crf>` and the
			:ref:`main sequence mass fraction <msmf>` for built-in IMFs. If
			assigned a function, VICE will calculate these quantities
			numerically, increasing the required integration time.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.IMF = "salpeter"
		>>> def f(m):
			if m < 0.5:
				return m**-1.2
			else:
				return m**-2.2
		>>> mw.IMF = f

		.. [1] Kroupa (2001), MNRAS, 322, 231
		.. [2] Salpeter (1955), ApJ, 121, 161
		"""
		return self.zones[0].IMF

	@IMF.setter
	def IMF(self, value):
		# Let the singlezone object do the error handling
		for i in range(self.n_zones):
			self.zones[i].IMF = value

	@property
	def mass_loading(self):
		r"""
		Type : ``<function>``

		Default : vice.milkyway.default_mass_loading

		The mass-loading factor as a function of galactocentric radius in kpc
		describing the efficiency of outflows. For a given star formation rate
		:math:`\dot{M}_\star` and an outflow rate :math:`\dot{M}_\text{out}`,
		the mass-loading factor is defined as the unitless ratio:

		.. math:: \eta \equiv \dot{M}_\text{out} / \dot{M}_\star

		This function must return a non-negative real number for all radii
		defined in the disk model.

		.. note:: This formalism assumes a time-independent mass-loading
			factor at each radius. To implement a time-dependent alternative,
			users should modify the attribute ``eta`` of the ``singlezone``
			objects corresponding to each annulus in this model. See example
			below.

		.. seealso:: vice.singlezone.eta

		Example Code
		------------
		>>> import math as m
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> def f(r):
			return 0.5 * m.exp(r / 3)
		>>> mw.mass_loading = f
		>>> def g(t): # a time-dependent mass-loading factor
			return 3.0 * m.exp(-t / 3)
		>>> # assign each individual annulus a time-dependent value
		>>> for i in range(mw.n_zones):
		>>> 	mw.zones[i].eta = g
		"""
		return self._mass_loading

	@mass_loading.setter
	def mass_loading(self, value):
		if callable(value):
			# Let the singlezone object do error handling from here
			for i in range(self.n_zones):
				self.zones[i].eta = value(
					(self.annuli[i] + self.annuli[i + 1]) / 2
				)
			# If the code gets here, the function passes
			self._mass_loading = value
		else:
			raise TypeError("""Attribute 'mass_loading' must be a callable \
object. Got: %s""" % (type(value)))

	@staticmethod
	def default_mass_loading(rgal):
		r"""
		The default mass loading factor as a function of galactocentric
		radius in kpc.

		**Signature**: vice.milkyway.default_mass_loading(rgal)

		Parameters
		----------
		rgal : real number
			Galactocentric radius in kpc.

		Returns
		-------
		eta : real number
			The mass loading factor at that radius, defined by:

			.. math:: \eta(r) = (y_\text{O}^\text{CC}) / Z_\text{O}^\odot
				10^{0.08(r - 4\text{ kpc}) - 0.3} - 0.6

			where :math:`Z_\text{O}^\odot` is the solar abundance by mass of
			oxygen and :math:`y_\text{O}^\text{CC}` is the IMF-averaged CCSN
			yield of oxygen. While these values are customizable through
			``vice.solar_z`` and ``vice.yields.ccsne.settings``, this function
			assumes a value of :math:`Z_\text{O}^\odot` = 0.00572 (Asplund et
			al. 2009 [1]_) and :math:`y_\text{O}^\text{CC}` = 0.015 (Johnson &
			Weinberg 2020 [2]_, Johnson et al. 2021 [3]_).

		.. seealso:: vice.milkyway.mass_loading

		Example Code
		------------
		>>> import vice
		>>> vice.milkyway.default_mass_loading(0)
		0.029064576665950193
		>>> vice.milkyway.default_mass_loading(8)
		2.1459664721614495

		.. [1] Asplund et al. (2009), ARA&A, 47, 481
		.. [2] Johnson & Weinberg (2020), MNRAS, 498, 1364
		.. [3] Johnson et al. (2021), arxiv:2103.09838
		"""
		return 0.015 / 0.00572 * (10**(0.08 * (rgal - 4) - 0.3)) - 0.6

	@property
	def dt(self):
		r"""
		Type : ``float``

		Default: 0.01

		The timestep size in Gyr.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example", zone_width = 0.2)
		>>> mw.dt
		0.01
		>>> mw.dt = 0.02
		>>> mw.dt
		0.02
		"""
		return self.zones[0].dt

	@dt.setter
	def dt(self, value):
		# Let the singlezone object do the error handling
		for i in range(self.n_zones):
			self.zones[i].dt = value

	@property
	def bins(self):
		r"""
		Type : ``list`` [elements must be real numbers]

		Default: [-3, -2.95, -2.9, ... , 0.9, 0.95, 1.0]

		The bins in each [X/Y] abundance and [X/Y] abundance ratio to sort the
		normalized stellar metallicity distribution function into. By default,
		VICE sorts everything into 0.05-dex bins between [X/H] and [X/Y] =
		-3 and +1.

		.. note::

			The metallicity distributions reported by VICE are normalized to
			probability distribution functions (i.e. the integral over all
			bins is equal to 1).

		.. seealso:: vice.milkyway.elements

		Example Code
		------------
		>>> import numpy as np
		>>> import vice
		>>> mw = vice.milkyway(name = "example", zone_width = 0.2)
		>>> mw.bins = np.linspace(-3, 1, 401) # 400 bins between -3 and 1
		>>> mw.bins = np.linspace(-2, 2, 801) # 800 bins between -2 and +2
		"""
		return self.zones[0].bins

	@bins.setter
	def bins(self, value):
		# Let the singlezone object do the error handling
		for i in range(self.n_zones):
			self.zones[i].bins = value

	@property
	def delay(self):
		r"""
		Type : real number

		Default : 0.15

		The minimum delay time in Gyr before the onset of type Ia supernovae
		assocaited with a single stellar population. Default value is adopted
		from Weinberg, Andrews & Freudenburg (2017) [1]_.

		.. seealso:: vice.milkyway.RIa

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.delay
		0.15
		>>> mw.delay = 0.1
		>>> mw.delay
		0.1

		.. [1] Weinberg, Andrews & Freudenburg (2017), ApJ, 837, 183
		"""
		return self.zones[0].delay

	@delay.setter
	def delay(self, value):
		# Let the singlezone object do the error handling
		for i in range(self.n_zones):
			self.zones[i].delay = value

	@property
	def RIa(self):
		r"""
		Type : ``<function>`` or ``str`` [case-insensitive]

		Default: "plaw"

		The delay-time distribution (DTD) for type Ia supernovae to adopt. If
		type ``str``, VICE will use a built-in DTD:

		- "exp" : :math:`R_\text{Ia} \sim e^{-t}`
		- "plaw" : :math:`R_\text{Ia} \sim t^{-1.1}`

		When using the exponential DTD, the e-folding timescale is set by the
		attribute ``tau_ia``.

		Functions must accept time in Gyr as the only parameter and return the
		rate at that delay-time.

		.. tip::

			A custom DTD does not need to be normalized by the user. VICE will
			take care of this automatically.

		.. note::

			Saving functional attribute with VICE outputs requires the
			package dill_, an extension to ``pickle`` in the Python_ standard
			library. It is recommended that VICE users install dill_
			>= 0.2.0.

			.. _dill: https://pypi.org/project/dill/
			.. _Python: https://docs.python.org/library/

		Example Code
		------------
		>>> import math as m
		>>> import vice
		>>> mw = vice.milkway(name = "example")
		>>> mw.RIa = "exp"
		>>> mw.RIa
		"exp"
		>>> def f(t):
			if t < 0.2:
				return 1
			else:
				return m.exp(-(t - 0.2) / 1.4)
		>>> mw.RIa = f
		"""
		return self.zones[0].RIa

	@RIa.setter
	def RIa(self, value):
		# Let the singlezone object do the error handling
		for i in range(self.n_zones):
			self.zones[i].RIa = value

	@property
	def smoothing(self):
		r"""
		Type : real number

		Default : 0.0

		The outflow smoothing in Gyr (Johnson & Weinberg 2020 [1]_). This is
		the timescale on which the star formation rate is time-averaged
		before determining the outflow rate via the mass loading factor
		(attribute ``eta``). For an outflow rate :math:`\dot{M}_\text{out}`
		and a star formation rate :math:`\dot{M}_\star` with a smoothing time
		:math:`\tau_\text{s}`:

		.. math:: \dot{M}_\text{out} =
			\eta(t) \langle\dot{M}_\star\rangle_{\tau_\text{s}}

		The traditional relationship of
		:math:`\dot{M}_\text{out} = \eta\dot{M}_\star` is recovered when the
		user specifies a smoothing time that is smaller than the timestep
		size.

		.. note::

			While this parameter time-averages the star formation rate, it
			does NOT time-average the mass-loading factor.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.smoothing = 0.0
		>>> mw.smoothing = 0.5
		>>> mw.smoothing = 1.0

		.. [1] Johnson & Weinberg (2020), MNRAS, 498, 1364
		"""
		return self.zones[0].smoothing

	@smoothing.setter
	def smoothing(self, value):
		# Let the singlezone object do the error handling
		for i in range(self.n_zones):
			self.zones[i].smoothing = value

	@property
	def tau_ia(self):
		r"""
		Type : real number

		Default: 1.5

		The e-folding timescale in Gyr of an exponentially decaying delay-time
		distribution in type Ia supernovae. Default value is adopted from
		Weinberg, Andrews & Freudenburg (2017) [1]_.

		.. note::

			Because this is an e-folding timescale, it only matters when the
			attribute ``RIa`` == "exp".

		.. seealso:: vice.milkyway.RIa

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.tau_ia = 1.0
		>>> mw.tau_ia = 1.5
		>>> mw.tau_ia = 2.0

		.. [1] Weinberg, Andrews & Freudenburg (2017), ApJ, 837, 183
		"""
		return self.zones[0].tau_ia

	@tau_ia.setter
	def tau_ia(self, value):
		# Let the singlezone object do the error handling
		for i in range(self.n_zones):
			self.zones[i].tau_ia = value

	@property
	def m_upper(self):
		r"""
		Type : real number

		Default : 100

		The upper mass limit on star formation in :math:`M_\odot`.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.m_upper = 120
		"""
		return self.zones[0].m_upper

	@m_upper.setter
	def m_upper(self, value):
		# Let the singlezone object do the error handling
		for i in range(self.n_zones):
			self.zones[i].m_upper = value

	@property
	def m_lower(self):
		r"""
		Type : real number

		Default : 0.08

		The lower mass limit on star formation in :math:`M_\odot`.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.m_lower = 0.1
		"""
		return self.zones[0].m_lower

	@m_lower.setter
	def m_lower(self, value):
		# Let the singlezone object do the error handling
		for i in range(self.n_zones):
			self.zones[i].m_lower = value

	@property
	def postMS(self):
		r"""
		Type : real number

		Default : 0.1

		The ratio of a star's post main sequence lifetime to its main sequence
		lifetime.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.postMS = 0.12
		"""
		return self.zones[0].postMS

	@postMS.setter
	def postMS(self, value):
		# Let the singlezone object do the error handling
		for i in range(self.n_zones):
			self.zones[i].postMS = value

	@property
	def Z_solar(self):
		r"""
		Type : real number

		Default : 0.014

		The metallicity by mass of the sun :math:`M_Z/M_\odot`. This is used
		in calibrating the total metallicity of the interstellar medium (ISM),
		which is necessary when there are only a few elements tracked by the
		simulation with metallicity dependent yields. This scaling is
		implemented as follows:

		.. math:: Z_\text{ISM} = Z_\odot \left[\sum_i Z_i\right]
			\left[\sum_i Z_i^\odot\right]^{-1}

		where the summation is taken over all elements tracked by the
		simulation.

		.. note::

			The default value is the metallicity calculated by Asplund et al.
			(2009) [1]_; VICE by default adopts the Asplund et al. (2009)
			measurements on their element-by-element basis in calculating [X/H]
			and [X/Y] in simulations. Users who wish to adopt a different model
			for the composition of the sun should modify **both** this value
			**and** the element-by-element entires in ``vice.solar_z``.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.Z_solar = 0.014

		.. [1] Asplund et al. (2009), ARA&A, 47, 481
		"""
		return self.zones[0].Z_solar

	@Z_solar.setter
	def Z_solar(self, value):
		# Let the singlezone object do the error handling
		for i in range(self.n_zones):
			self.zones[i].Z_solar = value


def _get_radial_bins(zone_width):
	r"""
	Get the radial bins associated with a multizone model.

	Parameters
	----------
	zone_width : float
		The width of each zone in kpc.

	Returns
	-------
	radii : list
		The least-to-greatest sorted list of radii that serve as the divisions
		between annuli in the multizone disk model.

	Raises
	------
	* ValueError
		- zone_width is not positive
	* TypeError
		- zone_width is not a numerical value

	Notes
	-----
	If the zone_width is any larger than the difference between maximum and
	minimum radii (declared in this file), then the returned radii will be
	a list containing only those two values.
	"""
	if isinstance(zone_width, numbers.Number):
		if zone_width > _MAX_RADIUS_ - _MIN_RADIUS_:
			return [_MIN_RADIUS_, _MAX_RADIUS_]
		elif zone_width > 0:
			return _pyutils.range_(_MIN_RADIUS_, _MAX_RADIUS_, zone_width)
		else:
			raise ValueError("Zone width must be positive. Got: %g" % (
				zone_width))
	else:
		raise TypeError("Zone width must be a numerical value. Got: %s" % (
			type(zone_width)))

