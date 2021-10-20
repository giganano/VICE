/*
 * This file implements the core routines of the interp_scheme_1d object.
 */

#include <math.h>
#include "interp_scheme_1d.h"
#include "../utils.h"


/*
 * Evaluate an interp_scheme_1d object at some value of the x-coordinate.
 *
 * Parameters
 * ==========
 * is1d: 		The interp_scheme_1d object to evaluate as a function.
 * x: 			The value of the x-coordinate to evaluate at.
 *
 * Returns
 * =======
 * is1d(x), the value fo the function f(x) approximated via linear interpolation
 * off the known (x, y) values of the interpolation scheme.
 *
 * header: interp_scheme_1d.h
 */
extern double interp_scheme_1d_evaluate(INTERP_SCHEME_1D is1d, double x) {

	long bin = get_bin_number(is1d.xcoords, is1d.n_points - 1ul, x);
	if (bin == -1l) {
		/*
		 * The x-coordinate is either larger than the largest x-coordinate or
		 * smaller than the smallest one.
		 */
		if (x < is1d.xcoords[0]) {
			bin = 0ul;
		} else if (x > is1d.xcoords[is1d.n_points - 1ul]) {
			bin = (long) is1d.n_points - 2l;
		} else {
			/* error handling for manylinux1 distribution */
			#ifdef NAN
				return NAN;
			#else
				return 0;
			#endif
		}
	}

	return interpolate(is1d.xcoords[bin], is1d.xcoords[bin + 1l],
		is1d.ycoords[bin], is1d.ycoords[bin + 1l], x);

}

