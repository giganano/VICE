
from __future__ import absolute_import
from ._interp_scheme_1d import c_interp_scheme_1d


class interp_scheme_1d(c_interp_scheme_1d):

	r"""
	A 1-dimensional interpolation scheme. This object takes in x-coordinates
	and y-coordinates of the same length and constructs a continuous function
	by connecting the points with straight lines.

	**Signature**: vice.toolkit.interpolation.interp_scheme_1d(xcoords, ycoords)

	.. versionadded:: 1.2.0

	Parameters
	----------
	xcoords : array-like
		The attribute ``xcoords``. See below.
	ycoords : array-like
		The attribute ``ycoords``. See below.

	Attributes
	----------
	xcoords : ``list`` [elements are real numbers]
		The x-coordinates of the points to construct the interpolation scheme
		out of, in arbitrary units.

		.. note:: These values will be automatically sorted from least to
			greatest upon construction of an ``interp_scheme_1d`` object. While
			this could potentially alter the ordering of this attribute, it
			will not affect the ``ycoords`` attribute, which is assumed to
			correspond component-wise to the x-coordinates in their least to
			greatest ordering.

	ycoords : ``list`` [elements are real numbers]
		The y-coordinates of the points to construct the interpolation scheme
		out of, in arbitrary units.

	Calling
	-------
	Call this object with a given x-coordinate, and it will automatically
	determine the correct pair of (x, y) coordinates to interpolate from, and
	return the appropriate value.

		Parameters:

			- x : real number
				The x-coordinate to evaluate the interpolation scheme at, in
				the same units as the attribute ``xcoords``.

		Returns:

			- y : real number
				The value of the y-coordinate, approximated via the line
				connecting the two points :math:`(x_1, y_1)` and
				:math:`(x_2, y_2)` such that :math:`x_1 \leq x \leq x_2`. If
				``x`` is less than the smallest x-coordinate or larger than
				the largest one, the result will be determined via linear
				extrapolation using either the two smallest or two largest
				elements of the ``xcoords`` attribute.

	Indexing
	--------
	Index this object as you would an array-like object, and it will return the
	(x, y) coordinates of the sampled points from the attributes ``xcoords``
	and ``ycoords``.

	Example Code
	------------
	>>> from vice.toolkit.interpolation import interp_scheme_1d
	>>> example = interp_scheme_1d([1, 2, 3], [2, 4, 6])
	>>> example(0)
	0.0
	>>> example(5)
	10.0
	>>> example(4)
	8.0
	>>> example[:]
	[[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]]
	>>> example.xcoords
	[1.0, 2.0, 3.0]
	>>> example.ycoords
	[2.0, 4.0, 6.0]
	>>> example.n_points
	3
	"""

	# This seemingly pointless code ensures that a signature will be found
	# when an interp_scheme_1d object is passed to inspect.signature, allowing
	# this class to be used in a multitude of places throughout VICE.

	def __call__(self, x):
		return super().__call__(x)

