/* 
 * This file implements the memory management for the CHANNEL object. 
 */ 

#include <stdlib.h> 
#include "../channel.h" 
#include "objects.h" 
#include "channel.h" 


/* 
 * Allocate memory for and return a pointer to a CHANNEL object. 
 * Automatically initializes yield_ and rate to NULL. Allocates memory for and 
 * fills the grid_. 
 * 
 * header: channel.h 
 */ 
extern CHANNEL *channel_initialize(void) {

	CHANNEL *ch = (CHANNEL *) malloc (sizeof(CHANNEL)); 
	ch -> yield_ = NULL; 
	ch -> rate = NULL; 

	/* 
	 * The number of metallicities on the grid between CHANNEL_YIELD_GRID_MIN 
	 * and CHANNEL_YIELD_GRID_MAX in steps of CHANNEL_YIELD_GRID_STEP 
	 * (inclusive) 
	 */ 
	unsigned long n_grid_elements = (long) (
		(CHANNEL_YIELD_GRID_MAX - CHANNEL_YIELD_GRID_MIN) / 
		CHANNEL_YIELD_GRID_STEP
	) + 1l; 

	/* 
	 * Fill the grid starting at CHANNEL_YIELD_GRID_MIN in steps of 
	 * CHANNEL_YIELD_GRID_STEP 
	 */ 
	unsigned long i; 
	ch -> grid = (double *) malloc (n_grid_elements * sizeof(double)); 
	for (i = 0l; i < n_grid_elements; i++) {
		ch -> grid[i] = CHANNEL_YIELD_GRID_MIN + i * CHANNEL_YIELD_GRID_STEP; 
	} 
	ch -> entrainment = 1; 

	return ch; 

} 


/* 
 * Free up the memory in a CHANNEL object. 
 * 
 * header: channel.h 
 */ 
extern void channel_free(CHANNEL *ch) {

	if (ch != NULL) {

		if ((*ch).yield_ != NULL) {
			free(ch -> yield_); 
			ch -> yield_ = NULL; 
		} else {} 

		if ((*ch).grid != NULL) {
			free(ch -> grid); 
			ch -> grid = NULL; 
		} else {} 

		if ((*ch).rate != NULL) {
			free(ch -> rate); 
			ch -> rate = NULL; 
		} else {} 

		free(ch); 
		ch = NULL; 

	} else {} 

} 

