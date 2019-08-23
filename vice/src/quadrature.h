
#ifndef QUADRATURE_H 
#define QUADRATURE_H 

#ifdef __cplusplus 
extern "C" {
#endif 

/* hash-code for euler's method */ 
#ifndef EULER 
#define EULER 541 
#endif /* EULER */ 

/* hash-code for trapezoid rule */ 
#ifndef TRAPEZOID 
#define TRAPEZOID 978 
#endif /* TRAPEZOID */ 

/* hash-code for midpoint rule */ 
#ifndef MIDPOINT 
#define MIDPOINT 868 
#endif /* MIDPOINT */ 

/* hash-code for simpson's rule */ 
#ifndef SIMPSON 
#define SIMPSON 777 
#endif /* SIMPSON */ 

#ifndef MAX_METHOD_SIZE 
#define MAX_METHOD_SIZE 100l 
#endif /* MAX_METHOD_SIZE */ 

#include "objects.h" 

/* 
 * Allocate memory for and return a pointer to an integral object. 
 * 
 * source: integral.c 
 */ 
extern INTEGRAL *integral_initialize(void); 

/* 
 * Free up the memory stored in the integral object. 
 * 
 * source: quadrature.c 
 */ 
extern void integral_free(INTEGRAL *intgrl); 

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
 * source: quadrature.c 
 */
extern unsigned short quad(INTEGRAL *intgrl); 

#ifdef __cplusplus 
} 
#endif 

#endif /* QUADRATURE_H */ 


