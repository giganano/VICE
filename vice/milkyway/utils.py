r"""
milkyway utilities
==================
.. note:: The objects contained in this file are intended for internal usage
	by the ``milkyway`` object. User access is discouraged.

- ``mass_from_surface_density`` : ``object``
	An object which converts surface densities in masses.
"""

import numbers


class mass_from_surface_density:

	r"""
	An object which converts surface densities of gas in
	:math:`M_\odot kpc^{-2}` and surface densities of infall and star formation
	in :math:`M_\odot yr^{-1} kpc^{-2}` as functions of time in Gyr to absolute
	values/rates in :math:`M_\odot` or :math:`M_\odot yr^{-1}`.

	.. warning:: This object is intended for internal usage by VICE's
		``milkyway`` object. User access is discouraged.

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
		set by the attribute ``mode`` of the ``milkyway`` model.
	radius : float
		The exact radius in kpc that an annulus is assumed to represent. In
		these models, this is the arithmetic mean of the edges of an annulus.
		This is the radius that the functional attribute ``surface_density``
		will be evaluated at in simulation.
	area : float
		The area of the corresponding annulus in the disk model in
		:math:`kpc^2`.
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

		.. warning:: This object is intended for internal usage by VICE's
			``milkyway`` object. User access is discouraged.
		"""
		return self._surface_density


	@property
	def radius(self):
		r"""
		Type : float

		The exact radius in kpc that an annulus is assumed to represent. In
		these models, this is the arithmetic mean of the edges of an annulus.
		This is the radius that the attribute ``surface_density`` will be
		evaluated at in simulations using the ``milkyway`` object.

		.. warning:: This object is intended for internal usage by VICE's
			``milkyway`` object. User access is discouraged.
		"""
		return self._radius


	@property
	def area(self):
		r"""
		Type : float

		The area of the corresponding annulus in the milkyway model in
		:math:`kpc^2`. With known galactocentric radii of the inner and outer
		edge, the area follows the simple definition:

		.. math:: A = \pi (r_2^2 - r_1^2)

		.. warning:: This object is intended for internal usage by VICE's
			``milkyway`` object. User access is discouraged.
		"""
		return self._area

