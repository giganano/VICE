
#ifndef QUADRATURE_H 
#define QUADRATURE_H 

#ifdef __cplusplus 
extern "C" {
#endif 

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
 * source: quadrature.c 
 */
extern double *quad(double (*func)(double), double a, double b, 
	double tolerance, char *method, unsigned long Nmax, unsigned long Nmin); 

#ifdef __cplusplus 
} 
#endif 

#endif /* QUADRATURE_H */ 


