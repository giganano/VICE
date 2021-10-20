r"""
This file implements the Ertl et al. (2016) explodability engine as an instance
of a derived class.
"""

from __future__ import absolute_import
from ...._globals import _DIRECTORY_
from ....toolkit.interpolation import interp_scheme_1d
from .._yield_integrator import _MINIMUM_MASS_
from .read_engine import read
from .engine import engine
import numbers


class E16(engine):

	r"""
	Core collapse supernova explosion engine as calculated by Ertl et al.
	(2016) [1]_ and studied in Griffith et al. (2021) [2]_.

	**Signature**: from vice.yields.ccsne.engines import E16

	.. versionadded:: 1.2.0

	.. tip:: This object can be passed as the keyword argument ``explodability``
		to ``vice.yields.ccsne.fractional`` to calculate IMF-averaged yields
		assuming this black hole landscape.

	Attributes
	----------
	masses : ``list``
		The stellar masses in :math:`M_\odot` on which the explosion engine is
		sampled.
	m4 : ``list``
		The quantity :math:`M_4` at the time of core collapse for stars with
		ZAMS masses given by the attribute ``masses``. Values are taken from
		Sukhbold et al. (2016) [3]_. See `Notes`_.
	mu4 : ``list``
		The quantity :math:`\mu_4` at the time of core collapse for stars with
		ZAMS masses given by the attribute ``masses``. Values are taken from
		Sukhbold et al. (2016). See `Notes`_.
	slope : ``float`` [default : 0.283]
		The slope of the line in :math:`\mu_4-\mu_4M_4` space dividing
		progenitors which explode and collapse.
	intercept : ``float`` [default : 0.043]
		The intercept of the line in :math:`\mu_4-\mu_4M_4` space dividing
		progenitors which explode and collapse.
	frequencies : ``list``
		The fraction of stars at the sampled masses that explode as a core
		collapse supernova. Though this attribute has meaning for other
		``engine`` objects, here it simply returns the binary 0 or 1 describing
		whether or not each element of the attribute ``masses`` explodes under
		the current parameters.

	Calling
	-------
	Call this object with progenitor mass as the only argument, and either 0 or
	1 will be returned based on whether or not such a progenitor should explode
	based on the current attributes of this object.

		Parameters:

			- mass : ``float``
				Progenitor zero age main sequence mass in :math:`M_\odot`.

		Returns:

			- explodability : ``float``
				1 if the star would produce a core collapse supernova under the
				current assumptions, and 0 if it would collapse to a black hole.

				.. note:: The base class ``engine`` will return non-binary
					values for masses between grid elements where the explosion
					frequency is 0 and 1. This derived class, however, will
					always return a binary value.

	Notes
	-----
	The base class ``engine`` determines explodability by linearly
	interpolating between elements of the grid defined by the attributes
	``masses`` and ``frequencies``. This class, however, linearly interpolates
	on the ``masses``-``m4`` and ``masses``-``mu4`` grids to determine
	:math:`M_4` and :math:`\mu_4` at a given progenitor zero age main sequence
	(ZAMS) mass. Whether or not this progenitor would explode is then
	determined according to the following criterion:

	.. math:: \mu_4 \leq a M_4 \mu_4 + b

	where :math:`a` and :math:`b` are the attributes ``slope`` and
	``intercept``. Default values of :math:`a` = 0.283 and :math:`b` = 0.043
	are adopted from Ertl et al. (2016), while the ``m4`` and ``mu4`` tables
	are taken from Sukhbold et al. (2016). The attribute ``frequencies`` plays
	no role in this calculation.

	Example Code
	------------
	>>> from vice.yields.ccsne.engines import E16
	>>> E16.masses
	[9.0,
	 9.25,
	 9.5,
	 ...,
	 80.0,
	 100.0,
	 120.0]
	>>> E16.m4
	[1.357,
	 1.36955,
	 1.38349,
	 ...,
	 1.66232,
	 1.81718,
	 1.60252]
	>>> E16.mu4
	[1.79891e-05,
	 0.000933825,
	 0.00210795,
	 ...,
	 0.0896075,
	 0.103897,
	 0.0759102]
	>>> E16(20)
	0.0
	>>> E16(21)
	1.0
	>>> E16(22)
	0.0

	.. [1] Ertl et al. (2016), ApJ, 818, 124
	.. [2] Griffith et al. (2021), arxiv:2103.09837
	.. [3] Sukhbold et al. (2016), ApJ, 821, 38
	"""

	def __init__(self, slope = 0.283, intercept = 0.043):
		masses, m4, mu4 = read("%syields/ccsne/engines/mu4_M4.dat" % (
			_DIRECTORY_))
		self.__m4_interpolator = interp_scheme_1d(masses, m4)
		self.__mu4_interpolator = interp_scheme_1d(masses, mu4)
		super().__init__(masses, len(masses) * [0.])
		self.slope = slope
		self.intercept = intercept


	def __call__(self, mass):
		if isinstance(mass, numbers.Number):
			if mass < _MINIMUM_MASS_:
				return 0.
			else:
				m4 = self.__m4_interpolator(mass)
				mu4 = self.__mu4_interpolator(mass)
				return float(mu4 <= self._slope * m4 * mu4 + self._intercept)
		else:
			raise TypeError("Must be a numerical value. Got: %s" % (type(mass)))


	@property
	def m4(self):
		r"""
		Type : ``list`` [elements of type ``float``]

		The quantity :math:`M_4` at the time of core collapse for stars with
		ZAMS masses given by the attribute ``masses``. :math:`M_4` is defined
		as the normalized mass enclosed in a region defined by the
		dimensionless energy per nucleon of :math:`s` = 4.

		Ertl et al. (2016) [1]_ conclude that the quantities :math:`M_4` and
		:math:`\mu_4` can predict whether or not a massive star will produce
		a core collapse supernova based on the following criterion with only a
		few exceptions (~1 - 2.5%):

		.. math:: \mu_4 \leq a M_4 \mu_4 + b

		where they report :math:`a` = 0.283 and :math:`b` = 0.043 as best fit
		values. The values of :math:`a` and :math:`b` are controlled by the
		attributes ``slope`` and ``intercept`` respectively.

		.. note:: This attribute's values are adopted from Sukhbold et al.
			(2016) [2]_.

		Example Code
		------------
		>>> from vice.yields.ccsne.engines import E16
		>>> E16.m4
		[1.357,
		 1.36955,
		 1.38349,
		 ...,
		 1.66232,
		 1.81781,
		 1.60252]

		.. [1] Ertl et al. (2016), ApJ, 818, 124
		.. [2] Sukhbold et al. (2016), ApJ, 821, 38
		"""
		return self.__m4_interpolator.ycoords


	@property
	def mu4(self):
		r"""
		Type : ``list`` [elements of type ``float``]

		The quantity :math:`\mu_4` at the time of core collapse for stars with
		ZAMS masses given by the attribute ``masses``. :math:`\mu_4` is defined
		as the normalized mass derivative in a region defined by the
		dimensionless energy per nucleon of :math:`s` = 4:

		.. math:: \mu_4 \equiv (dm/M_\odot)/(dr/1000 km)|_{s = 4}

		Ertl et al. (2016) [1]_ conclude that the quantities :math:`M_4` and
		:math:`\mu_4` can predict whether or not a massive star will produce
		a core collapse supernova based on the following criterion with only a
		few exceptions (~1 - 2.5%):

		.. math:: \mu_4 \leq a M_4 \mu_4 + b

		where they report :math:`a` = 0.283 and :math:`b` = 0.043 as best fit
		values. The values of :math:`a` and :math:`b` are controlled by the
		attributes ``slope`` and ``intercept``, respectively.

		.. note:: This attribute's values are adopted from Sukhbold et al.
			(2016) [2]_.

		Example Code
		------------
		>>> from vice.yields.ccsne.engines import E16
		>>> E16.mu4
		[1.79891e-05,
		 0.000933825,
		 0.00210795,
		 ...,
		 0.0896075,
		 0.103897,
		 0.0759102]

		.. [1] Ertl et al. (2016), ApJ, 818, 124
		.. [2] Sukhbold et al. (2016), ApJ, 821, 38
		"""
		return self.__mu4_interpolator.ycoords


	@property
	def slope(self):
		r"""
		Type : ``float`` [default : 0.283]

		The slope of the line in :math:`\mu_4-M_4\mu_4` space dividing
		progenitors which explode and collapse. Ertl et al. (2016) [1]_ argue
		that the quantities :math:`M_4` and :math:`\mu_4` can predict whether
		or not a massive star will produce a core collapse supernova based on
		the following criterion with only a few exceptions (~1 - 2.5%):

		.. math:: \mu_4 \leq a M_4 \mu_4 + b

		where this attribute encodes the value of :math:`a`.

		Example Code
		------------
		>>> from vice.yields.ccsne.engines import E16
		>>> E16.slope
		0.283
		>>> E16.slope = 0.3
		>>> E16.slope
		0.3
		>>> E16.slope = 0.25
		>>> E16.slope
		0.25

		.. [1] Ertl et al. (2016), ApJ, 818, 124
		"""
		return self._slope

	@slope.setter
	def slope(self, value):
		if isinstance(value, numbers.Number):
			self._slope = float(value)
		else:
			raise TypeError("""Attribute 'slope' must be a numerical value. \
Got: %s.""" % (type(value)))


	@property
	def intercept(self):
		r"""
		Type : ``float`` [default : 0.043]

		The intercept of the line in :math:`\mu_4-M_4\mu_4` space dividing
		progenitors which explode and collapse. Ertl et al. (2016) [1]_ argue
		that the quantities :math:`M_4` and :math:`\mu_4` can predict whether
		or not a massive star will produce a core collapse supernova based on
		the following criterion with only a few exceptions (~1 - 2.5%):

		.. math:: \mu_4 \leq a M_4 \mu_4 + b

		where this attribute encodes the value of :math:`b`.

		Example Code
		------------
		>>> from vice.yields.ccsne.engines import E16
		>>> E16.intercept
		0.043
		>>> E16.intercept = 0.04
		>>> E16.intercept
		0.04
		>>> E16.intercept = 0.045
		>>> E16.intercept
		0.045

		.. [1] Ertl et al. (2016), ApJ, 818, 124
		"""
		return self._intercept


	@intercept.setter
	def intercept(self, value):
		if isinstance(value, numbers.Number):
			self._intercept = float(value)
		else:
			raise TypeError("""Attribute 'intercept' must be a numerical \
value. Got: %s.""" % (type(value)))


	@property
	def frequencies(self):
		r"""
		Type : ``list``

		The frequencies with which stars of a given mass explode; the
		progenitor zero age main sequence masses in :math:`M_\odot` are stored
		in the attribute ``masses``. Though this number can be anywhere between
		0 and 1, in the current version they are binary.

		In this derived class, this attribute plays no role in the
		interpolation to determine if a star of a given progenitor mass should
		explode. This simply determines which of the progenitor masses explode
		under the current parameters by calling the instance for each element
		of the attribute ``masses``.

		Example Code
		------------
		>>> from vice.yields.ccsne.engines import E16
		>>> E16.frequencies
		[1.0,
		 1.0,
		 1.0,
		 ...,
		 0.0,
		 0.0,
		 1.0]
		"""
		return [self.__call__(_) for _ in self.masses]

