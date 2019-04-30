/*
 * This file, included with the VICE package, is protected under the terms of 
 * the associated MIT License, and any use or redistribution of this file in 
 * original or altered form is subject to the copyright terms therein. 
 * 
 * This script handles the numerical implementation of integration by quadrature 
 * for the functions which integrate mass yields of elements over an assumed 
 * IMF. 
 */ 

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "cc_yields.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double euler(double (*func)(double), double a, double b, long N);
static double trapzd(double (*func)(double), double a, double b, long N);
static double midpt(double (*func)(double), double a, double b, long N);
static double simp(double (*func)(double), double a, double b, long N);
static double *binspace(double start, double stop, long N);
static double *bin_centers(double *edges, long num_bins);
static double sum(double *arr, long len);
static double absval(double val);
static double sign(double val);

/*
 * Evaluate an integral from a to b numerically using quadrature 
 * 
 * Args:
 * =====
 * func:		The function to integrate
 * a:			The lower bound of integration
 * b:			The upper bound of integration
 * tolerance:	The maximum allowed fractional yield
 * method:		The method of quadrature to use
 * Nmax:		Maximum number of bins (safeguard against divergent solns)
 * Nmin:		Minimum number of bins 
 * 
 * Returns:
 * ========
 * A 3-element array
 * returned[0]:		The estimated value of the integral
 * returned[1]:		The estimated fractional error
 * returned[2]:		The number of iterations it took to the get there 
 * 
 * header: cc_yields.h 
 */
extern double *quad(double (*func)(double), double a, double b, 
	double tolerance, char *method, long Nmax, long Nmin) {

	long N = Nmin / 2l; 		// Start with half the specified minimum 
	if (N % 2l != 0l) {			// Make the number of quadrature bins even 
		N += 1l;
	} else {}

	/* 
	 * The integral is measured using Riemann sums. The algorithm implemented 
	 * here measures the integral for a given numer of bins, then doubles the 
	 * number of bins and measures the error from the fractional difference 
	 * between the two integrations. The numerical value of the integral is 
	 * then said to converge when the error falls below the specified 
	 * tolerance. 
	 */
	double old_int = 0;			
	double new_int;
	double error;
	do {
		if (!strcmp(method, "euler")) {
			/* Integrate according to Euler's method */ 
			new_int = euler(func, a, b, N);
		} else if (!strcmp(method, "trapezoid")) {
			/* Integrate according to Trapezoid rule */ 
			new_int = trapzd(func, a, b, N);
		} else if (!strcmp(method, "midpoint")) {
			/* Integrate according to midpoint rule */ 
			new_int = midpt(func, a, b, N);
		} else if (!strcmp(method, "simpson")) {
			/* Integrate according to Simpson's rule */ 
			new_int = simp(func, a, b, N);
		} else {
			/* This should be caught by Python anyway, included as a failsafe */ 
			printf("ERROR in IMF-INTEGRATOR. Please submit bug report to ");
			printf("giganano9@gmail.com.\n");
			exit(0);
		}
		if (new_int == 0) {
			/* 
			 * If the integral evaluates to zero, we can't estimate an error 
			 * given the algorithm implemented here 
			 */ 
			error = 1;
		} else {
			error = absval(old_int / new_int - 1);
		}
		/* Store the previously determined value of the integral and double N */ 
		old_int = new_int;
		N *= 2l;
		/* 
		 * Only evaluate while the error is larger than the tolerance and 
		 * the number of integrations is less than the specified maximum 
		 */ 
	} while (error > tolerance && N < Nmax);

	/* Return the results */ 
	double *results = (double *) malloc (3 * sizeof(double));
	results[0] = new_int;
	results[1] = error;
	results[2] = N;
	return results;

}

/* 
 * Approximates the integral of a function between two bounds using Euler's 
 * method with a given number of bins. 
 * 
 * Args: 
 * =====
 * func: 		A pointer to the function to integrate 
 * a: 			The lower bound of the integral 
 * b: 			The upper bound of the integral 
 * N: 			The number of bins to use in evaluating the Riemann sum 
 * 
 * For details on Euler's method, see chapter 4 of Numerical Recipes: 
 * Press, Teukolsky, Vetterling, & Flannery (2007), Cambridge University Press 
 */ 
static double euler(double (*func)(double), double a, double b, long N) {

	double hN = (b - a) / N;		// The width of the bins 
	/* Euler's method uses only the left edge of the bins */ 
	double *x = binspace(a, b - hN, N - 1l);	
	double *eval = (double *) malloc (N * sizeof(double));
	long i;

	/* 
	 * Evaluate the function at each bin edge, add it up, multiply by the 
	 * bin width and return 
	 */ 
	for (i = 0l; i < N; i++) {
		eval[i] = func(x[i]);
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
 * Args: 
 * =====
 * func: 		A pointer to the function to integrate 
 * a: 			The lower bound of the integral 
 * b: 			The upper bound of the integral 
 * N: 			The number of bins to use in evaluating the Riemann sum 
 * 
 * For details on the Trapezoid rule, see chapter 4 of Numerical Recipes: 
 * Press, Teukolsky, Vetterling, & Flannery (2007), Cambridge University Press 
 */ 
static double trapzd(double (*func)(double), double a, double b, long N) {

	double hN = (b - a) / N;		// The width of each bin 
	double *x = binspace(a, b, N);
	double *eval = (double *) malloc ((N + 1l) * sizeof(double));
	long i;

	/* 
	 * Evaluate the function at each bin edge, and add everything up. According 
	 * to trapezoid rule, subtract half of the value of the function at the 
	 * first and last bin edges, then multiply by the width and return 
	 */ 
	for (i = 0l; i <= N; i++) {
		eval[i] = func(x[i]);
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
 * Args: 
 * =====
 * func: 		A pointer to the function to integrate 
 * a: 			The lower bound of the integral 
 * b: 			The upper bound of the integral 
 * N: 			The number of bins to use in evaluating the Riemann sum 
 * 
 * For details on the Midpoint rule, see chapter 4 of Numerical Recipes: 
 * Press, Teukolsky, Vetterling, & Flannery (2007), Cambridge University Press 
 */ 
static double midpt(double (*func)(double), double a, double b, long N) {

	double hN = (b - a) / N;		// The width of each bin 
	double *x = binspace(a, b, N);
	double *mids = bin_centers(x, N); // Midpoint rule evaluates at bin centers 
	double *eval = (double *) malloc (N * sizeof(double));
	long i;

	/* 
	 * Evaluate the function at the bin centers, add everything up, then 
	 * multiply by the width and return 
	 */ 
	for (i = 0l; i < N; i++) {
		eval[i] = func(mids[i]);
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
 * Args: 
 * =====
 * func: 		A pointer to the function to integrate 
 * a: 			The lower bound of the integral 
 * b: 			The upper bound of the integral 
 * N: 			The number of bins to use in evaluating the Riemann sum 
 * 
 * For details on Simpson's rule, see chapter 4 of Numerical Recipes: 
 * Press, Teukolsky, Vetterling, & Flannery (2007), Cambridge University Press 
 */ 
static double simp(double (*func)(double), double a, double b, long N) {

	/* Simpson's rule is essentially a complication of Trapezoid rule */ 
	return (4 * trapzd(func, a, b, N) - trapzd(func, a, b, N/2l)) / 3;

}

/*
 * Returns a pointer to an array of linearly spaced doubles between two 
 * specified values. For a binspace with n bins, the resulting array is of 
 * length N + 1. 
 * 
 * Args: 
 * =====
 * start: 			The left-most bin edge
 * stop: 			The right-most bin edge 
 * N: 				The number of desired bins 
 */
static double *binspace(double start, double stop, long N) {

	/* Allocated memory and determine the bin width */ 
	double *arr = (double *) malloc ((N + 1l) * sizeof(double));
	double dx = (stop - start) / N;
	long i;
	for (i = 0l; i <= N; i++) {
		/* Incremenet each element forward based on the step size */ 
		arr[i] = start + i * dx;
	}
	return arr;

}

/* 
 * Determines the centers of each bin in a binspace by averaging adjacent 
 * elements. For a binspace of n bins (an array of length n + 1), the returned 
 * array will be of length n. 
 * 
 * Args:
 * =====
 * edges: 			The bin edges themselves 
 * num_bins: 		The number of bins in the bin-space
 * 					This is one less than the length of the array edges 
 */
static double *bin_centers(double *edges, long num_bins) {

	/* 
	 * Allocate memory and take the arithmetic mean of adjacent elements in 
	 * the array edges
	 */ 
	double *out = (double *) malloc (num_bins * sizeof(double));
	long i;
	for (i = 0l; i < num_bins; i++) {
		out[i] = (edges[i] + edges[i + 1l]) / 2.0;
	}
	return out;

}

/*
 * Returns the sum of an array of doubles with a given length 
 * 
 * Args:
 * =====
 * arr: 		A pointer to the array to sum 
 */ 
static double sum(double *arr, long len) {

	double s = 0;
	long i;
	for (i = 0l; i < len; i++) {
		s += arr[i];
	}
	return s;

}

/* 
 * Returns the absolute value of a given double precision number 
 * 
 * Args: 
 * =====
 * val: 		The number itself 
 */
static double absval(double val) {

	return sign(val) * val;

}

/* 
 * Returns -1 if a number if negative, 0 if it is 0, and +1 if it is positive 
 * 
 * Args: 
 * =====
 * val: 		The number itself 
 */
static double sign(double val) {

	return (val >= 0) - (val <= 0);

}



