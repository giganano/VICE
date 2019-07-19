/* 
 * This file implements gaussian quadrature for the numerical evaluation of 
 * integrals. 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include "quadrature.h" 
#include "utils.h" 

/* ---------- static function comment headers not duplicated here ---------- */
static double euler(double (*func)(double), double a, double b, 
	unsigned long N);
static double trapzd(double (*func)(double), double a, double b, 
	unsigned long N);
static double midpt(double (*func)(double), double a, double b, 
	unsigned long N);
static double simp(double (*func)(double), double a, double b, 
	unsigned long N); 
static double absval(double x); 
static int sign(double x); 

/*
 * Evaluate an integral from a to b numerically using quadrature 
 * 
 * Parameters 
 * ========== 
 * func:		The function to integrate
 * a:			The lower bound of integration
 * b:			The upper bound of integration
 * tolerance:	The maximum allowed fractional yield
 * method:		The method of quadrature to use
 * Nmax:		Maximum number of bins (safeguard against divergent solns)
 * Nmin:		Minimum number of bins 
 * 
 * Returns 
 * ======= 
 * A 3-element array
 * returned[0]:		The estimated value of the integral
 * returned[1]:		The estimated fractional error
 * returned[2]:		The number of iterations it took to the get there 
 * NULL in the case of an unrecognized method of integration 
 * 
 * Notes & References 
 * ================== 
 * The methods of numerical quadrature implemented in this function and its 
 * subroutines are adopted from Chapter 4 of Numerical Recipes (Press, 
 * Teukolsky, Vetterling & Flannery 2007), Cambridge University Press. 
 * 
 * header: quadrature.h 
 */
extern double *quad(double (*func)(double), double a, double b, 
	double tolerance, char *method, unsigned long Nmax, unsigned long Nmin) {

	unsigned long N = Nmin / 2l; 	// Start with half the specified minimum 
	if (N % 2l != 0l) {				// Make the number of quadrature bins even 
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
			return NULL; 
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
 * Parameters 
 * ========== 
 * func: 		A pointer to the function to integrate 
 * a: 			The lower bound of the integral 
 * b: 			The upper bound of the integral 
 * N: 			The number of bins to use in evaluating the Riemann sum 
 * 
 * Returns 
 * ======= 
 * The approximate value of the integral with the given number of bins 
 * 
 * For details on Euler's method, see chapter 4 of Numerical Recipes: 
 * Press, Teukolsky, Vetterling, & Flannery (2007), Cambridge University Press 
 */ 
static double euler(double (*func)(double), double a, double b, 
	unsigned long N) {

	double hN = (b - a) / N;		// The width of the bins 
	/* Euler's method uses only the left edge of the bins */ 
	double *x = binspace(a, b - hN, N - 1l);	
	double *eval = (double *) malloc (N * sizeof(double));
	unsigned long i;

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
 * Parameters  
 * ========== 
 * func: 		A pointer to the function to integrate 
 * a: 			The lower bound of the integral 
 * b: 			The upper bound of the integral 
 * N: 			The number of bins to use in evaluating the Riemann sum 
 * 
 * Returns 
 * ======= 
 * The approximate value of the integral with the given number of bins 
 * 
 * For details on the Trapezoid rule, see chapter 4 of Numerical Recipes: 
 * Press, Teukolsky, Vetterling, & Flannery (2007), Cambridge University Press 
 */ 
static double trapzd(double (*func)(double), double a, double b, 
	unsigned long N) {

	double hN = (b - a) / N;		// The width of each bin 
	double *x = binspace(a, b, N);
	double *eval = (double *) malloc ((N + 1l) * sizeof(double));
	unsigned long i;

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
 * Parameters 
 * ========== 
 * func: 		A pointer to the function to integrate 
 * a: 			The lower bound of the integral 
 * b: 			The upper bound of the integral 
 * N: 			The number of bins to use in evaluating the Riemann sum 
 * 
 * Returns 
 * ======= 
 * The approximate value of the integral with the given number of bins 
 * 
 * For details on the Midpoint rule, see chapter 4 of Numerical Recipes: 
 * Press, Teukolsky, Vetterling, & Flannery (2007), Cambridge University Press 
 */ 
static double midpt(double (*func)(double), double a, double b, 
	unsigned long N) {

	double hN = (b - a) / N;		// The width of each bin 
	double *x = binspace(a, b, N);
	double *mids = bin_centers(x, N); // Midpoint rule evaluates at bin centers 
	double *eval = (double *) malloc (N * sizeof(double));
	unsigned long i;

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
 * Parameters 
 * ========== 
 * func: 		A pointer to the function to integrate 
 * a: 			The lower bound of the integral 
 * b: 			The upper bound of the integral 
 * N: 			The number of bins to use in evaluating the Riemann sum 
 * 
 * Returns 
 * ======= 
 * The approximate value of the integral with the given number of bins 
 * 
 * For details on Simpson's rule, see chapter 4 of Numerical Recipes: 
 * Press, Teukolsky, Vetterling, & Flannery (2007), Cambridge University Press 
 */ 
static double simp(double (*func)(double), double a, double b, 
	unsigned long N) {

	/* Simpson's rule is essentially a complication of Trapezoid rule */ 
	return (4 * trapzd(func, a, b, N) - trapzd(func, a, b, N/2l)) / 3;

}

/* 
 * Determine the absolute value of a double x. This function extends the 
 * standard library function abs, which only excepts values of type int. 
 * 
 * Parameters 
 * ========== 
 * x: 		The number to determine the absolute value of 
 * 
 * Returns 
 * ======= 
 * +x if x >= 0, -x if x < 0 
 */ 
static double absval(double x) {

	return sign(x) * x; 

}

/* 
 * Determine the sign of a double x 
 * 
 * Parameters 
 * ========== 
 * x: 		The value to determine the sign of 
 * 
 * Returns 
 * ======= 
 * +1 if x >= 0, -1 if x < 0 
 */ 
static int sign(double x) {

	return (x >= 0) - (x < 0); 

} 



