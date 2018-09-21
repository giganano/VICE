
#ifndef CC_YIELDS_H
#define CC_YIELDS_H

/*
Returns the yield-weighted integrated IMF 

Args:
=====
file:		The nme of the data file containing the grid
IMF:		The IMF to use ('kroupa' or 'salpeter')
lower:		The lower mass limit on star formation in units of Msun
upper:		The upper mass limit on star formation in units of Msun
tolerance:	The maximum fractional error to allow
method:		The method of quadrature to use
Nmax:		Maximum number of bins (safeguard against divergent solns)
Nmin:		Minimum number of bins
*/
extern double *numerator(char *file, char *IMF, double lower, double upper, 
	double tolerance, char *method, long Nmax, long Nmin);

/*
Returns the mass-weighted integrated IMF 

Args:
=====
IMF:		The IMF to use ('kroupa' or 'salpeter')
lower:		The lower mass limit on star formation in units of Msun
upper:		The upper mass limit on star formation in units of Msun
tolerance:	The maximum fractional error to allow
method:		The method of quadrature to use
Nmax:		Maximum number of bins (safeguard against divergent solns)
Nmin:		Minimum number of bins
*/
extern double *denominator(char *IMF, double lower, double upper, 
	double tolerance, char *method, long Nmax, long Nmin);

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
	double tolerance, char *method, long Nmax, long Nmin);

/*
Pulls the total yields off of the data file and returns them as a 2-D array 
where the zeroth column is the masses and the first column is the total 
yields of all isotopes at that stellar mass. 

Args:
=====
The name of the file
*/
extern double **yields(char *file);

/* The Kroupa IMF as a function of mass, up to a normalization constant */
extern double kroupa(double m);

/* The Salpeter IMF as a function of mass, up to a normalization constant */
extern double salpeter(double m);

#endif /* CC_YIELDS_H */

