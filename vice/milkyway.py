
from __future__ import absolute_import 
__all__ = ["milkyway"] 
from ._globals import _RECOGNIZED_ELEMENTS_ 
from .core.multizone import multizone 
from .core.dataframe._builtin_dataframes import solar_z 
from .core import _pyutils 
from .toolkit.hydrodisk import hydrodiskstars 
from . import yields 
import numbers 
import math as m 

_MIN_RADIUS_ = 0 # The minimum radius of the radial bins in kpc 
_MAX_RADIUS_ = 20 # The maximum radius of the radial bins in kpc 
_MAX_SF_RADIUS_ = 15.5 # The maximum radius of star formation in kpc 


class milkyway(multizone): 

	r""" 
	An object designed for running chemical evolution models of Milky Way-like 
	spiral galaxies. Inherits from vice.multizone. 

	**Signature**: vice.milkyway(radial_bins, name = "milkyway", n_stars = 1, 
	simple = False, verbose = False) 
	""" 

	def __new__(cls, zone_width = 0.5, **kwargs): 
		radial_bins = _get_radial_bins(zone_width) 
		return super().__new__(cls, n_zones = len(radial_bins) - 1) 

	def __init__(self, zone_width = 0.5, name = "milkyway", n_stars = 1, 
		simple = False, verbose = False, N = 1e5, migration_mode = "linear"): 
		radial_bins = _get_radial_bins(zone_width) 
		super().__init__(name = name, n_zones = len(radial_bins) - 1, 
			n_stars = n_stars, simple = simple, verbose = verbose) 
		
		# set default values 
		self.migration.stars = hydrodiskstars(radial_bins, N = N, 
			mode = migration_mode) 
		self.evolution = milkyway.default_evolution 
		self.mass_loading = milkyway.default_mass_loading 
		self.schmidt = True 
		for i in range(self.n_zones): 
			# set the entrainment to zero beyond 15.5 kpc 
			if (self.annuli[i] + self.annuli[i + 1]) / 2 > _MAX_SF_RADIUS_: 
				for j in _RECOGNIZED_ELEMENTS_: 
					self.zones[i].entrainment.agb[j] = 0 
					self.zones[i].entrainment.ccsne[j] = 0 
					self.zones[i].entrainment.sneia[j] = 0 
			else: pass 
			# in case running in infall mode, set initial gas mass to zero 
			self.zones[i].Mg0 = 0 

	@property 
	def annuli(self): 
		r""" 
		Type : list 

		The radii representing divisions between annuli in the disk model in 
		kpc. This property is determined by the ``zone_width`` attribute, and 
		can only be set at initialize of the ``milkyway`` object. 

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
		Type : float 

		Default : 0.5 

		The width of each annulus in kpc. This value can only be set at 
		initialization of the ``milkyway`` object. 

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
		Type : function 

		As a function of radius in kpc and time in Gyr, respectively, either 
		the surface density of gas in :math:`M_\odot kpc^{-2}`, the surface 
		density of star formation in :math:`M_\odot kpc^{-2} yr^{-1}`, or the 
		surface density of infall in :math:`M_\odot kpc^{-2} yr^{-1}`. 
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
			by the attribute ``mode``. 
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

		.. note:: 

			The attribute ``evolution`` will always be expected to accept 
			radius in kpc and time in Gyr as the first and second parameters, 
			respectively. However, infall and star formation histories will be 
			interpreted as having units of :math:`M_\odot yr^{-1}` according 
			to convention. 

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

	@property 
	def elements(self): 
		r""" 
		Type : tuple [elements of type str [case-insensitive]] 

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
			yield from core collapse supernovae [2]_. 

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
		.. [2] Johnson & Weinberg (2020), arxiv:1911.02598 
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

		.. versionadded:: 1.X.0 
			In version >= 1.X.0, users may construct a function of mass to 
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
		Type : <function> 

		Default : vice.milkyway.default_mass_loading 

		The mass-loading factor as a function of galactocentric radius in kpc 
		describing the efficiency of outflows. For a given star formation rate 
		:math:`\dot{M}_\star` and an outflow rate :math:`\dot{M}_\text{out}`, 
		the mass-loading factor is defined as the unitless ratio: 

		.. math:: \eta \equiv \dot{M}_\text{out} / \dot{M}_\star 

		This function must return a non-negative real number for all radii 
		defined in the disk model. 

		Example Code 
		------------
		>>> import math as m 
		>>> import vice 
		>>> mw = vice.milkyway(name = "example") 
		>>> def f(r): 
			return 0.5 * m.exp(r / 3) 
		>>> mw.mass_loading = f 
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

		Parameters 
		----------
		rgal : real number 
			Galactocentric radius in kpc. 

		Returns 
		-------
		eta : real number 
			The mass loading factor at that radius, defined by: 

			.. math:: \eta(r) = y_\text{O}^\text{CC} / Z_\text{O}^\odot 
				10^{0.08(r - 4\text{ kpc}) - 0.3} - 0.6 

			where :math:`C` is the corrective term, :math:`Z_\text{O}^\odot` 
			is the solar abundance by mass of oxygen, and 
			:math:`y_\text{O}^\text{CC}` is the IMF-averaged CCSN yield of 
			oxygen. These values are taken from the ``vice.yields`` module at 
			the time the ``milkyway`` object is initialized. 

		.. tip:: To reset the mass loading factor in each annulus after 
			modifying the oxygen yield, this function can be simply 
			reassigned. For a ``milkyway`` object ``x``: 

			>>> x.mass_loading = vice.milkyway.default_mass_loading  
		""" 
		# return yields.ccsne.settings['o'] / solar_z['o'] * (
		# 	10**(0.06 * (rgal - 4) - 0.3)) - 0.6 
		return 0.015 / solar_z['o'] * (10**(0.08 * (rgal - 4) - 0.3)) - 0.6 

	@property 
	def dt(self): 
		r""" 
		Type : float 

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
		Type : array-like [elements must be real numbers] 

		Default: [-3, -2.95, -2.9, ... , 0.9, 0.95, 1.0] 

		The bins in each [X/Y] abundance and [X/Y] abundance ratio to sort the 
		normalized stellar metallicity distribution function into. By default, 
		VICE sorts everything into 0.05-dex bins between [X/H] and [X/Y] = 
		-3 and +1. 

		.. note:: 

			The metallicity distributions reported by VICE are normalized to 
			probability distribution functions (i.e. the integral over all 
			bins is equal to 1). 

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
		Type : <function> or ``str`` [case-insensitive] 

		Default: "plaw" 

		The delay-time distribution (DTD) for type Ia supernovae to adopt. If 
		type ``str``, VICE will use a built-in DTD: 

		- "exp" : :math:`R_\text{Ia} \sim e^{-t}` 
		- "plaw" : :math:`R_\text{Ia} \sim t^{-1.1}` 

		When using the exponential DTD, the e-folding timescale is set by the 
		attribute ``tau_ia``. 

		Functions must accept time in Gyr as the only parameter. 

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
		distribution in type Ia supernovae. 

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
		""" 
		return self.zones[0].tau_ia 

	@tau_ia.setter 
	def tau_ia(self, value): 
		# Let the singlezone object do the error handling 
		for i in range(self.n_zones): 
			self.zones[i].tau_ia = value 

	@property 
	def tau_star_mol(self): 
		r""" 
		Type : real number or <function> 

		Default : 2.0 

		The adopted depletion time of molecular hydrogen due to star formation 
		in Gyr. If a real number, VICE will adopt the given value as a 
		constant. Functions must accept one numerical value as the only 
		parameter, which VICE will interpret as time in Gyr. The function is 
		expected to return the value of the molecular gas depletion time in 
		Gyr at that time in the simulation. 

		.. note:: 

			If the attribute ``schmidt`` is switched to ``False``, this 
			attribute no longer represents the depletion time of molecular 
			gas, instead describing the depletion time of the *total* gas 
			supply. 

		Example Code 
		------------
		>>> import vice 
		>>> mw = vice.milkyway(name = "example") 
		>>> mw.tau_star_mol = 1.5 
		>>> def f(t): 
			return 1.5 + 0.5 * (t / 10) 
		>>> mw.tau_star_mol = f 
		""" 
		return self.zones[0].tau_star 

	@tau_star_mol.setter 
	def tau_star_mol(self, value): 
		# Let the singlezone object do the error handling 
		for i in range(self.n_zones): 
			self.zones[i].tau_star = value 

	@property 
	def schmidt(self): 
		r"""
		Type : bool 

		Default : True 

		If True, the simulation will adopt a gas-dependent scaling of the 
		star formation efficiency timescale :math:`\tau_\star`. At each 
		timestep, :math:`\tau_\star` is determined via: 

		.. math:: \tau_\star(t) = \tau_{\star,\text{specified}}(t) 
			\left(
			\frac{\Sigma_g}{\Sigma_{g,\text{Schmidt}}} 
			\right)^{-\alpha} 

		where :math:`\tau_{\star,\text{specified}}(t)` is the user-specififed 
		value of the attribute ``tau_star``, :math:`\Sigma_g` is the 
		surface density of the interstellar medium, 
		:math:`\Sigma_{g,\text{Schmidt}}` is the normalization thereof 
		(attribute ``Sigma_gSchmidt``), and :math:`\alpha` is the power-law 
		index set by the attribute ``schmidt_index``. 

		This is an application of the Kennicutt-Schmidt star formation law 
		(Kennicutt 1998 [1]_; Schmidt 1959 [2]_, 1963 [3]_). 

		If False, this parameter does not impact the star formation efficiency 
		that the user has specified. 

		Example Code 
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example") 
		>>> mw.schmidt = True 
		>>> mw.schmidt = False 

		.. [1] Kennicutt (1998), ApJ, 498, 541 
		.. [2] Schmidt (1959), ApJ, 129, 243 
		.. [3] Schmidt (1963), ApJ, 137, 758 
		""" 
		return self.zones[0].schmidt 

	@schmidt.setter 
	def schmidt(self, value): 
		# Let the singlezone object do the error handling 
		for i in range(self.n_zones): 
			self.zones[i].schmidt = value 

	@property 
	def schmidt_index(self): 
		r""" 
		Type : real number 

		Default : 0.5 

		The power-law index on gas-dependent star formation efficiency, if 
		applicable: 

		.. math:: \tau_\star^{-1} \sim \Sigma_g^\alpha 

		.. note:: 

			This number should be 1 less than the power law index which 
			describes the scaling of star formation with the surface density 
			of gas. 

		Example Code 
		------------
		>>> import vice 
		>>> mw = vice.milkyway(name = "example") 
		>>> mw.schmidt_index = 0.5 
		>>> mw.schmidt_index = 0.4 
		>>> mw.schmidt_index 
		0.4 
		""" 
		return self.zones[0].schmidt_index 

	@schmidt_index.setter 
	def schmidt_index(self, value): 
		# Let the singlezone object do the error handling 
		for i in range(self.n_zones): 
			self.zones[i].schmidt_index = value 

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
			(2009) [1]_. VICE adopts the Asplund et al. (2009) measurements 
			on their element-by-element basis in calculating [X/H] and 
			[X/Y] in simulations; it is thus recommended that users adopt 
			these measurements as well so that the adopted solar composition 
			is self-consistent. This however has no qualitative impact on the 
			behavior of the simulation. 

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




class mass_from_surface_density: 

	r""" 
	An object which converts surface density in either :math:`M_\odot kpc^{-2}` 
	or :math:`M_\odot kpc^{-2} yr^{-1}` as a function of time in Gyr to either 
	:math:`M_\odot` or :math:`M_\odot yr^{-1}`. 

	.. note:: This object is for internal usage by the ``milkyway`` object 
		only. User access is discouraged. 

	**Signature**: mass_from_surface_density(surface_density, radius, area) 

	Parameters 
	----------
	surface_density : <function> 
		The attribute ``surface_density``. See below. 
	radius : float 
		The attribute ``radius``. See below. 
	area : float 
		The attribute ``area``. See below. 

	Attributes 
	----------
	surface_density : <function> 
		As a function of galactocentric radius in kpc and time in Gyr, 
		respectively, returns either the gas surface density in 
		:math:`M_\odot kpc^{-2}`, the surface density of infall in 
		:math:`M_\odot kpc^{-2} yr^{-1}`, or the surface density of star 
		formation in :math:`M_\odot kpc^{-2} yr^{-1}`. The interpretation is 
		set the attribute ``mode`` of the ``milkyway`` model. 
	radius : float 
		The exact radius in kpc that an annulus is assumed to represent. In 
		these models, this is the arithmetic mean of the edges of an annulus. 
		This is the radius that the attribute ``surface_density`` will be 
		evaluated at in simulation. 
	area : float 
		The area of an annulus in the disk model in :math:`kpc^2`. 
	""" 

	def __init__(self, surface_density, radius, area): 
		# Attributes not meant to be modifiable - set their values here 
		# surface density must be a callable function of time in Gyr 
		if callable(surface_density): 
			try: 
				x = surface_density(1, 0) 
			except: 
				raise TypeError("""Surface density as a function of radius \
and time must accept two numerical parameters.""") 
			if isinstance(x, numbers.Number): 
				self._surface_density = surface_density 
			else: 
				raise TypeError("""Surface density as a function of radius \
and time must return a numerical value.""") 
		else: 
			raise TypeError("Surface density must be a callable object.") 

		# radius must be a non-negative real number 
		if isinstance(radius, numbers.Number): 
			if radius >= 0: 
				self._radius = float(radius) 
			else: raise ValueError("Radius must be non-negative. Got: %g" % (
				radius)) 
		else: 
			raise TypeError("Radius must be a real number. Got: %s" % (
				type(radius))) 

		# area must be a positive real number 
		if isinstance(area, numbers.Number): 
			if area > 0: 
				self._area = float(area) 
			else: 
				raise ValueError("Area must be positive. Got: %g" % (area)) 
		else: 
			raise TypeError("Area must be a real number. Got: %s" % (
				type(area))) 

	def __call__(self, time): 
		return self.area * self.surface_density(self.radius, time) 

	@property 
	def surface_density(self): 
		r""" 
		Type : <function> 

		The callable function of time in Gyr representing surface density. 
		Depending on the user's model, this may be either surface density of 
		gas in :math:`M_\odot kpc^{-2}`, surface density of infall in 
		:math:`M_\odot kpc^{-2} yr^{-1}`, or surface of density of star 
		formation in :math:`M_\odot kpc^{-2} yr^{-1}`. The interpretation is 
		set by the attribute ``mode`` of the ``milkyway`` model. 

		For internal use by the ``milkyway`` object only. User access of this 
		object is discouraged. 
		""" 
		return self._surface_density 

	@property 
	def radius(self): 
		r""" 
		Type : float 

		The exact radius in kpc that an annulus is assumed to represent. In 
		these models, this is the arithmetic mean of the edges of an annulus. 
		This is the radius that the attribute ``surface_density`` will be 
		evaluated at in simulation. 

		For internal use by the ``milkyway`` object only. User access of this 
		object is discouraged. 
		""" 
		return self._radius 

	@property 
	def area(self): 
		r""" 
		Type : float 

		The area of an annulus in the milkyway model in :math:`kpc^2`. 

		For internal use by the ``milkyway`` object only. User access of this 
		object is discouraged. 
		""" 
		return self._area 


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

