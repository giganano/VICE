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
		(*test).interpolator != NULL &&
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

	test -> interpolator -> n_x_values = 7ul;
	test -> interpolator -> n_y_values = 15ul;
	test -> interpolator -> xcoords = (double *) malloc (
		(*(*test).interpolator).n_x_values * sizeof(double));
	test -> interpolator -> ycoords = (double *) malloc (
		(*(*test).interpolator).n_y_values * sizeof(double));

	unsigned short i, j;
	for (i = 0u; i < (*(*test).interpolator).n_x_values; i++) {
		/* masses are 1 - 7 */
		test -> interpolator -> xcoords[i] = 1 + i;
	}
	for (i = 0u; i < (*(*test).interpolator).n_y_values; i++) {
		/* metallicities are 0 - 0.014, in steps of 0.001 */
		test -> interpolator -> ycoords[i] = 0.001 * i;
	}

	test -> interpolator -> zcoords = (double **) malloc (
		(*(*test).interpolator).n_x_values * sizeof(double));
	for (i = 0u; i < (*(*test).interpolator).n_x_values; i++) {
		test -> interpolator -> zcoords[i] = (double *) malloc (
			(*(*test).interpolator).n_y_values * sizeof(double));
		for (j = 0u; j < (*(*test).interpolator).n_y_values; j++) {
			/*
			 * Fractional yield at a mass and metallicity is equal to the mass
			 * in units of the sun's mass times the metallicity.
			 */
			test -> interpolator -> zcoords[i][j] = (
				(*(*test).interpolator).xcoords[i] *
				(*(*test).interpolator).ycoords[j]
			);
		}
	}

	callback_2arg_free(test -> custom_yield);
	test -> custom_yield = callback_2arg_test_instance();
	test -> custom_yield -> user_func = NULL;

	return test;

}

