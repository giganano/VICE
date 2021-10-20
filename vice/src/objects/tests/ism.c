/*
 * This file implements testing of the ism object's memory management
 */

#include <stdlib.h>
#include <string.h>
#include "../../objects.h"
#include "../../singlezone.h"
#include "singlezone.h"
#include "ism.h"


/*
 * Test the function which constructs an ism object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ism.h
 */
extern unsigned short test_ism_initialize(void) {

	ISM *test = ism_initialize();
	unsigned short result = (test != NULL &&
		(*test).mode != NULL &&
		(*test).specified == NULL &&
		(*test).star_formation_history == NULL &&
		(*test).eta == NULL &&
		(*test).enh == NULL &&
		(*test).tau_star == NULL
	);
	ism_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored in an ism object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ism.h
 */
extern unsigned short test_ism_free(void) {

	/* The destructor function should not modify the address */
	ISM *test = ism_initialize();
	void *initial_address = (void *) test;
	ism_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}


/*
 * Obtain a pointer to a test instance of the ISM object
 *
 * header: ism.h
 */
extern ISM *ism_test_instance(void) {

	ISM *test = ism_initialize();
	strcpy(test -> mode, "ifr");
	unsigned long i, N = TEST_SINGLEZONE_N_STEPS + BUFFER;
	test -> specified = (double *) malloc (N * sizeof(double));
	test -> star_formation_history = (double *) malloc (N * sizeof(double));
	test -> eta = (double *) malloc (N * sizeof(double));
	test -> tau_star = (double *) malloc (N * sizeof(double));
	test -> mass = 5e9;
	test -> star_formation_rate = 5e9;
	test -> infall_rate = 1e9;
	test -> schmidt_index = 0.5;
	test -> mgschmidt = 6e9;
	test -> smoothing_time = 0;
	test -> schmidt = 0;

	for (i = 0ul; i < N; i++) {
		test -> specified[i] = 1e9;
		test -> eta[i] = 1;
		test -> tau_star[i] = 1;
	}

	return test;

}

