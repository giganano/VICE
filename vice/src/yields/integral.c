/*
 * This file implements gaussian quadrature for the numerical evaluation of
 * integrals.
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "../yields.h"
#include "../utils.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double euler(INTEGRAL intgrl, unsigned long N);
static double trapzd(INTEGRAL intgrl, unsigned long N);
static double midpt(INTEGRAL intgrl, unsigned long N);
static double simp(INTEGRAL intgrl, unsigned long N);


/*
 * Evaluate an integral from a to b numerically using quadrature
 *
 * Parameters
 * ==========
 * intgrl: 		The integral object
 *
 * Returns
 * =======
 * 0 on success, 1 on an error larger than the tolerance, and 2 on an
 * unrecognized evaluation method
 *
 * Notes & References
 * ==================
 * The methods of numerical quadrature implemented in this function and its
 * subroutines are adopted from Chapter 4 of Numerical Recipes (Press,
 * Teukolsky, Vetterling & Flannery 2007), Cambridge University Press.
 *
 * header: integral.h
 */
extern unsigned short quad(INTEGRAL *intgrl) {

	/*
	 * The integral is measured using Riemann sums. The algorithm implemented
	 * here measures the integral for a given numer of bins, then doubles the
	 * number of bins and measures the error from the fractional difference
	 * between the two integrations. The numerical value of the integral is
	 * then said to converge when the error falls below the specified
	 * tolerance.
	 *
	 * Start with half the specified minimum b/c there will always be at least
	 * two iterations. Ensure that the number of bins is even.
	 */

	unsigned long N = (*intgrl).Nmin / 2l;
	if (N % 2l != 0l) N += 1l;

	double (*integrate)(INTEGRAL, unsigned long);
	double old_int = 0;
	double new_int;


	switch ((*intgrl).method) {

		case EULER:
			/* integrate according to Euler's method */
			integrate = &euler;
			break;

		case TRAPEZOID:
			/* integrate according to Trapezoid rule */
			integrate = &trapzd;
			break;

		case MIDPOINT:
			/* integrate according to midpoint rule */
			integrate = &midpt;
			break;

		case SIMPSON:
			/* integrate according to Simpson's rule */
			integrate = &simp;
			break;

		default:
			/* error handling */
			return 2;

	}

	do {

		new_int = integrate(*intgrl, N);
		if (new_int) {
			intgrl -> error = absval(old_int / new_int - 1);
		} else {
			/*
			 * If the integral evaluates to zero, we can't estimate an error
			 * given the algorithm implemented here
			 */
			intgrl -> error = 1;
		}

		/* Store previous value and increment N */
		old_int = new_int;
		N *= 2l;

	} while ((*intgrl).error > (*intgrl).tolerance && N < (*intgrl).Nmax);

	intgrl -> result = new_int;
	intgrl -> iters = N;
	return ((*intgrl).error > (*intgrl).tolerance);

}


/*
 * Approximates the integral of a function between two bounds using Euler's
 * method with a given number of bins.
 *
 * Parameters
 * ==========
 * integrl: 	The integral object
 * N: 			The number of bins to use in evaluating the Riemann sum
 *
 * Returns
 * =======
 * The approximate value of the integral with the given number of bins
 *
 * For details on Euler's method, see chapter 4 of Numerical Recipes:
 * Press, Teukolsky, Vetterling, & Flannery (2007), Cambridge University Press
 */
static double euler(INTEGRAL intgrl, unsigned long N) {

	double hN = (intgrl.b - intgrl.a) / N; /* the width of the bins */
	/* Euler's method uses only the left edge of each bin */
	double *x = binspace(intgrl.a, intgrl.b - hN, N - 1l);
	double *eval = (double *) malloc (N * sizeof(double));

	/*
	 * Evaluate the function at each bin edge, add it up, multiply by the
	 * bin width and return
	 */
	unsigned long i;
	for (i = 0l; i < N; i++) {
		eval[i] = intgrl.func(x[i]);
	}
	double total = sum(eval, N);
	free(eval);
	free(x);
	return hN * total;

}


/*
 * Approximates the integral of a function between two bounds using the
 * Trapezoid rule with a given number of bins.
 *
 * Parameters
 * ==========
 * intgrl: 		The integral object
 * N: 			The number of bins to use in evaluating the Riemann sum
 *
 * Returns
 * =======
 * The approximate value of the integral with the given number of bins
 *
 * For details on the Trapezoid rule, see chapter 4 of Numerical Recipes:
 * Press, Teukolsky, Vetterling, & Flannery (2007), Cambridge University Press
 */
static double trapzd(INTEGRAL intgrl, unsigned long N) {

	double hN = (intgrl.b - intgrl.a) / N; /* width of each bin */
	double *x = binspace(intgrl.a, intgrl.b, N);
	double *eval = (double *) malloc ((N + 1l) * sizeof(double));

	/*
	 * Evaluate the function at each bin edge, and add everything up. According
	 * to trapezoid rule, subtract half of the value of the function at the
	 * first and last bin edges, then multiply by the width and return
	 */
	unsigned long i;
	for (i = 0l; i <= N; i++) {
		eval[i] = intgrl.func(x[i]);
	}
	double total = sum(eval, N + 1l);
	total -= 0.5 * (eval[0] + eval[N]);
	free(x);
	free(eval);
	return hN * total;

}


/*
 * Approximates the integral of a function between two bounds using the Midpoint
 * rule with a given number of bins.
 *
 * Parameters
 * ==========
 * intgrl: 		The integral object
 * N: 			The number of bins to use in evaluating the Riemann sum
 *
 * Returns
 * =======
 * The approximate value of the integral with the given number of bins
 *
 * For details on the Midpoint rule, see chapter 4 of Numerical Recipes:
 * Press, Teukolsky, Vetterling, & Flannery (2007), Cambridge University Press
 */
static double midpt(INTEGRAL intgrl, unsigned long N) {

	double hN = (intgrl.b - intgrl.a) / N; 	/* width of each bin */
	double *x = binspace(intgrl.a, intgrl.b, N);
	double *mids = bin_centers(x, N);
	double *eval = (double *) malloc (N * sizeof(double));

	/*
	 * Evaluate the function at the bin centers, add everything up, then
	 * multiply by the width and return
	 */
	unsigned long i;
	for (i = 0l; i < N; i++) {
		eval[i] = intgrl.func(mids[i]);
	}
	double total = sum(eval, N);
	free(x);
	free(mids);
	free(eval);
	return hN * total;

}


/*
 * Approximates the integral of a function between two bounds using Simpson's
 * rule with a given number of bins.
 *
 * Parameters
 * ==========
 * intgrl: 		The integral object
 * N: 			The number of bins to use in evaluating the Riemann sum
 *
 * Returns
 * =======
 * The approximate value of the integral with the given number of bins
 *
 * For details on Simpson's rule, see chapter 4 of Numerical Recipes:
 * Press, Teukolsky, Vetterling, & Flannery (2007), Cambridge University Press
 */
static double simp(INTEGRAL intgrl, unsigned long N) {

	/* Simpson's rule is essentially a complication of Trapezoid rule */
	return (4 * trapzd(intgrl, N) - trapzd(intgrl, N / 2l)) / 3;

}

