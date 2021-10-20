r"""
milkyway star formation efficiency
==================================
This file implements the default star formation law employed by the ``milkyway``
object. This model was adopted by Johnson et al. (2021) [1]_, the paper which
released these features.

.. [1] Johnson et al. (2021), arxiv:2103.09838
"""

from __future__ import absolute_import
import numbers


class J21_sf_law:

	r"""
	The default star formation law of the ``milkyway`` object. This is a
	callable object, accepting simulation time and either star formation rate
	or gas supply as second arguments. By default, it implements the star
	formation law adopted in Johnson et al. (2021) [1]_.

	**Signature**: vice.toolkit.J21_sf_law(area, \*\*kwargs)

	.. versionadded:: 1.2.0

	.. warning:: In a ``milkyway`` object, every zone has an instance of this
		class as its ``tau_star`` attribute. Any modifications to the attributes
		of this class should be made for **every zone**; if this is not
		ensured, the star formation law will not be consistent across all
		zones.

	Parameters
	----------
	area : real number
		The value of the attribute ``area``. See below.
	\*\*kwargs : varying types
		Other attributes can have their values set via keyword. See below.

	Attributes
	----------
	area : real number
		The surface area in :math:`kpc^2` of the corresponding annulus in a
		``milkyway`` model.
	present_day_molecular : real number [default : 2.0]
		The depletion time of molecular gas at the present day in Gyr. Positive
		definite.
	molecular_index : real number [default : 0.5]
		The power-law index on the time-dependence.
	Sigma_g1 : real number [default : 5.0e+06]
		The smaller of the two surface densities of gas at which there is a
		break in the Kennicutt-Schmidt relation. Assumes units of
		:math:`M_\odot kpc^{-2}`.
	Sigma_g2 : real number [default : 2.0e+07]
		The larger of the two surface densities of gas at which there is a
		break in the Kennicutt-Schmidt relation. Assumes units of
		:math:`M_\odot kpc^{-2}`.
	index1 : real number [default : 1.7]
		The index of the power-law at gas surface densities below ``Sigma_g1``.
	index2 : real number [default : 3.6]
		The index of the power-law at gas surface densities between ``Sigma_g1``
		and ``Sigma_g2``, above which it is assumed to be linear.
	mode : str ["sfr", "ifr", or "gas"] [default : "ifr"]
		The mode of the ``milkyway`` object.

	Calling
	-------
	Calling this object will calculate the star formation efficiency timescale
	:math:`\tau_\star` according to the parameters of the star formation law
	entered as attributes of this object. As in the ``singlezone`` object, this
	timescale is the gas supply per unit star formation in Gyr.

	Parameters:

			- time : real number
				Simulation time in Gyr. Postive definite.
			- arg2 : real number
				Either the gas supply in :math:`M_\odot` or the star formation
				rate in :math:`M_\odot Gyr^{-1}`. Will be called by VICE
				directly. With the attribute ``area``, the surface density of
				the corresponding quantity is known. Positive definite.

	Returns:

			- tau_star : real number
				The star formation efficiency timescale given that simulation
				time and star formation rate/gas supply, in Gyr (as necessary).

	.. seealso:: vice.milkyway

	Notes
	-----
	This object encodes the parameters of the desired Kennicutt-Schmidt relation
	into the ``milkyway`` object. This is the relationship relating the surface
	densities of star formation :math:`\dot{\Sigma}_\star` and gas
	:math:`\Sigma_\text{gas}`.

	This object implements a star formation law in the ``milkyway`` object
	defined according to:

	.. math:: \dot{\Sigma}_\star \sim \Sigma_\text{gas}^N

	The value of the power-law index :math:`N` has two breaks, at
	:math:`\Sigma_{\text{gas},1}` and :math:`\Sigma_{\text{gas},2}`.

	.. math::

		N = 1.0\ (\Sigma_\text{gas} \geq \Sigma_{\text{gas},2})
		\\
		N = \gamma_2\ (\Sigma_{\text{gas},1} \leq \Sigma_\text{gas} \leq
			\Sigma_{\text{gas},2})
		\\
		N = \gamma_1\ (\Sigma_\text{gas} \leq \Sigma_{\text{gas},1})

	The values :math:`\gamma_1` and :math:`\gamma_2` correspond to the
	attributes ``index1`` and ``index2``, respectively. As their names would
	suggest, :math:`\Sigma_{\text{gas},1}` and :math:`\Sigma_{\text{gas},2}`
	correspond to ``Sigma_g1`` and ``Sigma_g2``.

	The depletion time of molecular gas due to star formation
	:math:`\tau_\text{mol}` is defined according to the following
	scaling:

	.. math:: \tau_\text{mol} = \tau_{\text{mol},0} \left(t/t_0\right)^\beta

	where :math:`t_0` is the age of the universe today, :math:`t` is the age of
	the universe at some simulation time, and :math:`\tau_{\text{mol},0}` is
	:math:`\tau_\text{mol}` at the present day. Because the ``milkyway`` model
	only supports lookback times up to 13.2 Gyr, the relation between age of
	the universe and simulation time is a simple linear translation:

	.. math:: t = t_\text{sim} + 0.5\ \text{Gyr}

	with the assumption that :math:`t_0` = 13.7 Gyr is the age of the universe
	at the present day.

	.. [1] Johnson et al. (2021), arxiv:2103.09838
	"""

	def __init__(self, area, present_day_molecular = 2.0, molecular_index = 0.5,
		Sigma_g1 = 5.0e+06, Sigma_g2 = 2.0e+07, index1 = 1.7, index2 = 3.6,
		mode = "ifr"):
		self.area = area
		self.present_day_molecular = present_day_molecular
		self.molecular_index = molecular_index
		# allows value comparison in Sigma_g1 setter to pass w/o AttributeError
		self._Sigma_g2 = float("inf")
		self.Sigma_g1 = Sigma_g1
		self.Sigma_g2 = Sigma_g2
		self.index1 = index1
		self.index2 = index2
		if mode.lower() in ["sfr", "ifr", "gas"]:
			self._mode = mode.lower()
		else:
			raise SystemError("Internal Error.")


	def __call__(self, time, arg2):
		molecular = self.molecular(time)
		if self._mode in ["ifr", "gas"]:
			# arg2 represents the gas supply in Msun
			Sigma_gas = arg2 / self.area
			if Sigma_gas >= self.Sigma_g2:
				return molecular
			elif self.Sigma_g1 <= Sigma_gas <= self.Sigma_g2:
				return molecular * (Sigma_gas / self.Sigma_g2)**self._index2
			elif Sigma_gas:
				return molecular * (
					(self.Sigma_g1 / self.Sigma_g2)**self._index2 *
					(Sigma_gas / self.Sigma_g1)**self._index1
				)
			else:
				# avoid ZeroDivisionError if Sigma_gas == 0
				return float("inf") # force zero star formation
		else:
			# arg2 represents the star formation rate in Msun/yr
			Sigma_sfr = arg2 / self.area
			Sigma_sfr *= 1e9 # yr^-1 -> Gyr^-1

			# Solves for the star formation densities corresponding to
			# Sigma_g1 and Sigma_g2
			Sigma_sfr2 = self.Sigma_g2 / molecular
			Sigma_sfr1 = (self.Sigma_g1 / self.Sigma_g2)**(
				self._index2 * (1 - self._index2) /
				(self._index2 - self._index1)
			) / molecular * self.Sigma_g2**(
				self._index2 * (1 - self._index1) /
				(self._index2 - self._index1)
			) * self.Sigma_g1**(
				-self._index1 * (1 - self._index2) /
				(self._index2 - self._index1)
			)

			if Sigma_sfr >= Sigma_sfr2:
				return molecular
			elif Sigma_sfr1 <= Sigma_sfr <= Sigma_sfr2:
				return molecular**(1 / (1 - self._index2)) * (
					Sigma_sfr / self.Sigma_g2
				)**(self._index2 / (1 - self._index2))
			elif Sigma_sfr:
				return (self.Sigma_g1 / self.Sigma_g2)**(
					self._index2 / (1 - self._index1)
				) * molecular**(1 / (1 - self._index1)) * (
					Sigma_sfr / self.Sigma_g1
				)**(self._index1 / (1 - self._index1))
			else:
				# avoid ZeroDivisionError if Sigma_sfr == 0
				return 1.e-12 # will result in mgas = 0 regardless
				

	@property
	def area(self):
		r"""
		Type : float

		The surface area of the star forming region in :math:`kpc^2`. In the
		``milkway`` object, this is an annulus for which calculation of the
		area is trivial.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.zones[0].tau_star.area
		0.7853981633974483
		>>> mw.zones[10].tau_star.area
		16.493361431346415
		"""
		return self._area


	@area.setter
	def area(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				self._area = float(value)
			else:
				raise ValueError("Must be positive. Got: %g" % (value))
		else:
			raise TypeError("Must be a numerical value. Got: %s " % (
				type(value)))


	def molecular(self, time):
		r"""
		Calculate the star formation efficiency timescale of molecular gas at
		a given simulation time.

		**Signature**: x.molecular(time)

		Parameters
		----------
		x : ``J21_sf_law``
			An instance of this class.
		time : ``float``
			The simulation time in Gyr.

		Returns
		-------
		tau_star_mol : float
			The star formation efficiency timescale :math:`\tau_\star` for
			molecular gas only (:math:`\tau_\text{mol}`), defined accordingly:

			.. math:: \tau_\text{mol} = \tau_{\text{mol},0}
				\left(\frac{0.5 + t}{t_0}\right)^\gamma

			where :math:`\tau_{\text{mol},0}` is the value of
			:math:`\tau_\text{mol}` at the present day, :math:`t_0` is the
			present-day age of the universe (assumed to be 13.7 Gyr),
			:math:`\gamma` is the power-law index, and :math:`t` is the
			parameter ``time`` passed to this function. A value of 0.5 is added,
			beacuse the onset of star formation is assumed to occur 0.5 Gyr
			following the big bang in the Johnson et al. (2021) models [1]_.

			The values of :math:`\tau_{\text{mol},0}` and :math:`\gamma` are
			controlled by the attributes ``present_day_molecular`` and
			``molecular_index``, respectively.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.zones[0].tau_star.molecular(0)
		0.6617825960083583
		>>> mw.zones[0].tau_star.molecular(5)
		1.3776103291490314
		>>> mw.zones[0].tau_star.molecular(13.2)
		2.0

		.. [1] Johnson et al. (2021), arxiv:2103.09838
		"""
		return self.present_day_molecular * (
			(1.5 + time) / 13.7)**self.molecular_index


	@property
	def present_day_molecular(self):
		r"""
		Type : float

		Default : 2

		The star formation efficiency timescale of molecular gas at the
		present day, in Gyr. Scales with time according to a power-law whose
		index is given by teh value of the attribute ``molecular_index``. Must
		be positive.

		.. note:: In the interstellar medium and star formation literature,
			this quantity is more often referred to as the depletion time due
			to star formation. Default value is chosen based on the results of
			Leroy et al. (2008) [1]_.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.zones[0].tau_star.present_day_molecular
		2.0
		>>> for i in range(mw.n_zones):
		>>> 	mw.zones[i].tau_star.present_day_molecular = 1.0
		>>> mw.zones[0].tau_star.present_day_molecular
		1.0

		.. [1] Leroy et al. (2008), AJ, 136, 2782
		"""
		return self._present_day_molecular


	@present_day_molecular.setter
	def present_day_molecular(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				self._present_day_molecular = float(value)
			else:
				raise ValueError("Must be positive. Got: %g" % (value))
		else:
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value)))


	@property
	def molecular_index(self):
		r"""
		Type : float

		Default : 0.5

		The power-law index on the time-dependence of the molecular gas star
		formation efficiency timescale. The normalization will be set such
		that the value at :math:`t` = 12 Gyr is equal to the value of the
		attribute ``present_day_molecular``.

		.. note:: The default value is chosen based on the redshift dependence
			of :math:`\tau_\text{mol}` reported by Tacconi et al. (2018) [1]_
			and a redshift-time relation accurate for :math:`z \lesssim 3`.
			See discussion in section 2 of Johnson et al. (2021) [2]_.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.zones[0].tau_star.molecular_index
		0.5
		>>> for i in range(mw.n_zones):
		>>> 	mw.zones[i].tau_star.molecular_index = 0.6
		>>> mw.zones[0].tau_star.molecular_index
		0.6

		.. [1] Tacconi et al. (2018), ApJ, 853, 179
		.. [2] Johnson et al. (2021), arxiv:2103.09838
		"""
		return self._molecular_index

	@molecular_index.setter
	def molecular_index(self, value):
		if isinstance(value, numbers.Number):
			self._molecular_index = float(value)
		else:
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value)))


	@property
	def Sigma_g1(self):
		r"""
		Type : float

		Default : 5.0e+06

		The lower of the two surface densities of gas at which there is a break
		in the :math:`\dot{\Sigma}_\star - \Sigma_\text{gas}` relation. Below
		this value, the relation scales as a power-law with index set by the
		attribute ``index1``. Assumes units of :math:`M_\odot kpc^{-2}`.

		.. note:: The value of this attribute should be smaller than that of
			the attribute ``Sigma_g2``, the larger of the two surface
			densities of gas. Default values are chosen based on the aggregate
			data from Bigiel et al. (2010) [1]_ and Leroy et al. (2013) [2]_
			presented in Krumholz et al. (2018) [3]_.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.zones[0].tau_star.Sigma_g1
		5.0e+06
		>>> for i in range(mw.n_zones):
		>>> 	mw.zones[i].tau_star.Sigma_g1 = 6.0e+06
		>>> mw.zones[0].tau_star.Sigma_g1
		6.0e+06

		.. [1] Bigiel et al. (2010), AJ, 140, 1194
		.. [2] Leroy et al. (2013), AJ, 146, 19
		.. [3] Krumholz et al. (2018), MNRAS, 477, 2716
		"""
		return self._Sigma_g1

	@Sigma_g1.setter
	def Sigma_g1(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				if value <= self.Sigma_g2:
					self._Sigma_g1 = float(value)
				else:
					raise ValueError("""Attribute 'Sigma_g1' must not be \
greater than 'Sigma_g2'.""")
			else:
				raise ValueError("Attribute 'Sigma_g1' must be positive.")
		else:
			raise TypeError("""Attribute 'Sigma_g1' must be a numerical value. \
Got: %s.""" % (type(value)))


	@property
	def Sigma_g2(self):
		r"""
		Type : float

		Default : 2.0e+07

		The larger of the two surface densities of gas at which there is a break
		in the :math:`\dot{\Sigma}_\star - \Sigma_\text{gas}` relation. Below
		this value, the relation scales as a power-law with index set by the
		attribute ``index2``, and above it, it is assumed to be linear. Assumes
		units of :math:`M_\odot kpc^{-2}`.

		.. note:: The value of this attribute should be larger than that of the
			attribute ``Sigma_g1``, the smaller of the two surface densities of
			gas. Default values are chosen based on the aggregate data from
			Bigiel et al. (2010) [1]_ and Leroy et al. (2013) [2]_ presented in
			Krumholz et al (2018) [3]_.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.zones[0].tau_star.Sigma_g2
		2.0e+07
		>>> for i in range(mw.n_zones):
		>>> 	mw.zones[i].tau_star.Sigma_g2 = 1.5e+07
		>>> mw.zones[0].tau_star.Sigma_g2
		1.5e+07

		.. [1] Bigiel et al. (2010), AJ, 140, 1194
		.. [2] Leroy et al. (2013), AJ, 146, 19
		.. [3] Krumholz et al. (2018), MNRAS, 477, 2716
		"""
		return self._Sigma_g2

	@Sigma_g2.setter
	def Sigma_g2(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				if value >= self.Sigma_g1:
					self._Sigma_g2 = float(value)
				else:
					raise ValueError("""Attribute 'Sigma_g2' must not be \
smaller than 'Sigma_g1'.""")
			else:
				raise ValueError("Attribute 'Sigma_g2' must be positive.")
		else:
			raise TypeError("""Attribute 'Sigma_g2' must be a numerical value. \
Got: %s""" % (type(value)))


	@property
	def index1(self):
		r"""
		Type : float

		Default : 1.7

		The power-law index of the :math:`\dot{\Sigma}_\star - \Sigma_\text{gas}`
		relation at gas surface densities :math:`\Sigma_\text{gas} \leq
		\Sigma_{\text{gas},1}`, where :math:`\Sigma_{\text{gas},1}` is the
		value of the attribute ``Sigma_g1``.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.zones[0].tau_star.index1
		1.7
		>>> for i in range(mw.n_zones):
		>>> 	mw.zones[i].tau_star.index1 = 1.5
		>>> mw.zones[0].tau_star.index1
		1.5
		"""
		return -self._index1 + 1

	@index1.setter
	def index1(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				# Store the index of the \tau_\star - \Sigma_gas relation
				self._index1 = -(float(value) - 1)
			else:
				raise ValueError("""Attribute 'index1' must be positive. \
Got: %g""" % (value))
		else:
			raise TypeError("""Attribute 'index1' must be a numerical value. \
Got: %s""" % (type(value)))


	@property
	def index2(self):
		r"""
		Type : float

		Default : 3.6

		The power-law index of the :math:`\dot{\Sigma}_\star - \Sigma_\text{gas}`
		relation at gas surface densities :math:`\Sigma_\text{gas}` between
		:math:`\Sigma_{\text{gas},1}` and :math:`\Sigma_{\text{gas},2}`, the
		values of the attributes ``Sigma_g1`` and ``Sigma_g2``, respectively.
		At :math:`\Sigma_\text{gas} \geq \Sigma_{\text{gas},2}`, the relation
		is assumed to be linear.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.zones[0].tau_star.index2
		3.6
		>>> for i in range(mw.n_zones):
		>>> 	mw.zones[i].tau_star.index2 = 3.4
		>>> mw.zones[0].tau_star.index2
		3.4
		"""
		return -self._index2 + 1

	@index2.setter
	def index2(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				# Store the index of the \tau_\star - \Sigma_gas relation
				self._index2 = -(float(value) - 1)
			else:
				raise ValueError("""Attribute 'index2' must be positive. \
Got: %g""" % (value))
		else:
			raise TypeError("""Attribute 'index1' must be a numerical value. \
Got: %s""" % (type(value)))


	@property
	def mode(self):
		r"""
		Type : str

		Default : "ifr"

		The mode of the ``milkyway`` model being ran. Users may not modify this
		attribute directly; instead they should modify the corresponding
		attribute of the ``milkyway`` object.

		Example Code
		------------
		>>> import vice
		>>> mw = vice.milkyway(name = "example")
		>>> mw.zones[0].tau_star.mode
		"ifr"
		>>> mw.mode = "sfr"
		>>> mw.zones[0].tau_star.mode
		"sfr"
		"""
		return self._mode

