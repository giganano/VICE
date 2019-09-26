/* 
 * This file implements the core routines of the polynomial object. 
 */ 

#include <stdlib.h> 
#include <math.h> 
#include "polynomial.h" 
#include "numparam.h" 

/* 
 * Allocate memory for an return a pointer to a polynomial object. 
 * 
 * Parameters 
 * ========== 
 * n: 		The order of the polynomial 
 * 
 * header: polynomial.h 
 */ 
extern POLYNOMIAL *polynomial_initialize(unsigned short n) {

	POLYNOMIAL *poly = (POLYNOMIAL *) malloc (sizeof(POLYNOMIAL)); 
	poly -> order = n; 
	poly -> coeffs = (NUMPARAM **) malloc ((unsigned) (n + 1) * 
		sizeof(NUMPARAM *)); 
	return poly; 
} 

/* 
 * Free up the memory stored in a polynomial object. 
 * 
 * header: polynomial.h 
 */ 
extern void polynomial_free(POLYNOMIAL *poly) {

	if (poly != NULL) {

		#if 0
		if ((*poly).coeffs != NULL) {
			unsigned short i; 
			for (i = 0; i <= (*poly).order; i++) {
				if ((*poly).coeffs[i] != NULL) {
					numparam_free(poly -> coeffs[i]); 
					poly -> coeffs[i] = NULL; 
				} else {} 
			} 
			free(poly -> coeffs); 
			poly -> coeffs = NULL; 
		} else {} 
		#endif 

		free(poly); 
		poly = NULL; 

	} else {} 

} 

/* 
 * Evaluate the polynomial f(x) for a given value of x. 
 * 
 * Parameters 
 * ========== 
 * poly: 		The polynomial object 
 * x: 			The value of x to evaluate at 
 * 
 * Returns 
 * ======= 
 * The value of f(x) 
 * 
 * header: polynomial.h 
 */ 
extern double polynomial_evaluate(POLYNOMIAL poly, double x) {

	double f_of_x = 0.0; 
	unsigned short i; 
	for (i = 0; i <= poly.order; i++) {
		f_of_x += (*poly.coeffs[i]).current * pow(x, i); 
	} 
	return f_of_x; 

} 


