/*
 * This file implements the core routines of the interp_scheme_2d object.
 */

#include <math.h>
#include "interp_scheme_2d.h"
#include "../utils.h"


/*
 * Evaluate an interp_scheme_2d object at some value of the x- and
 * y-coordinates.
 *
 * Parameters
 * ==========
 * is2d: 		The interp_scheme_2d object to evaluate as a function.
 * x: 			The value of the x-coordinate to evaluate at.
 * y: 			The value of the y-coordinate to evaluate at.
 *
 * Returns
 * =======
 * is2d(x), the value of the function f(x, y) approximated via 2-D linear
 * interpolation off the known (x, y, z) values of the interpolation scheme.
 *
 * header: interp_scheme_2d.h
 */
extern double interp_scheme_2d_evaluate(INTERP_SCHEME_2D is2d, double x,
	double y) {

	long x_bin = get_bin_number(is2d.xcoords, is2d.n_x_values - 1ul, x);
	long y_bin = get_bin_number(is2d.ycoords, is2d.n_y_values - 1ul, y);

	if (x_bin == -1l) {
		/*
		 * The x-coordinate is either larger than the largest x-coordinate or
		 * smaller than the smallest one.
		 */
		if (x < is2d.xcoords[0]) {
			x_bin = 0ul;
		} else if (x > is2d.xcoords[is2d.n_x_values - 1ul]) {
			x_bin = (signed) is2d.n_x_values - 2l;
		} else {
			/* error handling for manylinux1 distribution */
			#ifdef NAN
				return NAN;
			#else
				return 0;
			#endif
		}
	}

	/* Same check for the y-coordinate */
	if (y_bin == -1l) {
		if (y < is2d.ycoords[0]) {
			y_bin = 0ul;
		} else if (y > is2d.ycoords[is2d.n_y_values - 1ul]) {
			y_bin = (signed) is2d.n_y_values - 2l;
		} else {
			#ifdef NAN
				return NAN;
			#else
				return 0;
			#endif
		}
	}

	/* The x-, y-, and z-vals to conduct 2-D linear interpolation between */
	double xvals[2] = {is2d.xcoords[x_bin], is2d.xcoords[x_bin + 1l]};
	double yvals[2] = {is2d.ycoords[y_bin], is2d.ycoords[y_bin + 1l]};
	double zvals[2][2] = {
		{is2d.zcoords[x_bin][y_bin], is2d.zcoords[x_bin][y_bin + 1l]},
		{is2d.zcoords[x_bin + 1l][y_bin], is2d.zcoords[x_bin + 1l][y_bin + 1l]}
	};

	return interpolate2D(xvals, yvals, zvals, x, y);

}

