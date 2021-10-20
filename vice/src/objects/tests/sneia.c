/*
 * This file implements testing of the sneia_yield_specs object's memory
 * management
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "../../objects.h"
#include "../../sneia.h"
#include "callback_1arg.h"
#include "singlezone.h"
#include "sneia.h"


/*
 * Test the function which constructs a sneia_yield_specs object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: sneia.h
 */
extern unsigned short test_sneia_yield_initialize(void) {

	SNEIA_YIELD_SPECS *test = sneia_yield_initialize();
	unsigned short result = (test != NULL &&
		(*test).yield_ != NULL &&
		(*test).RIa == NULL &&
		(*test).dtd != NULL &&
		(*test).tau_ia == 1.5 &&
		(*test).t_d == 0.15 &&
		(*test).entrainment == 1
	);
	sneia_yield_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored in a sneia_yield_specs object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: sneia.h
 */
extern unsigned short test_sneia_yield_free(void) {

	/* The destructor function should not modify the address */
	SNEIA_YIELD_SPECS *test = sneia_yield_initialize();
	void *initial_address = (void *) test;
	sneia_yield_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}


/*
 * Obtain a pointer to a test instance of the SNEIA_YIELD_SPECS object
 *
 * header: sneia.h
 */
extern SNEIA_YIELD_SPECS *sneia_yield_test_instance(void) {

	SNEIA_YIELD_SPECS *test = sneia_yield_initialize();

	callback_1arg_free(test -> yield_);
	test -> yield_ = callback_1arg_test_instance();
	test -> yield_ -> assumed_constant = 0.01;
	strcpy(test -> dtd, "custom");

	unsigned long i, n = RIA_MAX_EVAL_TIME / TEST_SINGLEZONE_TIMESTEP_SIZE;
	test -> RIa = (double *) malloc (n * sizeof(double));
	for (i = 0ul; i < n; i++) {
		if (i * TEST_SINGLEZONE_TIMESTEP_SIZE < 0.1) {
			test -> RIa[i] = 0;
		} else {
			test -> RIa[i] = pow(i * TEST_SINGLEZONE_TIMESTEP_SIZE, -1);
		}
	}

	return test;

}

