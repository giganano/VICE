/* 
 * This file implements testing of the agb_yield_grid object's memory management 
 */ 

#include <stdlib.h> 
#include "../../objects.h" 
#include "agb.h" 


/* 
 * Test the function which constructs an agb_yield_grid object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: agb.h 
 */ 
extern unsigned short test_agb_yield_grid_initialize(void) {

	AGB_YIELD_GRID *test = agb_yield_grid_initialize(); 
	unsigned short result = (test != NULL && 
		(*test).grid == NULL && 
		(*test).m == NULL && 
		(*test).z == NULL && 
		(*test).entrainment == 1 
	); 
	agb_yield_grid_free(test); 
	return result; 

} 


/* 
 * Test the function which frees the memory stored by an agb_yield_grid object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: agb.h 
 */ 
extern unsigned short test_agb_yield_grid_free(void) { 

	/* The destructor function should not modify the address */ 
	AGB_YIELD_GRID *test = agb_yield_grid_initialize(); 
	void *initial_address = (void *) test; 
	agb_yield_grid_free(test); 
	void *final_address = (void *) test; 
	return initial_address == final_address; 

}


