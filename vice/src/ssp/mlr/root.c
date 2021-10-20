/*
 * This file implements a simple root-finding algorithm for the mass-lifetime
 * relations which do not allow analytic solutions. This algorithm is a
 * recursive implementation of the bisection method detailed in Chapter 9 of
 * Numerical Recipes by Press, Teukolsky, Vetterling & Flannery (2007).
 */

#include <stdio.h>
#include "../../ssp.h"
#include "../../utils.h"
#include "root.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double percent_difference(double actual, double test);


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
 * header: root.h
 */
extern double bisection(double (*func)(double, double, double), double lower,
	double upper, double time, double postMS, double Z) {

	/*
	 * In the bisection method, you start with an interval enclosing a root
	 * in the function. Then cut it in half and pick which interval encloses
	 * the root after splitting it in two. Repeat this process until you are
	 * within some reasonable tolerance of the real solution.
	 */

	double middle = (lower + upper) / 2;
	if (percent_difference(func(middle, postMS, Z), time) < SSP_TOLERANCE ||
		percent_difference(lower, upper) < SSP_TOLERANCE) {
		/* the base case -> solution has converged */
		return middle;
	} else {
		/* the recursive case -> solution has not yet converged. */
		double f_lower = func(lower, postMS, Z);
		double f_middle = func(middle, postMS, Z);
		double f_upper = func(upper, postMS, Z);

		if (sign(f_upper - time) == sign(f_lower - time)) {
			/*
			 * The root is not on the interval. In practice this likely means
			 * this function is being timed or tested and received a very small
			 * stellar age value, and if not then the turnoff mass is
			 * sufficiently above the relevant mass range for the parts of VICE
			 * that use this function. A large number can safely be returned
			 * in this instance.
			 */
			return 500;
		} else if (sign(f_lower - time) == sign(f_middle - time)) {
			/* the root is between middle and upper */
			return bisection(func, middle, upper, time, postMS, Z);
		} else if (sign(f_middle - time) == sign(f_upper - time)) {
			/* the root is between lower and middle */
			return bisection(func, lower, middle, time, postMS, Z);
		} else {
			/*
			 * There has been an error. Return a dummy value for error
			 * handling.
			 */
			#ifdef NAN
				return NAN;
			#else
				return -1;
			#endif
		}

	}

}


/*
 * Compute the percent difference between an actual value and a test value.
 *
 * Parameters
 * ==========
 * actual: 		The "known" value
 * test: 		The test value, which is subject to change.
 */
static double percent_difference(double actual, double test) {

	return absval( (actual - test) / actual );

}

