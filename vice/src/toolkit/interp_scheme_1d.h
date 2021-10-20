
#ifndef TOOLKIT_INTERP_SCHEME_1D_H
#define TOOLKIT_INTERP_SCHEME_1D_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

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
 * source: interp_scheme_1d.c
 */
extern double interp_scheme_1d_evaluate(INTERP_SCHEME_1D is1d, double x);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TOOLKIT_INTERP_SCHEME_1D_H */
