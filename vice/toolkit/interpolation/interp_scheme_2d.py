
from __future__ import absolute_import
from ._interp_scheme_2d import c_interp_scheme_2d


class interp_scheme_2d(c_interp_scheme_2d):

	r"""
	A 2-dimensional interpolation scheme. This object takes in x-, y-, and
	z-coordinates of the appropriate lengths and constructs a continuous
	function by connecting the points with bilinear interpolation.

	**Signature**: vice.toolkit.interpolation.interp_scheme_2d(xcoords, ycoords,
	zcoords)
	
	.. versionadded:: 1.2.0

	Parameters
	----------
	xccords : array-like
		The attribute ``xcoords``. See below.
	ycoords : array-like
		The attribute ``ycoords``. See below.
	zcoords : array-like
		The attribute ``zcoords``. See below.

	Attributes
	----------
	xcoords : ``list`` [elements are real numbers]
		The x-coordinates of the points to construct the interpolation scheme
		out of, in arbitrary units.

		.. note:: These values will be automatically sorted from least to
			greatest upon construction of an ``interp_scheme_2d`` object. While
			this could potentially alter the ordering of this attribute, it
			will not affect the ``zcoords`` attribute, which is assumed to
			correspond component-wise to the x-coordinates in their least to
			greatest sorting. The burden is on the user to ensure that their
			coordinates are in the proper ordering.

	ycoords : ``list`` [elements are real numbers]
		The y-coordinates fo the points to construct the interpolation scheme
		out of, in arbitrary units.

		.. note:: The same note which applies to the x-coordinates above also
			applies to the y-coordinates.

	zcoords : ``list`` [elements are of type ``list`` containing real numbers]
		The z-coordinates of the points to construct the interpolation scheme
		out of, in arbitrary units. This must be of the same length as the
		``xcoords`` array, containing elements which are of the same length as
		the ``ycoords`` array. The values stored should correspond
		component-wise to those arrays such that
		``self(xcoords[i], ycoords[j]) = zcoords[i][j]``.

	Calling
	-------
	Call this object with any given x- and y-coordinates, and it will
	automatically determine the correct set of (x, y) coordinates to
	interpolate between, and return the appropriate value.

		Parameters:

			- x : real number
				The x-coordinate to evaluate the interpolation scheem at, in
				the same units as the attribute ``xcoords``.
			- y : real number
				The y-coordinate to evaluate the interpolation scheme at, in
				the same units as the attribute ``ycoords``.

		Returns:

			- z : real number
				The value of the z-coordinate, approximated via bilinear
				interpolation connecting the points :math:`(x_1, y_1)`,
				:math:`(x_1, y_2)`, :math:`(x_2, y_1)`, and :math:`(x_2, y_2)`:
				the points defining the four corners of the box in x-y space
				bouding the point (``x``, ``y``).

				The interpolation is such that the values of :math:`f(x_1, y)`
				and :math:`f(x_2, y)` are determined via linear interpolation in
				one-dimension at constant :math:`x`, then the value of
				:math:`f(x, y)` is calculated similarly at constant :math:`y`.

	Example Code
	------------
	>>> from vice.toolkit.interpolation import interp_scheme_2d
	>>> example = interp_scheme_2d([1, 2, 3], [2, 4, 6],
		[[3, 6, 9], [4, 8, 12], [5, 10, 15]])
	>>> example(0, 0)
	0.0
	>>> example(10, 10)
	60.0
	>>> example(3.1, 2.8)
	7.140000000000001
	>>> example.xcoords
	[1, 2, 3]
	>>> example.ycoords
	[2, 4, 6]
	>>> example.zcoords
	[[3, 6, 9], [4, 8, 12], [5, 10, 15]]
	"""

	# This seemingly pointless code ensures that a signature will be found
	# when an interp_scheme_2d object is passed to inspect.signature, allowing
	# this class to be used in a multitude of places throughout VICE.
	def __call__(self, x, y):
		return super().__call__(x, y)

