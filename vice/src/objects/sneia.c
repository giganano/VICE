/* 
 * This file implements memory management for the SNEIA_YIELD_SPECS object. 
 */ 

#include <stdlib.h> 
#include "../sneia.h" 
#include "objects.h" 
#include "sneia.h" 


/* 
 * Allocate memory for and return a pointer to a SNEIA_YIELD_SPECS struct. 
 * Automatically initializes RIa and yield_ to NULL. Allocates memory for a 
 * 100-character dtd char * specifier. 
 * 
 * header: sneia.h 
 */ 
extern SNEIA_YIELD_SPECS *sneia_yield_initialize(void) {

	SNEIA_YIELD_SPECS *sneia_yields = (SNEIA_YIELD_SPECS *) malloc (sizeof(
		SNEIA_YIELD_SPECS)); 
	sneia_yields -> dtd = (char *) malloc (100 * sizeof(char)); 
	sneia_yields -> RIa = NULL; 

	sneia_yields -> yield_ = NULL; 

	/* 
	 * The number of elements on the yield grid between IA_YIELD_GRID_MIN and 
	 * IA_YIELD_GRID_MAX in steps of IA_YIELD_STEP (inclusve). 
	 */ 
	unsigned long num_grid_elements = (long) (
		(IA_YIELD_GRID_MAX - IA_YIELD_GRID_MIN) / IA_YIELD_STEP 
	) + 1l; 

	/* Fill the grid starting at IA_YIELD_GRID_MIN in steps of IA_YIELD_STEP */ 
	unsigned long i; 
	sneia_yields -> grid = (double *) malloc (num_grid_elements * sizeof(double)); 
	for (i = 0l; i < num_grid_elements; i++) {
		sneia_yields -> grid[i] = IA_YIELD_GRID_MIN + i * IA_YIELD_STEP; 
	} 

	sneia_yields -> entrainment = 1; 

	return sneia_yields; 

} 


/* 
 * Free up the memory stored in a SNEIA_YIELD_SPECS struct. 
 * 
 * header: sneia.h 
 */ 
extern void sneia_yield_free(SNEIA_YIELD_SPECS *sneia_yields) { 

	if (sneia_yields != NULL) {

		if ((*sneia_yields).RIa != NULL) {
			free(sneia_yields -> RIa); 
			sneia_yields -> RIa = NULL; 
		} else {} 

		if ((*sneia_yields).dtd != NULL) {
			free(sneia_yields -> dtd); 
			sneia_yields -> dtd = NULL; 
		} else {} 

		if ((*sneia_yields).yield_ != NULL) {
			free(sneia_yields -> yield_); 
			sneia_yields -> yield_ = NULL; 
		} else {} 

		if ((*sneia_yields).grid != NULL) {
			free(sneia_yields -> grid); 
			sneia_yields -> grid = NULL; 
		} else {} 

		free(sneia_yields); 
		sneia_yields = NULL; 

	} else {} 

} 

