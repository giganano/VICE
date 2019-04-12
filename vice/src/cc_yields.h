/*
 * This file, included with the VICE package, is protected under the terms of 
 * the associated MIT License, and any use or redistribution of this file in 
 * original or altered form is subject to the copyright terms therein. 
 * 
 * This script contains extern declarations for routines used in the numerical 
 * integration of elemental yields from core-collapse supernovae.  
 */

#ifndef CC_YIELDS_H
#define CC_YIELDS_H

/*
 * Returns the yield-weighted integrated IMF 
 * 
 * Args:
 * =====
 * file:		The nme of the data file containing the grid
 * IMF:			The IMF to use ('kroupa' or 'salpeter')
 * lower:		The lower mass limit on star formation in units of Msun
 * upper:		The upper mass limit on star formation in units of Msun
 * tolerance:	The maximum fractional error to allow
 * method:		The method of quadrature to use
 * Nmax:		Maximum number of bins (safeguard against divergent solns)
 * Nmin:		Minimum number of bins
 * 
 * source: cc_yield.c 
 */
extern double *numerator(char *file, char *IMF, double lower, double upper, 
	double tolerance, char *method, long Nmax, long Nmin);

/*
 * Returns the mass-weighted integrated IMF 
 * 
 * Args:
 * =====
 * IMF:			The IMF to use ('kroupa' or 'salpeter')
 * lower:		The lower mass limit on star formation in units of Msun
 * upper:		The upper mass limit on star formation in units of Msun
 * tolerance:	The maximum fractional error to allow
 * method:		The method of quadrature to use
 * Nmax:		Maximum number of bins (safeguard against divergent solns)
 * Nmin:		Minimum number of bins
 * 
 * source: cc_yield.c 
 */
extern double *denominator(char *IMF, double lower, double upper, 
	double tolerance, char *method, long Nmax, long Nmin);

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
 * source: quadrature.c  
 */
extern double *quad(double (*func)(double), double a, double b, 
	double tolerance, char *method, long Nmax, long Nmin);

/* 
 * The Salpeter IMF as a function of mass, up to a normalization constant. 
 * 
 * Args:
 * =====
 * m:			The stellar mass in Msun
 * 
 * source: imf.c  
 */
extern double salpeter(double m);

/* 
 * The Kroupa IMF as a function of mass, up to a normalization constant 
 * 
 * Args:
 * =====
 * m:			The stellar mass in Msun 
 * 
 * source: imf.c 
 */
extern double kroupa(double m);

#endif /* CC_YIELDS_H */

