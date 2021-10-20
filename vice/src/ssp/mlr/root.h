
#ifndef SSP_MLR_ROOT_H
#define SSP_MLR_ROOT_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#ifndef BISECTION_INITIAL_LOWER_BOUND
#define BISECTION_INITIAL_LOWER_BOUND 1E-3
#endif /* BISECTION_INITIAL_LOWER_BOUND */

#ifndef BISECTION_INITIAL_UPPER_BOUND
#define BISECTION_INITIAL_UPPER_BOUND 1E+3
#endif /* BISECTION_INITIAL_UPPER_BOUND */

#include "../../objects.h"

/*
 * Compute the root of a mass-lifetime relation according to the bisection
 * method outlined in Chapter 9 of Press, Teukolsky, Vetterling & Flannery
 * (2007).
 *
 * Parameters
 * ==========
 * func: 		The functional form of the mass-lifetime relation.
 * lower: 		The lower bound of the interval containing the root.
 * upper: 		The upper bound of the interval containing the root.
 * time: 		The lifetime of a star whose mass is to be calculated.
 * postMS: 		The ratio of a star's post main sequence lifetime to its main
 * 				sequence lifetime. 0 for the true main sequence turnoff mass.
 * 				The second parameter to func.
 * Z: 			The metallicity by mass of the stellar population. The third
 * 				parameter to func.
 *
 * Returns
 * =======
 * The root of the mass-lifetime relation in solar masses within a percent
 * difference of 10^-4 (declared in source file).
 *
 * Notes
 * =====
 * Although the mass-lifetime relation is uni-dimensional at a given
 * metallicity, the functions as implemented require three parameters to
 * account for post main sequence lifetimes and metallicity in addition to
 * stellar mass.
 *
 * References
 * ==========
 * Press, Teukolsky, Vetterling & Flannery (2007), Numerical Recipes, Cambridge
 * University Press
 *
 * source: root.c
 */
extern double bisection(double (*func)(double, double, double), double lower,
	double upper, double time, double postMS, double Z);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SSP_MLR_ROOT_H */
