/*
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
*/

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "cc_yields.h"

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
Evaluate an integral from a to b numerically using quadrature 

Args:
=====
func:		The function to integrate
a:			The lower bound of integration
b:			The upper bound of integration
tolerance:	The maximum allowed fractional yield
method:		The method of quadrature to use
Nmax:		Maximum number of bins (safeguard against divergent solns)
Nmin:		Minimum number of bins

Returns:
========
A 3-element array
returned[0]:		The estimated value of the integral
returned[1]:		The estimated fractional error
returned[2]:		The number of iterations it took to the get there
*/
extern double *quad(double (*func)(double), double a, double b, 
	double tolerance, char *method, long Nmax, long Nmin) {

	long N = Nmin / 2l;
	if (N % 2l != 0l) {
		N += 1l;
	} else {}

	double old_int = 0;
	double new_int;
	double error;
	do {
		if (!strcmp(method, "euler")) {
			new_int = euler(func, a, b, N);
		} else if (!strcmp(method, "trapezoid")) {
			new_int = trapzd(func, a, b, N);
		} else if (!strcmp(method, "midpoint")) {
			new_int = midpt(func, a, b, N);
		} else if (!strcmp(method, "simpson")) {
			new_int = simp(func, a, b, N);
		} else {
			printf("ERROR in IMF-INTEGRATOR. Please submit bug report to ");
			printf("giganano9@gmail.com.\n");
			exit(0);
		}
		if (new_int == 0) {
			error = 1;
		} else {
			error = absval(old_int / new_int - 1);
		}
		old_int = new_int;
		N *= 2l;
	} while (error > tolerance && N < Nmax);
	double *results = (double *) malloc (3 * sizeof(double));
	results[0] = new_int;
	results[1] = error;
	results[2] = N;
	return results;

}

/*
Approximates the integral of func from a to b using Euler's method with N 
steps.
*/
static double euler(double (*func)(double), double a, double b, long N) {

	double hN = (b - a) / N;
	double *x = binspace(a, b - hN, N - 1l);
	double *eval = (double *) malloc (N * sizeof(double));
	long i;
	for (i = 0l; i < N; i++) {
		eval[i] = func(x[i]);
	}
	double total = sum(eval, N);
	free(eval);
	free(x);
	return hN * total;

}

/*
Approximates the integral of func from a to b using trapezoid rule with N 
steps.
*/
static double trapzd(double (*func)(double), double a, double b, long N) {

	double hN = (b - a) / N;
	double *x = binspace(a, b, N);
	double *eval = (double *) malloc ((N + 1l) * sizeof(double));
	long i;
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
Approximates the integral of func from a to b using midpoint rule with N 
steps.
*/
static double midpt(double (*func)(double), double a, double b, long N) {

	double hN = (b - a) / N;
	double *x = binspace(a, b, N);
	double *mids = bin_centers(x, N);
	double *eval = (double *) malloc (N * sizeof(double));
	long i;
	for (i = 0l; i < N; i++) {
		eval[i] = func(mids[i]);
	}
	double total = sum(eval, N + 1l);
	free(x);
	free(mids);
	free(eval);
	return hN * total;

}

/*
Approximates the integral of func from a to b using Simpson's Rule with N 
steps.
*/
static double simp(double (*func)(double), double a, double b, long N) {

	return (4 * trapzd(func, a, b, N) - trapzd(func, a, b, N/2l)) / 3;

}

/*
Returns a pointer to an array of linearly spaced doubles between 
start and stop with N bins. The returned array is of length N + 1l
*/
static double *binspace(double start, double stop, long N) {

	double *arr = (double *) malloc ((N + 1l) * sizeof(double));
	double dx = (stop - start) / N;
	long i;
	for (i = 0l; i <= N; i++) {
		arr[i] = start + i * dx;
	}
	return arr;

}

static double *bin_centers(double *edges, long num_bins) {

	double *out = (double *) malloc (num_bins * sizeof(double));
	long i;
	for (i = 0l; i < num_bins; i++) {
		out[i] = (edges[i] + edges[i + 1l]) / 2.0;
	}
	return out;

}

/*
Returns the sum of an array of doubles arr with length len
*/
static double sum(double *arr, long len) {

	double s = 0;
	long i;
	for (i = 0l; i < len; i++) {
		s += arr[i];
	}
	return s;

}

/* Returns the absolute value of val */
static double absval(double val) {

	return sign(val) * val;

}

/* Returns the sign of val as +/- 1 and zero at 0 */
static double sign(double val) {

	return (val >= 0) - (val <= 0);

}



