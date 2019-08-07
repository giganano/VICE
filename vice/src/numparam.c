/* 
 * This file implements the routines associated with the numparam object. 
 */ 

#include <stdlib.h> 
#include "numparam.h" 
#include "stats.h" 

/* 
 * Allocates memory for an returns a pointer to a numparam object. 
 * 
 * Parameters 
 * ========== 
 * start: The value to start the markov chain at 
 * let_vary: The boolean int describing whether or not this numparam object is 
 * 		being fitted. 
 * 
 * header: numparam.h 
 */ 
extern NUMPARAM *numparam_initialize(double start, unsigned short let_vary) {

	NUMPARAM *p = (NUMPARAM *) malloc (sizeof(NUMPARAM)); 
	p -> varies = let_vary; 
	p -> stepsize = 0.1; 
	p -> current = start; 
	return p; 

} 

/* 
 * Frees up the memory stored in a numparam object. 
 * 
 * header: numparam.h 
 */ 
extern void numparam_free(NUMPARAM *p) {

	if (p != NULL) {

		#if 0 
		if ((*p).value != NULL) {
			free(p -> value); 
			p -> value = NULL; 
		} else {} 
		#endif 

		free(p); 
		p = NULL; 

	} else {} 

} 

/* 
 * Update the current value of the numerical parameter by one step via a 
 * psuedo-randomly generated number with a normal distribution 
 * 
 * Parameters 
 * ========== 
 * p: 		A pointer to the numparam object 
 * 
 * header: numparam.h 
 */ 
extern void numparam_step(NUMPARAM *p) { 

	if ((*p).varies) p -> current = normal((*p).current, (*p).stepsize); 

}



