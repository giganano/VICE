/* 
 * This file implements the memory management for the AGB_YIELD_GRID 
 * object. 
 */ 

#include <stdlib.h> 
#include "../agb.h" 
#include "objects.h" 
#include "agb.h" 


/* 
 * Allocate memory for and return a pointer to an AGB_YIELD_GRID struct and 
 * initialize all fields to NULL. 
 * 
 * header: agb.h 
 */ 
extern AGB_YIELD_GRID *agb_yield_grid_initialize(void) {

	AGB_YIELD_GRID *agb_grid = (AGB_YIELD_GRID *) malloc (sizeof(
		AGB_YIELD_GRID)); 

	agb_grid -> grid = NULL; 
	agb_grid -> m = NULL; 
	agb_grid -> z = NULL; 
	agb_grid -> entrainment = 1; 

	return agb_grid; 

} 


/* 
 * Free up the memory stored in an AGB_YIELD_GRID struct 
 * 
 * header: agb.h 
 */ 
extern void agb_yield_grid_free(AGB_YIELD_GRID *agb_grid) { 

	if (agb_grid != NULL) {

		if ((*agb_grid).grid != NULL) {
			free(agb_grid -> grid); 
			agb_grid -> grid = NULL; 
		} else {} 

		if ((*agb_grid).m != NULL) {
			free(agb_grid -> m); 
			agb_grid -> m = NULL; 
		} else {} 

		if ((*agb_grid).z != NULL) {
			free(agb_grid -> z); 
			agb_grid -> z = NULL; 
		} else {} 

		free(agb_grid); 
		agb_grid = NULL; 

	} else {} 

} 


