r"""
Implement the vice.yields.agb.interpolator, which constructs a 2-D linear
interpolation scheme off of the built-in yield sets.
"""

from ...toolkit.interpolation.interp_scheme_2d import interp_scheme_2d
from ._grid_reader import yield_grid


class interpolator(interp_scheme_2d):

	r"""
	A bi-linear interpolation scheme constructed from the yield tables built
	into the vice.yields.agb module.

	**Signature**: vice.yields.agb.interpolator(element, study = "cristallo11")

	.. versionadded:: 1.2.0

	Parameters
	----------
	element : ``str`` [case-insensitive]
		The symbol of the element to obtain the yield grid for.
	study : ``str`` [case-insensitive] [default : "cristallo11"]
		A keyword denoting which study to pull the yield table from.

		Recognized keywords:

			- "cristallo11" : Cristallo et al. (2011, 2015) [1]_ [2]_
			- "karakas10" : Karakas (2010) [3]_
			- "ventura13" : Ventura et al. (2013) [4]_
			- "karakas16": Karakas & Lugaro (2016) [5]_; Karkas et al. (2018)
				[6]_

		.. versionadded:: 1.3.0
			The "ventura13" and "karakas16" yield models were introduced in
			version 1.3.0.

	Attributes
	----------
	masses : ``list`` [elements of type ``float``]
		The masses on which the yield table is sampled.
	metallicities : ``list`` [elements of type ``float``]
		The metallicities on which the yield table is sampled.
	yields : ``list`` [elements of type ``list``]
		The yields at each stellar mass and metallicity reported by the
		adopted study.

	Calling
	-------
	Call this object with stellar mass and metallicity to compute the
	fractional net yield for such an AGB star, estimated via bi-linear
	interpolation.

		Parameters:

			- mass : real number
				The stellar mass of an AGB star in solar masses.
			- metallicity : real number
				The metallicity by mass :math:`Z` of the AGB star.

		Returns:

			- y : real number
				The fractional net yield, estimated via bi-linear
				interpolation. See `Notes`_ below.

	.. tip:: This object can be used as a callable object to describe the
		AGB star yields of any given element. For the base class, it makes
		little sense to do so, since this is the same as setting the yield to
		the study itself. However, alternate functionality or interpolation
		schema can be achieved by subclassing this object and overriding the
		``__call__`` function.

	Notes
	-----
	To conduct the interpolation, this object first finds the masses and
	metallicities on the grid that enclose the values passed as parameters
	when this object is called. It then interpolates linearly in metallicity at
	constant mass twice, then once in mass at constant metallicity to determine
	the value of the yield at the appropriate mass and metallicity. If the
	mass and/or metallicity are above or below the maximum or minimum values
	of the grid, the interpolation scheme falls back on linear extrapolation
	off of the two largest/smallest values.

	This object inherits its functionality from
	``vice.toolkit.interpolation.interp_scheme_2d``, where the stellar masses
	are the x-coordinates, the metallicities the y-coordiantes, and the
	yields the z-coordinates. For further details, see the associated
	documentation.

	.. warning:: VICE's AGB star yield interpolation routines force negative
		yields to zero below 1.5 :math:`M_\odot` in order to prevent numerical
		artifacts associated with extrapolation to stellar masses below the
		table of yields. This object does **not** include this functionality;
		numerical artifacts may be introduced as a consequence (see "Asymptotic
		Giant Branch Stars" under "Nucleosynthetic Yields" in VICE's science
		documentation: https://vice-astro.readthedocs.io/en/latest/science_documentation/index.html).
		If this correction is desired, users should subclass this object and
		add the following ``if`` statement to the ``__call__`` function for a
		value ``y`` returned from the inherited ``__call__`` function:
		``if mass < 1.5 and y < 0: return 0``.

	Example Code
	------------
	>>> import vice
	>>> example = vice.yields.agb.interpolator('c')
	>>> example.masses
	[1.3, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]
	>>> example.metallicities
	[0.0001, 0.0003, 0.001, 0.002, 0.003, 0.006, 0.008, 0.01, 0.014, 0.02]
	>>> example.yields[0]
	[0.00233122,
	 0.00206212,
	 0.00163226,
	 0.00150313,
	 0.000781408,
	 0.000406231,
	 -5.03077e-05,
	 -0.000150308,
	 -0.000317615,
	 -0.000422]
	>>> example.yields[2]
	[0.00760034,
	 0.00650061,
	 0.0060516,
	 0.00610347,
	 0.00510498,
	 0.00443045,
	 0.00347925,
	 0.0035931,
	 0.0026206,
	 0.002503]
	>>> # the yield at 2.2 solar masses and Z = 0.011
	>>> example(2.2, 0.011)
	0.004022337000000001
	>>> example(5.4, 0.0036)
	0.0004046900263999999
	>>> example(1.8, 0.018)
	0.0017274533333333335

	.. [1] Cristallo et al. (2011), ApJS, 197, 17
	.. [2] Cristallo et al. (2015), ApJS, 219, 40
	.. [3] Karakas (2010), MNRAS, 403, 1413
	.. [4] Ventura et al. (2013), MNRAS, 431, 3642
	.. [5] Karakas & Lugaro (2016), ApJ, 825, 26
	.. [6] Karakas et al. (2018), MNRAS, 477, 421
	"""

	def __init__(self, element, study = "cristallo11"):
		# let the grid reader function do the error handling
		yields, masses, metallicities = yield_grid(element, study = study)
		super().__init__(list(masses), list(metallicities), list(yields))

	@property
	def masses(self):
		r"""
		Type : ``list`` [elements of type ``float``]

		The stellar masses in :math:`M_\odot` on which the yield grid is
		sampled.

		Example Code
		------------
		>>> import vice
		>>> example = vice.yields.agb.interpolator('c')
		>>> example.masses
		[1.3, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]
		>>> example = vice.yields.agb.interpolator('c', study = "karakas10")
		[1.0,
		 1.25,
		 1.5,
		 1.75,
		 1.9,
		 2.25,
		 2.5,
		 3.0,
		 3.5,
		 4.0,
		 4.5,
		 5.0,
		 5.5,
		 6.0]
		"""
		return super().xcoords

	@property
	def metallicities(self):
		r"""
		Type : ``list`` [elements of type ``float``]

		The metallicities by mass :math:`Z = M_z / M_\star` of the AGB stars
		on which the yield grid is sampled.

		Example Code
		------------
		>>> import vice
		>>> example = vice.yields.agb.interpolator('c')
		>>> example.metallicities
		[0.0001, 0.0003, 0.001, 0.002, 0.003, 0.006, 0.008, 0.01, 0.014, 0.02]
		>>> example = vice.yields.agb.interpolator('c', study = "karakas10")
		>>> example.metallicities
		[0.0001, 0.004, 0.008, 0.02]
		"""
		return super().ycoords

	@property
	def yields(self):
		r"""
		Type : ``list`` [elements of type ``list``, storing ``float`` types]

		The fractional net yields of the given element on which the yield
		grid is sampled.

		Example Code
		------------
		>>> import vice
		>>> example = vice.yields.agb.interpolator('c')
		>>> example.yields[0]
		[0.00233122,
		 0.00206212,
		 0.00163226,
		 0.00150313,
		 0.000781408,
		 0.000406231,
		 -5.03077e-05,
		 -0.000150308,
		 -0.000317615,
		 -0.000422]
		>>> example.yields[2]
		[0.00760034,
		 0.00650061,
		 0.0060516,
		 0.00610347,
		 0.00510498,
		 0.00443045,
		 0.00347925,
		 0.0035931,
		 0.0026206,
		 0.002503]
		>>> example = vice.yields.agb.interpolator('c', study = "karakas10")
		>>> example.yields[0]
		[0.000250197, -3.861e-05, -6.944e-05, -0.0001502]
		>>> example.yields[2]
		[0.00773393, 0.00111333, -5.62667e-05, -0.0004974]
		"""
		return super().zcoords

