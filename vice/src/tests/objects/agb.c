/* 
 * This file implements testing of the agb_yield_grid object's memory management 
 */ 

#include <stdlib.h> 
#include "../../objects.h" 
#include "callback_2arg.h" 
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
		(*test).custom_yield != NULL && 
		(*test).grid == NULL && 
		(*test).m == NULL && 
		(*test).z == NULL && 
		(*test).n_m == 0ul && 
		(*test).n_z == 0ul && 
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


/* 
 * Obtain a pointer to test instance of the AGB_YIELD_GRID object 
 * 
 * header: agb.h 
 */ 
extern AGB_YIELD_GRID *agb_yield_grid_test_instance(void) { 

	AGB_YIELD_GRID *test = agb_yield_grid_initialize(); 

	test -> n_m = 7ul; 
	test -> n_z = 15ul; 
	test -> m = (double *) malloc ((*test).n_m * sizeof(double)); 
	test -> z = (double *) malloc ((*test).n_z * sizeof(double)); 

	unsigned short i, j; 
	for (i = 0u; i < (*test).n_m; i++) { 
		/* masses are 1 - 7 */ 
		test -> m[i] = 1 + i; 
	} 
	for (i = 0u; i < (*test).n_z; i++) { 
		/* metallicities are 0 - 0.014, in steps of 0.001 */ 
		test -> z[i] = 0.001 * i; 
	} 

	test -> grid = (double **) malloc ((*test).n_m * sizeof(double *)); 
	for (i = 0u; i < (*test).n_m; i++) {
		test -> grid[i] = (double *) malloc ((*test).n_z * sizeof(double)); 
		for (j = 0u; j < (*test).n_z; j++) {
			/* 
			 * Fractional yield at a mass and metallicity is equal to the mass 
			 * in units of the sun's mass times the metallicity. 
			 */ 
			test -> grid[i][j] = (*test).m[i] * (*test).z[j]; 
		} 
	} 

	callback_2arg_free(test -> custom_yield); 
	test -> custom_yield = callback_2arg_test_instance(); 
	test -> custom_yield -> user_func = NULL; 

	return test; 

}

