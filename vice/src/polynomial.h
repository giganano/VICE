
#ifndef POLYNOMIAL_H 
#define POLYNOMIAL_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#include "objects.h" 

/* 
 * Allocate memory for an return a pointer to a polynomial object. 
 * 
 * Parameters 
 * ========== 
 * n: 		The order of the polynomial 
 * 
 * source: polynomial.c 
 */ 
extern POLYNOMIAL *polynomial_initialize(unsigned short n); 

/* 
 * Free up the memory stored in a polynomial object. 
 * 
 * source: polynomial.c 
 */ 
extern void polynomial_free(POLYNOMIAL *poly); 

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
 * source: polynomial.c 
 */ 
extern double polynomial_evaluate(POLYNOMIAL poly, double x); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* POLYNOMIAL_H */ 

