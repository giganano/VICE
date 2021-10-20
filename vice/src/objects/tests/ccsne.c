/*
 * This file implements testing of the ccsne_yield_specs object's memory
 * management
 */

#include <stdlib.h>
#include "../../objects.h"
#include "callback_1arg.h"
#include "ccsne.h"


/*
 * Test the function which constructs a ccsne_yield_specs object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ccsne.h
 */
extern unsigned short test_ccsne_yield_initialize(void) {

	CCSNE_YIELD_SPECS *test = ccsne_yield_initialize();
	unsigned short result = (test != NULL &&
		(*test).yield_ != NULL &&
		(*test).entrainment == 1
	);
	ccsne_yield_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored by a ccsne_yield_specs object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ccsne.h
 */
extern unsigned short test_ccsne_yield_free(void) {

	/* The destructor function should not modify the address */
	CCSNE_YIELD_SPECS *test = ccsne_yield_initialize();
	void *initial_address = (void *) test;
	ccsne_yield_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}


/*
 * Obtain a pointer to a test instance of the CCSNE_YIELD_SPECS object
 *
 * header: ccsne.h
 */
extern CCSNE_YIELD_SPECS *ccsne_yield_test_instance(void) {

	CCSNE_YIELD_SPECS *test = ccsne_yield_initialize();
	callback_1arg_free(test -> yield_);
	test -> yield_ = callback_1arg_test_instance();
	test -> yield_ -> assumed_constant = 0.01;
	return test;

}

