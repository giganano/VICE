/* 
 * This file imlements the memory manangement for the CCSNE_YIELD_SEPCS 
 * object. 
 */ 

#include <stdlib.h> 
#include "../ccsne.h" 
#include "objects.h" 
#include "ccsne.h" 

/* 
 * Allocate memory for and return a pointer to a CCSNE_YIELD_SPECS struct. 
 * This also allocates memory for the grid of metallicities and automatically 
 * fills it with the grid defined by CC_YIELD_GRID_MIN, CC_YIELD_GRID_MAX, 
 * and CC_YIELD_STEP as defined in ccsne.h. Initializes the yield_ value to 
 * NULL. 
 * 
 * header: ccsne.h 
 */ 
extern CCSNE_YIELD_SPECS *ccsne_yield_initialize(void) {

	CCSNE_YIELD_SPECS *ccsne_yield = (CCSNE_YIELD_SPECS *) malloc (sizeof(
		CCSNE_YIELD_SPECS)); 

	ccsne_yield -> yield_ = NULL; 

	/* 
	 * The number of elements on the yield grid between CC_YIELD_GRID_MIN and 
	 * CC_YIELD_GRID_MAX in steps of CC_YIELD_STEP (inclusive). 
	 */ 
	unsigned long num_grid_elements = (long) (
		(CC_YIELD_GRID_MAX - CC_YIELD_GRID_MIN) / CC_YIELD_STEP
	) + 1l; 

	/* Fill the grid starting at CC_YIELD_GRID_MIN in steps of CC_YIELD_STEP */ 
	unsigned long i; 
	ccsne_yield -> grid = (double *) malloc (num_grid_elements * sizeof(double)); 
	for (i = 0l; i < num_grid_elements; i++) {
		ccsne_yield -> grid[i] = CC_YIELD_GRID_MIN + i * CC_YIELD_STEP; 
	} 

	ccsne_yield -> entrainment = 1; 

	return ccsne_yield; 

} 

/* 
 * Free up the memory stored in a CCSNE_YIELD_SPECS struct 
 * 
 * header: ccsne.h 
 */ 
extern void ccsne_yield_free(CCSNE_YIELD_SPECS *ccsne_yield) { 

	if (ccsne_yield != NULL) {

		if ((*ccsne_yield).yield_ != NULL) {
			free(ccsne_yield -> yield_); 
			ccsne_yield -> yield_ = NULL; 
		} else {} 

		if ((*ccsne_yield).grid != NULL) {
			free(ccsne_yield -> grid); 
			ccsne_yield -> grid = NULL; 
		} else {} 

		free(ccsne_yield); 
		ccsne_yield = NULL; 

	} else {} 

} 

