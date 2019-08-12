
#ifndef NUMPARAM_H 
#define NUMPARAM_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#include "objects.h" 

/* 
 * Allocates memory for an returns a pointer to a numparam object. 
 * 
 * Parameters 
 * ========== 
 * start: The value to start the markov chain at 
 * let_vary: The boolean int describing whether or not this numparam object is 
 * 		being fitted. 
 * 
 * source: numparam.c 
 */ 
extern NUMPARAM *numparam_initialize(double start, unsigned short let_vary); 

/* 
 * Frees up the memory stored in a numparam object. 
 * 
 * source: numparam.c 
 */ 
extern void numparam_free(NUMPARAM *p); 

/* 
 * Update the current value of the numerical parameter by one step via a 
 * psuedo-randomly generated number with a normal distribution 
 * 
 * Parameters 
 * ========== 
 * p: 		A pointer to the numparam object 
 * 
 * source: numparam.c 
 */ 
extern void numparam_step(NUMPARAM *p); 

/* 
 * Prints the address of a numparam pointer 
 * 
 * source: numparams.c 
 */ 
extern void numparam_address(NUMPARAM *p); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* NUMPARAM_H */ 


