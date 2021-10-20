
#ifndef TOOLKIT_INTERP_SCHEME_2D_H
#define TOOLKIT_INTERP_SCHEME_2D_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

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
 * source: interp_scheme_2d.c
 */
extern double interp_scheme_2d_evaluate(INTERP_SCHEME_2D is2d, double x,
	double y);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* INTERP_SCHEME_2D_H */

